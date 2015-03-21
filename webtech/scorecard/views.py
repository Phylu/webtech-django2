from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.core.urlresolvers import reverse

from scorecard.models import Course

class IndexView(generic.ListView):
    template_name = 'scorecard/index.html'
    model = Course

    def get_queryset(self):
        return Course.objects.get_queryset().order_by('-votes')

def vote(request, pk, vote):
    course = get_object_or_404(Course, pk=pk)
    if(vote == '1'):
        course.votes += 1
        course.save()
        return HttpResponseRedirect(reverse('scorecard:index'))
    elif(vote == '-1'):
        course.votes -= 1
        course.save()
        return HttpResponseRedirect(reverse('scorecard:index'))
    else:
        return Http404('Vote must be either 1 or -1')