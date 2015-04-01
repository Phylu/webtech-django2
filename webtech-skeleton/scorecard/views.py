from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Avg
import sys

from scorecard.models import Course, Lecturer


def redirect_to_index():
    return HttpResponseRedirect(reverse('scorecard:index'))

def update_vote(course, vote):
    vote = int(vote)
    if abs(vote) == 1:
        course.votes += vote
        course.save()
        return True
    return False

def vote(request, pk, vote):
    """
    You can either up- or down-vote a course
    The vote is saved in the model
    Then the user is redirected to the index page
    :param request: Request to work on
    :param pk:      Primary key of the Course
    :param vote:    1 or -1 depending on up/down-vote
    :return:        Redirect to Index view or 404 error
    """
    # If there is no course with the corresponding pk return an error
    course = get_object_or_404(Course, pk=pk)
    update_vote(course, vote)
    return redirect_to_index()


def statistics(request):
    """
    Show statistics page
    :param request:
    :return:
    """
    context = {
        'lecturer_count': "NA",
        'courses_count': "NA",
        'courses_votes_mean': "NA",
        'lecturer_best': "NA",
        'lecturer_best_votes_mean': "NA",
    }
    return render(request, 'scorecard/statistics.html', context)


def details(request, pk):
    """
    Show details page for course with primary key pk
    :param request:
    :param pk:
    :return:
    """
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'scorecard/details.html', {'course': course})


class IndexView(generic.ListView):
    """
    The index page is a generic ListView.
    All Courses are shown in a list
    """
    template_name = 'scorecard/index.html'  # Template to use
    model = Course  # Model to use

    def get_queryset(self):
        """
        Order the Courses by their votes begining from the course with most votes.
        """
        return Course.objects.get_queryset().order_by('-votes')
