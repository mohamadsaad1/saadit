from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Thread
from django.contrib.auth.views import LoginView





class Home(LoginView):
  template_name = 'home.html'

def threads_index(request):
  threads = Thread.objects.all()
  return render(request, 'threads/index.html', { 'threads': threads })

# def threads_index(request):
#     threads = Thread.objects.filter(status=1).order_by('-created_on')
#     return render(request, 'threads/index.html',{
#       "threads" : threads
#     })


def threads_detail(request, thread_id):
  thread= Thread.objects.get(id=thread_id)
  return render(request, 'threads/detail.html', {
    "thread" : thread
  })

class ThreadCreate(CreateView):
  model = Thread
  fields = '__all__'


class ThreadUpdate(UpdateView):
  model = Thread
  fields = ['title', 'slug', 'content']


class ThreadDelete(DeleteView):
  model = Thread
  success_url = '/threads'


