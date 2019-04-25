from django.db import models

# Add your models here
from django.db import models
from datetime import datetime
# Add your models here


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return 'Dr. {} {}'.format(self.first_name, self.last_name,
        )


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(editable = False, max_length=100)
    last_name = models.CharField(editable = False, max_length=100)
    #ssns in U.S. are 9 digits long
    ssn = models.CharField(max_length=9)
    email = models.EmailField()
    #allow 3 choices for gender
    GENDER_CHOICES =(('M', 'Male'),
                     ('F', 'Female'),
                     ('NB', 'Non-binary'))
    #gender will be represented as either 1 or 2 chars
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(editable =False, null=True)

    def __str__(self):
        return '[{} {}, {}]'.format(
            self.first_name,
            self.last_name,
            self.social_security_number
        )


