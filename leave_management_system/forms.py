from django import forms 
from .models import *
  
class Proj_img(forms.ModelForm): 
  
    class Meta: 
        model = tbl_profile 
        fields = ['emp_img'] 