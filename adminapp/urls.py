from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # admin reg + login
    path('', views.admin_login_page, name='admin_login_page'),
    path('admin_reg', views.admin_registration, name='admin_reg'),
    path('admin_activate/<uidb64>/<token>', views.admin_activate, name='admin_activate'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),

    # user / admin add recipe
    path('add_recipe_page', views.recipe_db, name='add_recipe_page'),
    path('add_recipe', views.recipe_db_rend, name='add_recipe'),

    # admin dashboard
    path('admin_dash', views.admin_das, name='admin_dash'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_read_more/<int:id>/', views.admin_read_more, name='admin_read_more'),
    path('users_list', views.users_list, name='users_list')

]
