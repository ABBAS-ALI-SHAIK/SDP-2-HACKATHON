from user import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='userhome'),
    path('login/', views.login_view, name='userlogin'),
    path('register/', views.register_view, name='userregister'),
    path('logout/', views.logout_view, name='userlogout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
]