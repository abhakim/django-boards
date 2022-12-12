from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('signin/', auth_views.LoginView.as_view(template_name='accounts/sign_in.html'), name='sign_in'),
    path('signout/', auth_views.LogoutView.as_view(), name='sign_out'),
    path('user_update/', views.UserUpdateView.as_view(), name='user_update'),
    
    re_path(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    re_path(r'^password_change_done/$', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),
    
    re_path(r'^reset/$',auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ), name='password_reset'),
    re_path(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    re_path(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
]
