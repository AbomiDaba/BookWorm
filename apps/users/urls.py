from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.reg_login, name= 'reg_log'),
    path('register', views.new_user),
    path('login', views.login),
    path('logout', views.logout),
    path('<int:user_id>', views.user_page)
]