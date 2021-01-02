from django.urls import path

from .views import login, add_task, signup, signout, index, update_task, delete_task

urlpatterns = [
    path("", index, name="index"),
    path('add_task/', add_task, name='add_task'),
    path("update/<int:pk>/", update_task, name="update_task"),
    path("delete/<int:pk>/", delete_task, name="delete_task"),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', signout, name='logout'),
]

