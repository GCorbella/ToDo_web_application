from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ToDo


class Log(LoginView):
    template_name = "base/login.html"
    field = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todos")


class SignIn(FormView):
    template_name = "base/signin.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todos")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignIn, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todos")
        return super(SignIn, self).get(*args,**kwargs)


class ToDoList(LoginRequiredMixin, ListView):
    model = ToDo
    context_object_name = "todos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todos"] = context["todos"].filter(user=self.request.user)
        context["count"] = context["todos"].filter(complete=False).count()

        search_value = self.request.GET.get("searcher") or ""
        if search_value:
            context["todos"] = context["todos"].filter(title__icontains=search_value)
        context["search_value"] = search_value
        return context


class ToDoDetail(LoginRequiredMixin, DetailView):
    model = ToDo
    context_object_name = "todo"


class CreateToDo(LoginRequiredMixin, CreateView):
    model = ToDo
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("todos")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateToDo, self).form_valid(form)


class EditToDo(LoginRequiredMixin, UpdateView):
    model = ToDo
    fields = '__all__'
    success_url = reverse_lazy("todos")


class DeleteToDo(LoginRequiredMixin, DeleteView):
    model = ToDo
    context_object_name = "todos"
    success_url = reverse_lazy("todos")
