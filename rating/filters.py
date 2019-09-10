import django_filters

from rating.models import Subject


class SubjectFilter(django_filters.FilterSet):
    basic_info = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Subject
        fields = ['shortcut', 'tutor']


class OpinionFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte', label='Minimal mark')

