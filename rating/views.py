import datetime

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_GET
from django.views.generic import FormView

from rating.filters import OpinionFilter
from rating.forms import InactiveSubjectForm
from rating.models import Subject, Opinion, User, Status


def find_subjects(request):
    subjects = Subject.objects.all().filter(status=Status.ACCEPTED.value)
    if request.GET.get('rating'):
        subjects = [subject for subject in subjects if
                    isinstance(subject.rating, float) and subject.rating > float(request.GET['rating'])]
    elif request.GET.get('number_of_opinions'):
        subjects = [subject for subject in subjects if
                    subject.number_of_opinions >= float(request.GET['number_of_opinions'])]
    print(subjects)
    return subjects


@require_GET
@login_required
def index(request):
    context = {'subjects': find_subjects(request),
               'logged_user': User.objects.filter(basic_info=request.user)[0],
               'opinions': Opinion.objects.all()}

    return render(request, 'rating/index.html', context)


class SubjectView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
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

    def test_func(self):
        subject = Subject.objects.filter(pk=self.kwargs['pk'])[0]
        return subject.status == Status.ACCEPTED.value


class AddSubjectView(LoginRequiredMixin, generic.CreateView):
    template_name = 'rating/add_subject.html'
    model = Subject
    fields = ['fullname', 'shortcut', 'tutor', 'basic_info']

    def form_valid(self, form):
        user = User.objects.get(basic_info=self.request.user)
        form.instance.user = user
        if user.basic_info.is_staff:
            form.instance.status = Status.ACCEPTED.value
        else:
            form.instance.status = Status.WAITING_FOR_CONFIRMATION.value
        # send_mail(
        #     'Subject added successfully',
        #     f'You just added subject written down below:\n{form.instance.whole_info()}',
        #     'pik.konsultacje@gmail.com',
        #     [form.instance.user.basic_info.email],
        #     fail_silently=False
        # )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('rating:index')


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


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        import django.contrib.auth.models as auth_model
        model = auth_model.User
        fields = ('username', 'email', 'password1', 'password2')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            basic_user = form.save()
            user = User(basic_info=basic_user)
            # user.basic_info.is_active = False
            user.basic_info.save()
            user.save()
            from django.db import connection
            print(connection.queries)
            return redirect('/account/login')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


class UserView(LoginRequiredMixin, generic.DetailView):
    template_name = 'rating/user.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = User.objects.get(basic_info=self.request.user)
        context['opinions'] = Opinion.objects.filter(user=logged_user).order_by('date')[:5]
        return context


class ActivateSubjectView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'rating/activate_subject.html'
    form_class = InactiveSubjectForm

    def form_valid(self, form):
        subjects_to_be_activated = form.cleaned_data.get('Inactive_Subjects')
        print(subjects_to_be_activated)
        for subject in Subject.objects.filter(pk__in=subjects_to_be_activated):
            subject.status = Status.ACCEPTED.value
            subject.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('rating:activate_subject')
