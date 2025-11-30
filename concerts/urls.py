from django.urls import path
from . import views

urlpatterns = [
    path('', views.concert_list, name='concert_list'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('concert/<int:concert_id>/artists/', views.artist_management, name='artist_management'),
    path('concert/<int:concert_id>/program/', views.program_management, name='program_management'), 
    path('artists/', views.artist_list, name='artist_list'),
    path('instruments/', views.instrument_list, name='instrument_list'),
]