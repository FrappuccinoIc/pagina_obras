from django.shortcuts import render

def home(req):
    return render(req, "core/home.html")

def info(req):
    return render(req, "core/info.html")

def pedidos(req):
    return render(req, "core/pedidos.html")