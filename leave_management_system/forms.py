from django import forms 
from .models import *
  
class Proj_img(forms.ModelForm): 
  
    class Meta: 
        model = tbl_profile 
        fields = ['emp_id','emp_img','emp_dob','emp_email','emp_phone','emp_address','emp_type','emp_discriptin','emp_last_edit'] 