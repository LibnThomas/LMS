from django.db import models
import datetime
from django.utils.timezone import now
import os
# from datetime import datetime
# Create your models here.


# print(datetime.date.today)
class tbl_leave(models.Model):
	# id_student = models.CharField(primary_key=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
	emp_id=models.IntegerField()
	emp_name=models.CharField(max_length=50)
	l_type=models.CharField(max_length=50)
	l_date=models.DateField(default=datetime.date.today)
	l_time=models.TimeField(auto_now_add=True)
	l_reason=models.CharField(max_length=200)
	l_days=models.IntegerField(null=True)
	l_status=models.CharField(max_length=10)
	l_year=models.CharField(max_length=5)
	l_from=models.DateField(null=True)
	l_to=models.DateField(null=True)
	l_r_reason=models.CharField(max_length=200,null=True)

	class Meta:
		db_table="tbl_leave"
			
def imgAuth(instance,filename):
	ex=filename.split(".")[-1]
	name1="img/"+str(instance.emp_id)+"."+ex
	return name1

class tbl_profile(models.Model):
	emp_id=models.IntegerField()
	emp_img=models.ImageField(upload_to=imgAuth)
	emp_dob=models.DateField(default=datetime.date.today)
	emp_email=models.CharField(max_length=50)
	emp_phone=models.CharField(max_length=15)
	emp_address=models.CharField(max_length=200)
	emp_type=models.CharField(max_length=50)
	emp_discriptin=models.CharField(max_length=200)
	emp_last_edit=models.DateField(default=datetime.date.today)

	class Meta:
		db_table="tbl_profile"

