from django.contrib import admin
from django.urls import path
from datlien import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('viewHubs/', views.viewHubs, name='viewHubs'),
    path('viewCentralHubs/', views.viewCentralHubs, name='viewCentralHubs'),
    path('addHub/', views.addHub, name='addHub'),
    path('addCentralHub/', views.addCentralHub, name='addCentralHub'),
    path('editCentralHub/<str:username>', views.editCentralHub, name='editCentralHub'),
    path('editHub/<str:username>', views.editHub, name='editHub'),
    path('prequest/', views.prequest, name='prequest'),
    path('porders/', views.porders, name='porders'),
    path('corders/', views.corders, name='corders'),
    path('approve/<int:id>', views.approve, name='approve'),
    path('pick/<int:id>', views.pick, name='pick'),
    path('ship/<int:id>', views.ship, name='ship'),
    path('transit/<int:id>', views.transit, name='transit'),
    path('receive/<int:id>', views.receive, name='receive'),
    path('out_for_delivery/<int:id>', views.out_for_delivery, name='out_for_delivery'),
    path('deliver/<int:id>', views.deliver, name='deliver'),
    path('profile/', views.profile, name="profile"),
    path('editprofile/', views.editprofile, name="editprofile"),
    path('users/', views.users, name="users"),
    path('orders_history/', views.orders_history, name="orders_history"),
    path('history/<int:id>', views.history, name="history"),
    path('c_hub_history/<int:id>', views.c_hub_history, name="c_hub_history"),
    path('hub_history/<int:id>', views.hub_history, name="hub_history"),
    path('viewStates/', views.viewStates, name='viewStates'),
    path('addCity/<int:id>', views.addCity, name='addCity'),
    path('state/<int:id>', views.state, name="state"),
    path('addDeliveryBoy/<int:id>', views.addDeliveryBoy, name="addDeliveryBoy"),
]