from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('utility/<int:utility_id>/', views.utility, name='utility'),
    path('month/', views.month, name='month')
]