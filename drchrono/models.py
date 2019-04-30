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
    date_of_birth = models.DateField(editable=False, null=True)

    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=25, null=True)
    zip_code = models.CharField(max_length=5, null=True)
    cell_phone = models.CharField(max_length=12, null=True)
    #stores path to patients photo on filesystem in db
    patient_pic = models.ImageField(upload_to='/photos', null=True)

    def __str__(self):
        return '[{},{} - {}, {}, {}]'.format(
            self.first_name,
            self.last_name,
            self.ssn,
            self.email,
            self.gender
        )

class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    duration = models.IntegerField()
    appt_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    checked_in = models.BooleanField(null=False)
    check_in_time = models.TimeField()
    appt_start_time = models.TimeField()
    appt_end_time = models.TimeField()

    def calc_wait_time(self):
        if self.checked_in:
            delta = self.appt_start_time - self.check_in_time
            mins = int(delta.total_secs/60)
            return mins
        else:
            return None

class Stats(models.Model):
    total_wait_time = models.TimeField()
    num_appts = models.IntegerField()

    def calc_avg_wait(self):
        avg = (self.total_wait_time.total_secs / self.num_appts)
        avg = int(avg / 60)
        return avg

    class Meta:
        abstract = True

class DailyStats(Stats):
    date = models.DateField(null=False)


class MonthlyStats(Stats):
    month = models.IntegerField(choices=MONTHS.items(), null=False)

    def get_month(self):
        return MONTHS.get(self.month)













