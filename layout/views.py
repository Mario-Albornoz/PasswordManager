from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def register_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'register.html')

def sign_in_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'sign-in.html')

def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')



