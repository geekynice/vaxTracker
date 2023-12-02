from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('elements/', views.elements, name='elements'),
    path('add-doctors/', views.add_doctors, name='add-doctors'),
    path('add-family/', views.add_family, name='add-family'),
    path('add-family-members/<uuid:family_id>/', views.add_family_members, name='add-family-members'),
    path('delete-member/<uuid:member_id>/', views.delete_member, name='delete-member'),
    path('delete-doctor/<uuid:user_id>/', views.delete_doctor, name='delete-doctor'),
    path('edit-member/<uuid:member_id>/', views.edit_member, name='edit-member'),
    path('edit-family/<uuid:family_id>/', views.edit_family, name='edit-family'),
    path('delete-family/<uuid:family_id>/', views.delete_family, name='delete-family'),
]