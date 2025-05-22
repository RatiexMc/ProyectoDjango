from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

def home_view(request):
    return render(request,'home.html')
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request,"accounts/login.html",{"error":"Credenciales Incorrectas"})
    return render(request, "accounts/login.html")