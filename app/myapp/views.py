from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Point
from django.shortcuts import render, redirect
from .forms import PointForm

def create_point(request, point_id=None):
    if point_id:
        point = get_object_or_404(Point, id=point_id)
    else:
        point = None

    if request.method == 'POST':
        form = PointForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PointForm(instance=point)
    
    points = Point.objects.all()
    return render(request, 'create_point.html', {'form': form, 'points': points, 'point': point})

def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    point.delete()
    return redirect('create_point')
