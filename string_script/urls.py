from django.urls import path
from . import views

urlpatterns = [
    path('main-page/', views.main, name='main-page'),
    path('', views.main),
]
