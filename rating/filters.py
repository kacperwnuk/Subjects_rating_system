import django_filters

from rating.models import Subject, Opinion


class SubjectFilter(django_filters.FilterSet):
    basic_info = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Subject
        fields = ['shortcut', 'tutor']


class OpinionFilter(django_filters.FilterSet):

    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte', label='Minimalna ocena')

    # rating = django_filters.NumberFilter(choices=STATUS_CHOICES, lookup_expr='gt')
    # year__gt = django_filters.NumberFilter(name='date', lookup_expr='year__gt')

    class Meta:
        model = Opinion
        fields = ['date']
