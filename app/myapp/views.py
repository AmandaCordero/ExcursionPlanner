from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    context = {
        'title': 'My App',
        'message': 'Hello, this is a message from the backend!',
        'items': ['Item 1', 'Item 2', 'Item 3']
    }
    return render(request, 'index.html', context)

def my_method(request):
    data = {
        'message': 'Hello, this is a response from the backend!'
    }
    return JsonResponse(data)
