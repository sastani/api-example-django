from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import *
from social_django.models import UserSocialAuth
from django.http import JsonResponse
from .models import *
from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint,PatientEndpoint, APIException
from .forms import *
import datetime
import pytz

class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'login.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark
        magic will fetch it for us if we've already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get
        doctor details. If this succeeds, we've proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        self.request.session['access_token'] = access_token


        # Grab the first doctor from the list; normally this would be the whole
        # practice group, but your hackathon account probably only has one doctor in it.
        doctor = DoctorEndpoint(access_token).get_doctor()
        #self.request.session['doctor'] = doctor.id

        patient = PatientEndpoint(access_token).get_patients(doctor)
        appt = AppointmentEndpoint(access_token).get_appoinments(doctor, None)
        # Get patients and appointments for the doctor and store it in the local DB

        return doctor

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        return kwargs

class CheckinView(FormView):
    template_name = 'checkin.html'
    form_class = CheckinForm
    success_url = '/demographics/'

    def validate_form(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        ssn = form.cleaned_data.get('ssn')

        try:
            patient = Patient.objects.get(first_name=first_name,last_name=last_name,ssn=str(ssn))
        except Patient.DoesNotExist:
            patient = None
        if patient:
            access_token = self.request.session['access_token']
            a = AppointmentEndpoint(access_token)
            appts = Appointment.today.filter(patient=patient.id)
            date = datetime.now().isoformat()
            for appt in appts:
                updated_fields = {
                    'status': 'Checked In',
                    'checked_in': True,
                    'check_in_time': date
                }

                data = {
                    'status': 'Checked In',
                    'updated_at': date
                }
                response = {}
                try:
                    response = a.update(appt.id, data)
                    updated_appt, created = Appointment.objects.update_or_create(updated_fields, pk=appt.id)
                    self.request.session['checkedin_patient'] = patient.id
                    return super(CheckinView, self).validate_form(form)
                except APIException:
                    context = {
                        'form': form
                    }
                    return render(self.request, "checkin.html", context)

            context = {
                'form': form
            }
            return render(self.request, "checkin.html", context)

        context = {
            'form': form
        }
        return render(self.request, "checkin.html", context)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs = super(DashboardView, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        # appointments = self.make_api_request()

        #get all the appointments/update database if neccessary
        Appointment.objects.all()
        #only get todays from database
        appts = Appointment.objects.get_today()
        kwargs['appointments'] = appts
        return kwargs

class DemographicsView(TemplateView):
    template_name = 'update_demographic_info.html'
    form_class = DemographicsForm
    success_url = '/checkin_success/'

    def get_initial(self):
        initial = {}
        patient_id = self.request.session.get('checkedin_patient')

        patient = Patient.objects.filter(pk=patient_id).values()[0]
        if patient:
            initial = patient
        return initial

    def validate_form(self, form):

        email = form.cleaned_data.get('email')

        dob = form.cleaned_data.get('date_of_birth')
        gender = form.cleaned_data.get('gender')
        address = form.cleaned_data.get('address')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        zip_code = form.cleaned_data.get('zip_code')
        cell_phone = form.cleaned_data.get('cell_phone')

        patient_id = self.request.session.get('checkedin_patient')

        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            patient = None
        print(patient)

        if patient:
            access_token = self.request.session.get('access_token')
            p = PatientEndpoint(access_token)

            updated_fields = {
                'email': email,
                'gender': gender,
                'dob': dob,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'cell_phone': cell_phone,
            }

            response = {}
            try:
                response = p.update(patient_id, updated_fields)
                updated_patient, created = Patient.objects.update_or_create(updated_fields, pk=patient_id)
                return super(DemographicsView, self).validate_form(form)
            except APIException:
                context = {
                    'form': form
                }
                return render(self.request, "checkin.html", context)

        context = {
            'form': form
        }
        return render(self.request, "checkin.html", context)


class AnalyticsView(TemplateView):
    template_name = 'analytics.html'


