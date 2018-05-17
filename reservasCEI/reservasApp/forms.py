from django import forms

class EspacioForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
    espacio_id = forms.IntegerField()
