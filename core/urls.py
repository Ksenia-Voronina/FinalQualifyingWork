from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('reply/<int:id>/', views.reply_to_user, name='reply_to_user'),
    path('faq/', views.faq_view, name='faq'),
]