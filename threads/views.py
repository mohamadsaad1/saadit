from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from .models import Thread



def threads_index(request):
  threads = Thread.objects.all()
  return render(request, 'threads/index.html', { 'threads': threads })

class ThreadList(generic.ListView):
    queryset = Thread.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class ThreadDetail(generic.DetailView):
    model = Thread
    template_name = 'thread_detail.html'

class ThreadCreate(CreateView):
  model = Thread
  fields = '__all__'