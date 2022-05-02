from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import path
from adminapp import views as admin_views
from django.contrib.auth import views as auth_views

from .views import UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView

urlpatterns = [
    path('', views.user_home, name='index_home'),
    path('profile_return_home', views.user_profile_return_home, name='profile_return_home'),

    path('user_profile', views.user_index, name='user_profile'),
    path('user_signin_reg', views.user_login_reg, name='user_login_reg'),
    path('user_sign_in', views.user_signin, name='user_sign_in'),
    path('user_registration', views.user_register, name='user_registration'),
    path('activate/<uidb64>/<token>', views.user_activate, name='activate'),
    path('user_sign_out', views.user_sign_out, name='user_sign_out'),
    # path('user_forgot_password', views.user_forgot_password, name='user_forgot_password'),

    path('user_contact_form', views.user_contact_form, name='user_contact_form'),
    path('user_contact', views.user_contact, name='user_contact'),

    # profile activities
    path('user_update_prof', views.user_update_prof, name='user_update_prof'),

    # reset password

    path('password_reset', UserPasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),



    # Change Password
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/change-password.html', success_url='/'), name='change_password'),

    # admin urls / views
    path('user_add_recipe', admin_views.recipe_db_rend, name='user_add_recipe'),
    path('userAdmin_login', admin_views.admin_login_page, name='userAdmin_login_page'),

    # about
    path('develp_about',views.blog_about,name='develp_about'),

    # shows data
    path('show_recipe',views.show,name='show_recipe'),
    path('readmore',views.read_more,name='read_more')

]
