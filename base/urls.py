from django.urls import path
from .views import ToDoList, ToDoDetail, CreateToDo, EditToDo, DeleteToDo, Log, SignIn
from django.contrib.auth.views import LogoutView

urlpatterns = [path("", ToDoList.as_view(), name="todos"),
               path("login/", Log.as_view(), name="login"),
               path("signin/", SignIn.as_view(), name="signin"),
               path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
               path("todo/<int:pk>", ToDoDetail.as_view(), name="todo"),
               path("create-todo/", CreateToDo.as_view(), name="create-todo"),
               path("edit-todo/<int:pk>", EditToDo.as_view(), name="edit-todo"),
               path("delete-todo/<int:pk>", DeleteToDo.as_view(), name="delete-todo")]
