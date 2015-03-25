from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib import messages

from scorecard.models import Course

class IndexView(generic.ListView):
    """
    The index page is a generic ListView.
    All Courses are shown in a list
    """
    template_name = 'scorecard/index.html'  # Template to use
    model = Course                          # Model to use

    def get_queryset(self):
        """
        Order the Courses by their votes begining from the course with most votes.
        """
        return Course.objects.get_queryset().order_by('-votes')


def updateVote(course, vote):
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
    if updateVote(course, vote):
        messages.add_message(request, messages.SUCCESS, "Vote Successful!")
        return HttpResponseRedirect(reverse('scorecard:index'))
    else:
        # Vote invalid
        messages.add_message(request, messages.ERROR, "Vote Not Successful!")
        return HttpResponseRedirect(reverse('scorecard:index'))