from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
import requests



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
            return redirect('/libros/')
        else:
            return render(request,"accounts/login.html",{"error":"Credenciales Incorrectas"})
    return render(request, "accounts/login.html")

def register_view(request):
    mensaje = None
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        # Validar que las contraseñas coincidan
        if password != confirm:
            error = "Las contraseñas no coinciden."
            return render(request, "accounts/register.html", {
                "error": error,
                "mensaje": mensaje
            })

        # Enviar datos al endpoint de registro
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/register/",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        if response.status_code == 201:
            mensaje = "¡Usuario registrado correctamente!"
        else:
            error_data = response.json()
            error = (
                error_data.get("username") or
                error_data.get("email") or
                error_data.get("password") or
                "Error al registrar."
            )

    return render(request, "accounts/register.html", {"mensaje": mensaje, "error": error})
def logout_view(request):
    logout(request)
    return redirect('home')

