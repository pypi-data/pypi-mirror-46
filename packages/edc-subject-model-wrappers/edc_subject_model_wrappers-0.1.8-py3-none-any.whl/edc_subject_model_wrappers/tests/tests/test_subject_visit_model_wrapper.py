from django.test import TestCase, tag
from edc_dashboard.url_names import url_names
from edc_subject_model_wrappers import SubjectVisitModelWrapper
from edc_utils import get_utcnow
from edc_visit_schedule import site_visit_schedules

from ..models import SubjectVisit, Appointment
from ..visit_schedule import visit_schedule1


class TestModelWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        url_names.register(
            "subject_dashboard_url",
            "subject_dashboard_url",
            "edc_subject_model_wrapper",
        )
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        url_names.registry.pop("subject_dashboard_url")
        super().tearDownClass()

    def setUp(self):
        self.subject_identifier = "12345"
        site_visit_schedules._registry = {}
        site_visit_schedules.register(visit_schedule=visit_schedule1)

    @tag("1")
    def test_(self):
        model_obj = SubjectVisit(report_datetime=get_utcnow())
        wrapper = SubjectVisitModelWrapper(model_obj=model_obj)
        self.assertEqual(wrapper.model, "edc_subject_model_wrappers.subjectvisit")
        self.assertEqual(wrapper.model_cls, SubjectVisit)

    def test_knows_appointment(self):
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            appt_reason="scheduled",
            visit_schedule_name="visit_schedule1",
            schedule_name="schedule1",
            visit_code="1000",
        )
        subject_visit = SubjectVisit.objects.create(
            appointment=appointment, report_datetime=get_utcnow()
        )
        wrapper = SubjectVisitModelWrapper(model_obj=subject_visit)
        self.assertEqual(str(appointment.id), wrapper.appointment)
