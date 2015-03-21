from django.test import TestCase
from django.core.urlresolvers import reverse

from scorecard.models import Course

def create_courses():
    """
    Create some coursese
    """
    Course.objects.create(course_title="EADS", votes=0)
    Course.objects.create(course_title="ITSec", votes=0)
    Course.objects.create(course_title="Webtech", votes=0)

class ScoreboardTest(TestCase):

    def test_if_error_msg_if_no_course(self):
        """
        If there is no Course existing, the Index should present an error msg
        """
        response = self.client.get(reverse('scorecard:index'))
        self.assertContains(response, 'No courses available')

    def test_if_courses_are_shown_without_voting(self):
        """
        If courses are created, they should be shown on the index page
        """
        create_courses()
        response = self.client.get(reverse('scorecard:index'))
        self.assertQuerysetEqual(response.context['object_list'], ['<Course: EADS>', '<Course: ITSec>', '<Course: Webtech>'])

    def test_if_voting_redirect_is_correct(self):
        """
        If a vote is counted, the user is redirected
        """
        create_courses()
        response = self.client.get(reverse('scorecard:vote', kwargs={'pk':1, 'vote':1}))
        self.assertEqual(response.status_code, 302)

    def test_if_voting_increased_counter(self):
        """
        If a positive vote is counted, the counter should increase
        """
        create_courses()
        response = self.client.get(reverse('scorecard:index'))
        old_votes = response.context['object_list'].get(pk=1).votes
        response = self.client.get(reverse('scorecard:vote', kwargs={'pk':1, 'vote':1}))
        response = self.client.get(reverse('scorecard:index'))
        new_votes = response.context['object_list'].get(pk=1).votes
        self.assertEqual(old_votes + 1, new_votes)

    def test_if_voting_decreased_counter(self):
        """
        If a negative vote is counted, the counter should decrease
        """
        create_courses()
        response = self.client.get(reverse('scorecard:index'))
        old_votes = response.context['object_list'].get(pk=1).votes
        response = self.client.get(reverse('scorecard:vote', kwargs={'pk':1, 'vote':-1}))
        response = self.client.get(reverse('scorecard:index'))
        new_votes = response.context['object_list'].get(pk=1).votes
        self.assertEqual(old_votes - 1, new_votes)