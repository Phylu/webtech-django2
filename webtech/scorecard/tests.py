from django.test import TestCase
from django.core.urlresolvers import reverse

from scorecard.models import Course, Lecturer


class ScoreboardTest(TestCase):
    lecturer_1 = Lecturer()
    lecturer_2 = Lecturer()
    course_1 = Course()
    course_2 = Course()
    course_3 = Course()

    def setUp(self):
        """
        Create some courses & lecturers
        """
        self.lecturer_1 = Lecturer.objects.create(first_name="Janosch", last_name="Maier")
        self.lecturer_2 = Lecturer.objects.create(first_name="A", last_name="B")
        self.course_1 = Course.objects.create(course_title="EADS", votes=0, lecturer=self.lecturer_1)
        self.course_2 = Course.objects.create(course_title="ITSec", votes=0, lecturer=self.lecturer_2)
        self.course_3 = Course.objects.create(course_title="Webtech", votes=0, lecturer=self.lecturer_2)

    def delete_courses(self):
        """
        Delete all courses for test
        :return:
        """
        self.course_1.delete()
        self.course_2.delete()
        self.course_3.delete()

    def vote(self, course, up_down):
        """
        Vote for course with vote up_down
        :param course: Course object
        :param up_down: 1 or -1
        :return: old_votes, new_votes
        """
        response = self.client.get(reverse('scorecard:index'))
        old_votes = response.context['object_list'].get(pk=course.pk).votes
        self.client.get(reverse('scorecard:vote', kwargs={'pk': course.pk, 'vote': up_down}))
        response = self.client.get(reverse('scorecard:index'))
        new_votes = response.context['object_list'].get(pk=course.pk).votes
        return old_votes, new_votes

    def vote_again(self):
        """
        Reset has_already_voted hook
        :return:
        """
        self.client.get(reverse('scorecard:vote_again'))

    def test_lecturer_str(self):
        """
        Test if the __str__ method of lecturer works properly
        :return:
        """
        lecturer = Lecturer.objects.create(first_name='Janosch', last_name='Maier')
        self.assertEqual(lecturer.__str__(), 'Janosch Maier')

    def test_great_course_for_bad_course(self):
        """
        Return false if course has less then 100 votes
        :return:
        """
        course = Course.objects.create(course_title="EADS", votes=100, lecturer=self.lecturer_1)
        self.assertEqual(course.is_great_course(), False)

    def test_great_course_for_great_course(self):
        """
        Return false if course has less then 100 votes
        :return:
        """
        course = Course.objects.create(course_title="EADS", votes=101, lecturer=self.lecturer_1)
        self.assertEqual(course.is_great_course(), True)


    def test_error_msg_if_no_course(self):
        """
        If there is no Course existing, the Index should present an error msg
        """
        self.delete_courses()
        response = self.client.get(reverse('scorecard:index'))
        self.assertContains(response, 'No courses available')

    def test_if_courses_are_shown_without_voting(self):
        """
        If courses are created, they should be shown on the index page
        """
        response = self.client.get(reverse('scorecard:index'))
        self.assertQuerysetEqual(response.context['object_list'], ['<Course: EADS>', '<Course: ITSec>', '<Course: Webtech>'])

    def test_if_voting_redirect_is_correct(self):
        """
        If a vote is counted, the user is redirected
        """
        response = self.client.get(reverse('scorecard:vote', kwargs={'pk':1, 'vote':1}))
        self.assertEqual(response.status_code, 302)

    def test_if_voting_increased_counter(self):
        """
        If a positive vote is counted, the counter should increase
        """
        vote = 1
        old_votes, new_votes = self.vote(self.course_1, vote)
        self.assertEqual(old_votes + vote, new_votes)

    def test_if_voting_decreased_counter(self):
        """
        If a negative vote is counted, the counter should decrease
        """
        vote = -1
        old_votes, new_votes = self.vote(self.course_1, vote)
        self.assertEqual(old_votes + vote, new_votes)

    def test_if_voting_increased_counter_twice_without_reset(self):
        """
        If a positive vote is counted, the counter should increase
        """
        vote = 1
        old_votes, not_used = self.vote(self.course_1, vote)
        not_used, new_votes = self.vote(self.course_1, vote)
        self.assertEqual(old_votes + vote, new_votes)


    def test_if_voting_increased_counter_twice_with_reset(self):
        """
        If a positive vote is counted, the counter should increase
        """
        vote = 1
        old_votes, not_used = self.vote(self.course_1, vote)
        self.vote_again()
        not_used, new_votes = self.vote(self.course_1, vote)
        self.assertEqual(old_votes + (2 * vote), new_votes)


    def test_statistic(self):
        """
        Statistic should show correct values
        :return:
        """
        vote = 1
        self.vote(self.course_1, vote)
        self.vote_again()
        self.vote(self.course_1, vote)
        response = self.client.get(reverse('scorecard:statistics'))
        self.assertEqual(response.context['lecturer_best'], self.lecturer_1)
        self.assertEqual(response.context['lecturer_best_votes_mean'], 2)