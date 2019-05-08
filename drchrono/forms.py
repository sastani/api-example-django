from django import forms
from django.forms import widgets
import datetime

# Add your forms here
class CheckinForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    # date_of_birth = forms.DateField(initial=datetime.date.today)
    ssn = forms.RegexField(
        required=True,
        regex='^\d{3}-?\d{2}-?\d{4}$',
        error_messages={
            'invalid': 'SSN must be in following format: XXX-XX-XXXX'
        }
    )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name = first_name.strip()
        if first_name == '':
            raise forms.ValidationError("First name not entered")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name = last_name.strip()
        if last_name == '':
            raise forms.ValidationError("Last name not entered")
        return last_name


class DemographicsForm(forms.Form):

    date_of_birth = forms.DateField(
        required=False,
        error_messages={
            'invalid': 'Date must be in the format: YYYY-MM-DD'
        }
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICES)
    address = forms.CharField(required=False)
    zip_code = forms.RegexField(
        required=False,
        regex='^(\d{5})?$',
        error_messages={
            'invalid': 'Zip code must be in the format: XXXXX',
        }
    )
    city = forms.CharField(required=False)
    state = forms.RegexField(required=False,
                             regex='^([A-Z]{2})?$',
                             error_messages={
                                 'invalid': 'State abbreviation only',
                             })
    email = forms.EmailField(required=False)
    cell_phone = forms.RegexField(
        required=False,
        regex='^\(\d{3}\)\s*\d{3}-\d{4}$',
        error_messages={
            'invalid': 'Phone number must be in format: (XXX) XXX-XXXX',
        }
    )