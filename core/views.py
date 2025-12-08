from django.shortcuts import render
from django.contrib.auth import logout

def home(req):
    return render(req, "core/home.html")

def info(req):
    return render(req, "core/info.html")

def pedidos(req):
    return render(req, "core/pedidos.html")