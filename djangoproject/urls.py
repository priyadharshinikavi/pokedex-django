from django.contrib import admin
from django.urls import path
from pooki import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('pokedex/', views.pokedex, name='pokedex'),
    path('logout/', views.logout_view, name='logout'),
]
