from django.shortcuts import render
from django.views import generic
from .models import Article

class IndexView(generic.ListView):
    model = Article

class DetailView(generic.DetailView):
    model = Article

class CreateView(generic.edit.CreateView):
    model = Article
    fields = '__all__'

class UpdateView(generic.edit.UpdateView):
    model = Article
    fields = '__all__'