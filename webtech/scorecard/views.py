from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.core.urlresolvers import reverse

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
        Order the Ccurses by their votes begining from the course with most votes.
        """
        return Course.objects.get_queryset().order_by('-votes')

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
    if(vote == '1'):
        # Increase Vote
        course.votes += 1
        course.save()
        return HttpResponseRedirect(reverse('scorecard:index'))
    elif(vote == '-1'):
        # Decrease Vote
        course.votes -= 1
        course.save()
        return HttpResponseRedirect(reverse('scorecard:index'))
    else:
        # Vote invalid
        return Http404('Vote must be either 1 or -1')