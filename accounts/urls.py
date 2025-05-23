from django.urls import path
from .views import RegisterView, login_view, register_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),                      # ← API con DRF
    path('login/', TokenObtainPairView.as_view(), name='login'),                     # ← API para token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),        # ← API para refrescar JWT
    path('iniciar-sesion/', login_view, name='iniciar_sesion'),                      # ← Vista HTML login
    path('registrarse/', register_view, name='register_view'),                       # ← Vista HTML registro 
    path('cerrar-sesion/', logout_view, name='cerrar_sesion'),                       # ← Cerrar sesión 
]
