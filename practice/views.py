from django.shortcuts import render
from django.views import generic
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class IndexView(generic.ListView):
    model = Article

class DetailView(generic.DetailView):
    model = Article

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['title', 'content', 'image', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ['title', 'content', 'image', 'category']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('practice:index')