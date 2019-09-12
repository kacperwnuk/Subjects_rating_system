from django import forms

from rating.models import Subject, Status


class InactiveSubjectForm(forms.Form):
    Inactive_Subjects = forms.MultipleChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(InactiveSubjectForm, self).__init__(*args, **kwargs)
        self.options = (
            (subject.id, f'{subject.shortcut} {subject.fullname} created by {subject.user.basic_info.username}')
            for subject in Subject.objects.all().filter(status=Status.WAITING_FOR_CONFIRMATION.value))
        self.fields['Inactive_Subjects'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                     choices=self.options)
