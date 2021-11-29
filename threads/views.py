from django.shortcuts import render
from django.views import generic
from .models import Thread


class ThreadList(generic.ListView):
    queryset = Thread.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class ThreadDetail(generic.DetailView):
    model = Thread
    template_name = 'thread_detail.html'