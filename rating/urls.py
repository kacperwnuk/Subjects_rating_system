from django.urls import path
from django_filters.views import FilterView

from rating import views
from rating.filters import SubjectFilter, OpinionFilter

app_name = 'rating'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', FilterView.as_view(filterset_class=SubjectFilter, template_name='rating/search_subject.html'), name='search'),
    path('add_subject', views.AddSubjectView.as_view(), name='add_subject'),
    path('<int:pk>/subject', views.SubjectView.as_view(), name='subject'),
    path('<int:pk>/opinion', views.OpinionView.as_view(), name='opinion'),
    path('<int:pk>/opinion/modify', views.ModifyOpinionView.as_view(), name='modify_opinion'),
    path('register/', views.register, name='register'),
    path('<int:pk>/profile/', views.UserView.as_view(), name='user'),
    path('<int:pk>/subject/add_opinion', views.AddOpinionView.as_view(), name='add_opinion'),
]

