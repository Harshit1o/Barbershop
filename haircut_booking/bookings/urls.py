from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('logout/', views.user_logout, name='logout'),
    path('book', views.book_appointment, name='book_appointment'),
    path('confirm/', views.finalize_appointment, name='confirm_appointment'),  # Added confirm appointment
    path('verify_payment/', views.payment_verification, name='payment_verification'),
    path('recommendation/', views.recommendation, name='recommendation'),
]
