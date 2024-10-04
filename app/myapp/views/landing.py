from django.shortcuts import render

def pagina_inicio(request):
    return render(request, 'index.html')