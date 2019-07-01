from django.urls import path

from rating import views

app_name = 'rating'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/subject', views.SubjectView.as_view(), name='subject'),
    path('<int:pk>/opinion', views.OpinionView.as_view(), name='opinion'),
    path('register/', views.register, name='register'),
    path('<int:pk>/profile/', views.UserView.as_view(), name='user'),
    path('<int:pk>/subject/add_opinion', views.AddOpinionView.as_view(), name='add_opinion')
]
