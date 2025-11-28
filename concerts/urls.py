from django.urls import path
from . import views

urlpatterns = [
    path('', views.concert_list, name='concert_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('no-access/', views.no_access_view, name='no_access'),
    path('', views.concert_list, name='concert_list'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('concert/<int:concert_id>/artists/', views.artist_management, name='artist_management'),
    path('concert/<int:concert_id>/program/', views.program_management, name='program_management'), 
    path('artists/', views.artist_list, name='artist_list'),
    path('instruments/', views.instrument_list, name='instrument_list'),
]