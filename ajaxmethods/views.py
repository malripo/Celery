from django.shortcuts import render
from . models import *
from django.http import JsonResponse, HttpResponse

# Create your views here.
def home_page(request):
    likes = Like.objects.first()
    likes.count = 0
    likes.save()    
    return render(request, 'ajaxmethods/ajax.html')

def json_data(request):
    if request.method =="GET":
        likes = Like.objects.first()
        likes.count += 1
        likes.save()
        return JsonResponse({'likes': likes.count})
    
    if request.method =="POST":
        city = request.POST.get('city')
        return JsonResponse({'city': city}) 
    
def html_data(request): 
    if request.method =="GET":
        likes = Like.objects.first()
        likes.count += 1
        likes.save()
        return HttpResponse(likes.count)   
    
    if request.method =="POST":
        city = request.POST.get('city')
        return HttpResponse(f'<div>{city}</div>')  
