from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import SearchForm


class IndexView(generic.ListView, SearchForm):
    model = Article

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')


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


def search(request):
    searchForm = SearchForm(request.GET)
    if searchForm.is_valid():
        keyword = searchForm.cleaned_data['keyword']
        object_list = Article.objects.filter(title__contains=keyword).order_by('-created_at')
        context = {
            'message': '記事の検索',
            'object_list': object_list,
            'searchForm': searchForm,
            'comment': 'タイトルをキーワードに含む記事はありません',
        }
    else:
        searchForm = SearchForm()
        context = {
            'message': '記事の検索',
            'searchForm': searchForm,
            'comment': 'ヒットした記事がここに表示されます',
        }

    return render(request, 'practice/search.html', context)
