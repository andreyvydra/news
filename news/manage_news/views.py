from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm

from .models import News, NewsForm
from django.http import HttpResponseNotAllowed, Http404


class MainView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            news = News.objects.filter(author=request.user)
            ctx = {'news': news}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {})


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class AddNewsView(CreateView):
    fields = ['title', 'text', 'image', 'tags', 'file', 'ís_urgent', 'category']
    model = News
    success_url = '/'
    template_name = 'add_edit_news.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.form_class = NewsForm(request.POST)
            ctx = {
                'form': self.form_class
            }
            return render(request, AddNewsView.template_name, ctx)
        else:
            raise Http404()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for tag in form.cleaned_data['tags']:
            self.object.tags.add(tag)
        self.object.save()
        return super().form_valid(form)


class EditNewsView(UpdateView):
    fields = ['title', 'text', 'image', 'tags', 'file', 'ís_urgent', 'category']
    model = News
    success_url = '/'
    template_name = 'add_edit_news.html'

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
        return self.queryset.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        news_id = int(self.kwargs['news_id'])
        queryset = queryset.filter(id=news_id)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404('Страница не была найдена')
        if not (obj.author == self.request.user) or\
                not self.request.user.is_authenticated:
            raise Http404('Страница не была найдена')
        return obj


class DeleteNewsView(DeleteView):
    model = News
    success_url = '/'
    template_name = 'news_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return redirect('/')

    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
        return self.queryset.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        news_id = int(self.kwargs['news_id'])
        queryset = queryset.filter(id=news_id)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404('Страница не была найдена')
        if not (obj.author == self.request.user) or\
                not self.request.user.is_authenticated:
            raise Http404('Страница не была найдена')
        return obj
