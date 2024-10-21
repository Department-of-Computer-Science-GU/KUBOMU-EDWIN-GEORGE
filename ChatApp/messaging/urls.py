# messaging/urls.py

from django.urls import path
from . import views
from .views import register 

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('message/<int:id>/', views.message_view, name='message_view'),
    path('login/', views.login_view, name='login'),  # Custom login page
    path('logout/', views.logout_view, name='logout'),
    # Optionally, add this to handle /accounts/login/
    path('accounts/login/', views.login_view), 
    path('register/', register, name='register'),
    path('message/<int:id>/', views.message_view, name='message_view'),
]
