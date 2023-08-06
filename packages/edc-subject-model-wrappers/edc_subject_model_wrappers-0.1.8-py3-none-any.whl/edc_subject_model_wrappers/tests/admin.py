from django.contrib.admin import AdminSite as DjangoAdminSite
from edc_locator.models import SubjectLocator

from .models import SubjectConsent, SubjectVisit, Appointment


class AdminSite(DjangoAdminSite):
    pass


edc_subject_model_wrappers_admin = AdminSite(name="edc_subject_model_wrappers_admin")

edc_subject_model_wrappers_admin.register(Appointment)
edc_subject_model_wrappers_admin.register(SubjectConsent)
edc_subject_model_wrappers_admin.register(SubjectLocator)
edc_subject_model_wrappers_admin.register(SubjectVisit)
