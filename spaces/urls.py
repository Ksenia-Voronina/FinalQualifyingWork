from django.urls import path
from . import views

app_name = 'spaces'

urlpatterns = [
    path('', views.SpaceListView.as_view(), name='list'),
    path('<slug:slug>/', views.SpaceDetailView.as_view(), name='detail'),
]