from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic

from rating.models import Subject, Opinion, User


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'rating/index.html'

    def get_queryset(self):
        return Subject.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.filter(basic_info=self.request.user)[0]
        return context


class SubjectView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/subject.html'
    model = Subject


class OpinionView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/opinion.html'
    model = Opinion


class AddOpinionView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rating.add_opinion.html'
    model = Opinion
    fields = ['title', 'text', 'date', 'rating']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = Subject.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user = User.objects.filter(basic_info=self.request.user)[0]
        form.instance.subject = Subject.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            basic_user = form.save()
            user = User(basic_info=basic_user)
            user.save()
            return redirect('/account/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class UserView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/user.html'
    model = User

