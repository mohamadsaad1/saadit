from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Thread
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required





class Home(LoginView):
  template_name = 'home.html'


def threads_index(request):
  threads = Thread.objects.filter(user=request.user)
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
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)


class ThreadUpdate(UpdateView):
  model = Thread
  fields = ['title', 'slug', 'content']


class ThreadDelete(DeleteView):
  model = Thread
  success_url = '/threads'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('threads')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)


