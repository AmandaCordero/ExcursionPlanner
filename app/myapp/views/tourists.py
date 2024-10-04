from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect

import json

from ..models import Tourist
from ..forms import TouristForm

def create_tourist(request, tourist_id=None):
    if tourist_id:
        tourist = get_object_or_404(Tourist, id=tourist_id)
    else:
        tourist = None

    if request.method == 'POST':
        form = TouristForm(request.POST, instance=tourist)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TouristForm(instance=tourist)
    
    tourists = Tourist.objects.all()
    return render(request, 'create_tourist.html', {'form': form, 'tourists': tourists, 'tourist': tourist})

def delete_tourist(request, tourist_id):
    tourist = get_object_or_404(Tourist, id=tourist_id)
    tourist.delete()
    return redirect('create_tourist')

def get_tourists(request):
    tourists = list(Tourist.objects.all().values())
    return JsonResponse(tourists, safe=False)

def save_tourists(request):
    tourists = list(Tourist.objects.all().values())
    if len(tourists) > 0:
        # Guardar los datos de los turistas
        with open('./myapp/utils/tourists_data.json', 'w') as file:
            json.dump(tourists, file, indent=4)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay turistas guardados'})
