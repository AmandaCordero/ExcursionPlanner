from django import forms
from django.core.exceptions import ValidationError
from .models import Point, Edge, Tourist

def validate_decimal_range(value):
    if not (0 <= value <= 1):
        raise ValidationError('El valor debe estar entre 0 y 1.')

class PointForm(forms.ModelForm):
    characteristic_1 = forms.FloatField(label='Characteristic 1', validators=[validate_decimal_range])
    characteristic_2 = forms.FloatField(label='Characteristic 2', validators=[validate_decimal_range])
    characteristic_3 = forms.FloatField(label='Characteristic 3', validators=[validate_decimal_range])
    characteristic_4 = forms.FloatField(label='Characteristic 4', validators=[validate_decimal_range])

    class Meta:
        model = Point
        fields = ['x', 'y', 'height', 'point_id']

    def __init__(self, *args, **kwargs):
        super(PointForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.characteristics:
            characteristics = self.instance.characteristics
            self.fields['characteristic_1'].initial = characteristics[0] if len(characteristics) > 0 else None
            self.fields['characteristic_2'].initial = characteristics[1] if len(characteristics) > 1 else None
            self.fields['characteristic_3'].initial = characteristics[2] if len(characteristics) > 2 else None
            self.fields['characteristic_4'].initial = characteristics[3] if len(characteristics) > 3 else None

    def save(self, commit=True):
        instance = super(PointForm, self).save(commit=False)
        instance.characteristics = [
            self.cleaned_data['characteristic_1'],
            self.cleaned_data['characteristic_2'],
            self.cleaned_data['characteristic_3'],
            self.cleaned_data['characteristic_4'],
        ]
        if commit:
            instance.save()
        return instance

class EdgeForm(forms.ModelForm):
    characteristic_1 = forms.FloatField(label='Characteristic 1', validators=[validate_decimal_range])
    characteristic_2 = forms.FloatField(label='Characteristic 2', validators=[validate_decimal_range])

    class Meta:
        model = Edge
        fields = ['point1', 'point2', 'distance']

    def __init__(self, *args, **kwargs):
        super(EdgeForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.characteristics:
            characteristics = self.instance.characteristics
            self.fields['characteristic_1'].initial = characteristics[0] if len(characteristics) > 0 else None
            self.fields['characteristic_2'].initial = characteristics[1] if len(characteristics) > 1 else None

    def save(self, commit=True):
        instance = super(EdgeForm, self).save(commit=False)
        instance.characteristics = [
            self.cleaned_data['characteristic_1'],
            self.cleaned_data['characteristic_2'],
        ]
        if commit:
            instance.save()
        return instance
    
    def clean(self):
        cleaned_data = super().clean()
        point1 = cleaned_data.get('point1')
        point2 = cleaned_data.get('point2')      
        
        if point1 and point2 and point1.point_id >= point2.point_id:
            raise forms.ValidationError('El ID del punto 1 debe ser menor que el ID del punto 2.')

        return cleaned_data


class TouristForm(forms.ModelForm):
    characteristic_1 = forms.FloatField(label='Characteristic 1', validators=[validate_decimal_range])
    characteristic_2 = forms.FloatField(label='Characteristic 2', validators=[validate_decimal_range])
    characteristic_3 = forms.FloatField(label='Characteristic 3', validators=[validate_decimal_range])
    characteristic_4 = forms.FloatField(label='Characteristic 4', validators=[validate_decimal_range])
    characteristic_5 = forms.FloatField(label='Characteristic 5', validators=[validate_decimal_range])
    characteristic_6 = forms.FloatField(label='Characteristic 6', validators=[validate_decimal_range])

    class Meta:
        model = Tourist
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(TouristForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.characteristics:
            characteristics = self.instance.characteristics
            self.fields['characteristic_1'].initial = characteristics[0] if len(characteristics) > 0 else None
            self.fields['characteristic_2'].initial = characteristics[1] if len(characteristics) > 1 else None
            self.fields['characteristic_3'].initial = characteristics[2] if len(characteristics) > 2 else None
            self.fields['characteristic_4'].initial = characteristics[3] if len(characteristics) > 3 else None
            self.fields['characteristic_5'].initial = characteristics[4] if len(characteristics) > 4 else None
            self.fields['characteristic_6'].initial = characteristics[5] if len(characteristics) > 5 else None

    def save(self, commit=True):
        instance = super(TouristForm, self).save(commit=False)
        instance.characteristics = [
            self.cleaned_data['characteristic_1'],
            self.cleaned_data['characteristic_2'],
            self.cleaned_data['characteristic_3'],
            self.cleaned_data['characteristic_4'],
            self.cleaned_data['characteristic_5'],
            self.cleaned_data['characteristic_6'],
        ]
        if commit:
            instance.save()
        return instance

