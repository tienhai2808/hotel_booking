from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(template_name='pr_form.html'), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDoneView.as_view(template_name='pr_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='pr_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(template_name='pr_complete.html'), name='password_reset_complete'),
    path('my/', my, name='my'),
    path('my/create-hotel/', create_hotel, name='create_hotel'),
    path('my/edit/', edit, name='edit'),
    path('my/edit/hotel/', edit_hotel, name='edit_hotel'),
    path('my/edit/change-password/', change_password, name='change_password'),
    path('hotel/<slug:hotel_slug>/', hotel_detail, name='hotel_detail'),
    path('hotel/<slug:hotel_slug>/<slug:room_slug>/', room_detail, name='room_detail'),
    path('my/hotel/create-room/', create_room, name='create_room'),
    path('my/edit/hotel/<slug:room_slug>/', edit_room, name='edit_room'),
    path('my/hotel/rooms/', rooms, name='rooms'),
    path('my/hotel/create-voucher/', create_voucher, name='create_voucher'),
    path('my/hotel/vouchers/', vouchers, name='vouchers'),
    path('my/hotel/vouchers/<int:id_km>/', edit_voucher, name='edit_voucher'),
    path('my/orders/', my_order, name='my_order'),
    path('my/hotel/orders/', orders, name='orders'),
    path('my/hotel/orders/<int:id_order>/', order_detail, name='order_detail'),
    path('my/hotel/', my_hotel, name='my_hotel'),
    path('search/', search, name='search'),
    path('my/enjoys/', my_enjoy, name='my_enjoy')
]