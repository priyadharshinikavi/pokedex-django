from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

# Home page (optional)
def home(request):
    return render(request, 'home.html')

# Register
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')

# Login
def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('pokedex')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Pokédex Page (Protected)
@login_required(login_url='login')
def pokedex(request):
    context = {}
    if 'pokemon' in request.GET:
        pokemon_name = request.GET['pokemon'].lower()
        url = f"https://pokeapi.co/api/v2/pokemon/ditto"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            context['pokemon'] = {
                'name': data['name'],
                'image': data['sprites']['front_default'],
                'types': [t['type']['name'] for t in data['types']],
                'abilities': [a['ability']['name'] for a in data['abilities']]
            }
        else:
            context['error'] = "Pokémon not found"
    return render(request, 'pokedex.html', context)
