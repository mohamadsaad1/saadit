from django.db import models
from django.urls import reverse
# Import the User
from django.contrib.auth.models import User

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Thread(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='saadit_threads')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
      return reverse('threads_detail', kwargs={'thread_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=250)
  thread = models.OneToOneField(Thread, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for thread_id: {self.thread_id} @{self.url}"