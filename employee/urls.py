from django.urls import path
from .views import committee_dashboard
from . import views, views_tupot

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('check-username/', views.check_username, name='check_username'),
    path('change-password/', views.change_password, name='change_password'),
    path('edit-children/', views.edit_children, name='edit_children'),
    path('logout/', views.logout_view, name='logout'),
    path('committee-dashboard/', committee_dashboard, name='committee_dashboard'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('committee-dashboard/export-excel/', views.export_dashboard_excel, name='export_dashboard_excel'),
    path('tu-pot/', views_tupot.tu_pot, name='tu_pot'),
    path('update_birthday_gift/', views.update_birthday_gift, name='update_birthday_gift'),
    path('update_tet_gift/', views.update_tet_gift, name='update_tet_gift'),
    path('update_mooncake_gift/', views.update_mooncake_gift, name='update_mooncake_gift'),
    path('update_luckymoney_gift/', views.update_luckymoney_gift, name='update_luckymoney_gift'),
    path('update_june_gift/', views.update_june_gift, name='update_june_gift'),
    path('update_autumn_gift/', views.update_autumn_gift, name='update_autumn_gift'),
]
