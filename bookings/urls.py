from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='list'),
    path('create/<int:space_id>/', views.booking_create, name='create'),
    path('<int:id>/', views.booking_detail, name='detail'),
    path('<int:id>/cancel/', views.booking_cancel, name='cancel'),
]