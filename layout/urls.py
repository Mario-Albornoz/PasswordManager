from django.urls import path, include

from layout import views

urlpatterns = [

    path('home/', views.home_view, name='home'),
    path('authentication/', views.register_view, name='authentication'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
]