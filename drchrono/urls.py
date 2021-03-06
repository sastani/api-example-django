from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

import views


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^analytics/$', views.AnalyticsView.as_view(), name='analytics'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^checkin/$', views.CheckinView.as_view(), name='checkin'),
    url(r'^demographics/$', views.DemographicsView.as_view(), name='demographics')
]