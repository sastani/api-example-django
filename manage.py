#!/usr/bin/env python
import os
import sys
import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drchrono.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

    from drchrono.endpoints import DoctorEndpoint
    from drchrono.views import DoctorWelcome
    token = DoctorWelcome().get_token()
    d = DoctorEndpoint(token).get_doctor()
    print(d)


