from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from leave_management_system import views

urlpatterns=[
	path('',views.login1,name="login1"),
	path('Admin',views.p_admin,name="Main_Admin"),
	path('admin_home',views.admin_home,name="admin_home"),
	path('User_profile/',views.userprofile,name="userprofile"),
	path('user_home',views.user_home,name="user_home"),
	path('admin_user_profile',views.admin_user_profile,name="admin_user_profile"),
	path('forgotpass',views.forgotpass,name="forgotpass"),
	path('change_pass',views.change_pass,name="change_pass"),
	path('manager_view',views.manager_view,name="manager_view"),
	path('User_profile/User_profile_edit',views.user_profile_edit,name="userprofile_edit"),
	path('User_profile/Applay_Leave',views.applay_leave,name="applay_leave"),
	path('User_profile/msg',views.msg,name="msg"),
	path('User_profile/leave_history',views.leave_history,name="leave_history"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)