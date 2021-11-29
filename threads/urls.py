from django.urls import path
from . import views

urlpatterns = [
  # localhost:8000/
    path('', views.ThreadList.as_view(), name='home'),

    path('<slug:slug>/', views.ThreadDetail.as_view(), 
    name='thread_detail'), 

    path('create/', views.ThreadCreate.as_view(), name='threads_create'),
]