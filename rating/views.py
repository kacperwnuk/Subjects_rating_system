import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import generic
from django.views.decorators.http import require_GET

from rating.filters import OpinionFilter
from rating.models import Subject, Opinion, User


def find_subjects(request):
    subjects = Subject.objects.all()
    if request.GET.get('rating'):
        subjects = [subject for subject in subjects if
                    isinstance(subject.rating, float) and subject.rating > float(request.GET['rating'])]
    elif request.GET.get('number_of_opinions'):
        subjects = [subject for subject in subjects if subject.number_of_opinions >= float(request.GET['number_of_opinions'])]
    print(subjects)
    return subjects


@require_GET
@login_required
def index(request):
    context = {'subjects': find_subjects(request),
                   'logged_user': User.objects.filter(basic_info=request.user)[0],
                   'opinions': Opinion.objects.all()}

    return render(request, 'rating/index.html', context)


class SubjectView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/subject.html'
    model = Subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.filter(pk=self.kwargs['pk'])[0]
        context['subject'] = subject
        qs = subject.opinion_set
        context['filter'] = OpinionFilter(self.request.GET, queryset=qs)
        print(context)
        return context


class AddSubjectView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rating/add_subject.html'
    model = Subject
    fields = ['fullname', 'shortcut', 'tutor', 'basic_info']

    def form_valid(self, form):
        form.instance.user = User.objects.get(basic_info=self.request.user)
        # send_mail(
        #     'Subject added successfully',
        #     f'You just added subject written down below:\n{form.instance.whole_info()}',
        #     'pik.konsultacje@gmail.com',
        #     [form.instance.user.basic_info.email],
        #     fail_silently=False
        # )
        return super().form_valid(form)


class OpinionView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/opinion.html'
    model = Opinion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_user'] = User.objects.get(basic_info=self.request.user)
        return context


class AddOpinionView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rating/add_opinion.html'
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


class ModifyOpinionView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'rating/modify_opinion.html'
    model = Opinion
    fields = ['title', 'text', 'date', 'rating']

    def form_valid(self, form):
        form.instance.last_edited = datetime.date.today()
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            basic_user = form.save()
            user = User(basic_info=basic_user)
            user.basic_info.is_active = False
            user.basic_info.save()
            user.save()
            return redirect('/account/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class UserView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/user.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = User.objects.get(basic_info=self.request.user)
        context['opinions'] = Opinion.objects.filter(user=logged_user).order_by('date')[:5]
        return context
