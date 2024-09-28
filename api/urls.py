from django.urls import path
from .views import (
    verify_user,
    reject_user,
    add_family_member,
    get_family_members,
    edit_family_member,
    delete_family_member,
    get_all_users,
    user_login,
    user_signup,
)

urlpatterns = [
    # User Authentication
    path('auth/login/', user_login, name='user_login'),
    path('auth/signup/', user_signup, name='user_signup'),
    
    # Family Member Management
    path('users/<int:user_id>/family/add/', add_family_member, name='add_family_member'),
    path('users/<int:user_id>/family/', get_family_members, name='get_family_members'),
    path('users/<int:user_id>/family/<int:family_member_id>/', edit_family_member, name='edit_family_member'),
    path('users/<int:user_id>/family/<int:family_member_id>/delete/', delete_family_member, name='delete_family_member'),
    
    # Users List
    path('users/', get_all_users, name='get_users_list'),

    # User Verification and Rejection
    path('users/verify/<int:user_id>/<int:admin_id>/', verify_user, name='verify_user'),
    path('users/reject/<int:user_id>/<int:admin_id>/', reject_user, name='reject_user'),
]
