from django.shortcuts import render , redirect
from .models import ContactMessage

def save(request):
    ob = ContactMessage()
    ob.name = request.POST.get('name')
    ob.email = request.POST.get('email')
    ob.subject = request.POST.get('subject')
    ob.message = request.POST.get('message')
    ob.save()
    return redirect('/contactus')
