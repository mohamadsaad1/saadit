from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Thread, Photo
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3


S3_BASE_URL = "https://s3.us-east-2.amazonaws.com/"
BUCKET = "saadit-bucket"



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
  fields = ['title','content', 'status',]
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  
    form.instance.author = self.request.user
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
  

def add_photo(request, thread_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
  
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
  
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
    
      photo = Photo(url=url, thread_id=thread_id)
    
      thread_photo = Photo.objects.filter(thread_id=thread_id)
      if thread_photo.first():
        thread_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('threads_detail', thread_id=thread_id)




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


