from django.shortcuts import render, redirect
from.models import customer
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def main(request):
    return render(request, 'login.html')

