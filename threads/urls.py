from django.urls import path
from . import views

urlpatterns = [
    # localhost:8000/
    path('', views.Home.as_view(), name='home'),

    # localhost:8000/threadlist
    path('threadlist', views.ThreadList.as_view(), name='threadlist'),

    path('<slug:slug>/', views.ThreadDetail.as_view(), 
    name='thread_detail'), 

    path('threads/create', views.ThreadCreate.as_view(), name='thread_create'),

    path('<slug:slug>/update/', views.ThreadUpdate.as_view(), name='thread_update'),
    path('<slug:slug>/delete/', views.ThreadDelete.as_view(), name='thread_delete'),

]