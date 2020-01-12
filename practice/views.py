from django.shortcuts import render
from django.views import generic
from .models import Article

class IndexView(generic.ListView):
    model = Article
    template_name = 'index.html'