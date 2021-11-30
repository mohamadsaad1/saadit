from django.urls import path
from . import views

urlpatterns = [
    # localhost:8000/
    path('', views.Home.as_view(), name='home'),

    # localhost:8000/threadlist
    path('threads/', views.threads_index, name='threads_index'),

    path('<int:thread_id>/', views.threads_detail, 
    name='threads_detail'), 

    path('threads/create', views.ThreadCreate.as_view(), name='thread_create'),

    path('<int:pk>/update/', views.ThreadUpdate.as_view(), name='threads_update'),
    path('<int:pk>/delete/', views.ThreadDelete.as_view(), name='threads_delete'),
    path('accounts/signup/', views.signup, name='signup'),

]