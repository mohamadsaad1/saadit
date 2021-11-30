from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Thread
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView




class Home(LoginView):
  template_name = 'home.html'

@login_required
def threads_index(request):
  threads = Thread.objects.all()
  return render(request, 'threads/index.html', { 'threads': threads })

# def threads_index(request):
#     threads = Thread.objects.filter(status=1).order_by('-created_on')
#     return render(request, 'threads/index.html',{
#       "threads" : threads
#     })
@login_required
def threads_detail(request, thread_id):
  thread= Thread.objects.get(id=thread_id)
  return render(request, 'threads/detail.html', {
    "thread" : thread
  })

class ThreadCreate(LoginRequiredMixin, CreateView):
  model = Thread
  fields = ['title','content', 'author', 'status',]
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)


class ThreadUpdate(LoginRequiredMixin, UpdateView):
  model = Thread
  fields = ['title', 'content']


class ThreadDelete(LoginRequiredMixin, DeleteView):
  model = Thread
  success_url = '/threads/'

# def threads_delete(request, thread_id):
#     thread = Thread.objects.get(id=thread_id)
#     if request.user == thread.author.user:
#         thread.delete()
#     return redirect('threads/')

# class ThreadVoteToggle(RedirectView):

#     def get_redirect_url(self, *args ,**kwargs):

#         obj = get_object_or_404(Thread, pk=self.kwargs['pk'])
#         url_ = obj.get_absolute_url() 
#         user = self.request.user
#         if user.is_authenticated():
#             if user in obj.votes_total.all():
#                 # you could remove the user if double upvote or display a message or what ever you want here
#                 obj.votes_total.remove(user)
#             else:
#                 obj.votes_total.add(user)

#         return url_
  





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
      return redirect('threads_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)


