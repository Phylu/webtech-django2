from django.test import TestCase
from django.core.urlresolvers import reverse

from scorecard.models import Course, Lecturer


class ScoreboardTest(TestCase):

    def setUp(self):
        pass