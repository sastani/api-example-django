from django.db import models
from django.utils import timezone
from django.utils.dates import MONTHS
from datetime import datetime
# Add your models here


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return 'Dr. {} {}'.format(self.first_name, self.last_name,
        )

class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    #ssns are 9 digits long, 2 extra chars for dashes
    ssn = models.CharField(editable=False, max_length=11)
    email = models.EmailField()
    #allow 3 choices for gender
    GENDER_CHOICES = (('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Other'))
    #gender will be represented by 1 char
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(editable=False, null=True)

    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=25, null=True)
    zip_code = models.CharField(max_length=5, null=True)
    cell_phone = models.CharField(max_length=12, null=True)
    #stores path to patients photo on filesystem in db
    patient_pic = models.ImageField(upload_to='photos', null=True)

    def __str__(self):
        return '[{},{} - {}, {}, {}]'.format(
            self.first_name,
            self.last_name,
            self.ssn,
            self.email,
            self.gender
        )

class AppointmentQuerySet(models.QuerySet):
    todays_date = datetime.now()
    day = todays_date.day
    month = todays_date.month
    year = todays_date.year


    def today(self):
        return self.filter(appt_time__year=self.year,
                           appt_time__month=self.month,
                           appt_time__day=self.day).order_by('appt_time')

    def future(self):
        return None

class AppointmentManager(models.Manager):

    def get_queryset(self):
        return AppointmentQuerySet(self.model, using=self._db)

    def get_today(self):
        return self.get_queryset().today()


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    duration = models.IntegerField()
    appt_time = models.DateTimeField()
    exam_room = models.IntegerField()
    status = models.CharField(max_length=20, null=False, default="")
    reason = models.CharField(max_length=255, null=False, default="")
    checked_in = models.BooleanField(null=False, default=False)
    check_in_time = models.TimeField(null=True)
    appt_start_time = models.TimeField(null=True)
    appt_end_time = models.TimeField(null=True)
    objects = AppointmentManager()

    @staticmethod
    def patient_checked_in(status):
        if (status in ("Checked In", "In Room", "Complete", "In Session")):
            return True
        else:
            return False

    def calc_wait_time(self):
        if self.checked_in:
            delta = self.appt_start_time - self.check_in_time
            mins = int(delta.total_secs / 60)
            return mins
        else:
            return None

class Stats(models.Model):
    total_wait_time = models.TimeField()
    num_appts = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)


    def calc_avg_wait(self):
        avg = (self.total_wait_time.total_secs / self.num_appts)
        avg = int(avg / 60)
        return avg

    class Meta:
        abstract = True

class DailyStats(Stats):
    date = models.DateField(primary_key=True, null=False)


class MonthlyStats(Stats):
    month = models.IntegerField(primary_key=True, choices=MONTHS.items(), null=False)

    def get_month(self):
        return MONTHS.get(self.month)













