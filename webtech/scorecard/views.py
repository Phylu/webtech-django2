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

def set_voted(request, voted):
    request.session['has_voted'] = voted

def has_already_voted(request):
    return request.session.get('has_voted', False)

def get_best_lecturer_with_mean():
    best_lecturer = None
    best_lecturer_mean = -sys.maxsize
    lecturer_votes = Course.objects.values('lecturer').annotate(avg_votes=Avg('votes'))
    for lecturer_vote in lecturer_votes:
        if lecturer_vote['avg_votes'] > best_lecturer_mean:
            best_lecturer = lecturer_vote['lecturer']
            best_lecturer_mean = lecturer_vote['avg_votes']
    best_lecturer = Lecturer.objects.get(pk=best_lecturer)
    return best_lecturer, best_lecturer_mean

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
    if has_already_voted(request):
        messages.add_message(request, messages.ERROR, "You have already voted!")
    elif update_vote(course, vote):
        set_voted(request, True)
        messages.add_message(request, messages.SUCCESS, "Vote Successful!")
    else:
        # Vote invalid
        messages.add_message(request, messages.ERROR, "Vote Not Successful!")
    return redirect_to_index()


def statistics(request):
    """
    Show statistics page
    :param request:
    :return:
    """
    best_lecturer, best_lecturer_mean = get_best_lecturer_with_mean()
    context = {
        'lecturer_count': Lecturer.objects.count(),
        'courses_count': Course.objects.count(),
        'courses_votes_mean': Course.objects.aggregate(Avg('votes'))['votes__avg'],
        'lecturer_best': best_lecturer,
        'lecturer_best_votes_mean': best_lecturer_mean,
    }
    return render(request, 'scorecard/statistics.html', context)


def vote_again(request):
    """
    Remove vote counter from session
    :param request:
    :return:
    """
    set_voted(request, False)
    return redirect_to_index()


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
