from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
import json
from .models import tbl_leave,tbl_profile
from .forms import *
import numpy as np

import datetime
from datetime import date,datetime
from django.utils.timezone import now

def userauth(request):
	print(request.POST)
	print("session value name",request.session["user_username"])
	print("Session values in username :",request.session.get("user_username"))
	print("token 2")
	if (request.user.is_authenticated):
		loguser=request.user.first_name+" "+request.user.last_name
		print("User :"+request.user.first_name+" "+request.user.last_name)
	else:
		print("token 6")
		return redirect('login1')
		print("token 7")
		
	if(request.POST.get("logout")!=None):
		logout(request)
		del request.session["user_username"]
		print("token 4")
		return redirect('login1')
		print("token 8")

def login1(request):
	try:
		name=""
		print("Session values in username common :",request.session.get("user_username"))
		if(request.POST.get("login")!=None):
			user=authenticate(username=request.POST["unam"],password=request.POST["pass"])
			if(user!=None):
				login(request,user)
				if(user.is_superuser):
					q=User.objects.filter(username=request.POST['unam'])

					print("Session values in username admin :",request.session.get("user_username"))
					if(request.session.get("user_username")!=None and request.session.get("user_username")!=""):
						print(request.session.keys())
						return render(request,"home.html",{"msg":"One Session is already Running"})
					else:
						request.session['user_username']=name

					for i in q:
						name=i.first_name+" "+i.last_name
					print(request.session["user_username"])
					return redirect("admin_home")
				else:
					q=User.objects.filter(username=request.POST['unam'])

					print("Session values in username user :",request.session.get("user_username"))
					if(request.session.get("user_username")!=None and request.session.get("user_username")!=""):
						print(request.session.keys())
						return render(request,"home.html",{"msg":"One Session is already Running"})
					else:
						request.session['user_username']=name

					for i in q:
						name=i.first_name+" "+i.last_name
					return redirect("user_home")
			else:
				return render(request,"home.html",{"msg":"Incorrect User Name/Password"})

		if(request.POST.get("btn_signin")!=None):
			try:
				a=User.objects.get(username=request.POST["uname"])
				return render(request,"home.html",{"msg":"User Name Exists"})
			except:
				if(request.POST["pass"]==request.POST["conf_pass"]):
					q=User.objects.create_user(username=request.POST["uname"],password=request.POST["pass"],first_name=request.POST["fname"],last_name=request.POST["lname"])
					q.save()
				else:
					return render(request,"home.html",{"msg":"Password Doesn't Match"})

		return render(request,'home.html')
	except Exception as e:
		print("error : ",e)
		return render(request,'home.html')

def admin_home(request):
	userauth(request)
	try:
		print(request.POST)

		q=tbl_leave.objects.filter(l_status="Approved").order_by("-id")
		q1=tbl_leave.objects.filter(l_status="Pending").order_by("-id")
		q2=tbl_leave.objects.filter(l_status="Rejected").order_by("-id")
		q3=User.objects.filter(is_superuser=False)

		if(request.POST.get("btn_profile")!=None):
			print("button click works")
			ans=admin_user_profile(request)
			print(ans,"hello ::::::::::::::::::::::::::")
			return render(request,"admin_home.html",{"approved":q,"pending":q1,"rejected":q2,"employes":q3,"ans":ans,"pag":"active in","display":"block;"})

		if(request.POST.get("btn_approve")!=None):
			print("before update")
			q4=tbl_leave.objects.get(id=request.POST["btn_approve"])
			q4.l_status="Approved"
			q4.save()
			print("after update")

		if(request.POST.get("btn_reject")!=None):
			print("before update")
			q4=tbl_leave.objects.get(id=request.POST["btn_reject"])
			q4.l_status="Rejected"
			q4.l_r_reason=request.POST["reject_reason"]
			q4.save()
			print("after update")


	except Exception as e:
		print("Error ::::",e)
		return render(request,"Usr_profile.html")

	return render(request,"admin_home.html",{"approved":q,"pending":q1,"rejected":q2,"employes":q3,"pag1":"active in"})

def admin_user_profile(request):
	# dic={}
	print(request.POST)
	print("enna kuzapam")
	print(request.POST.get('btn_view'))
	print("hello word")
	if(request.POST.get('btn_profile')!=None):
		q1=tbl_profile.objects.filter(emp_id=request.POST['btn_profile'])
		q=User.objects.filter(id=request.POST['btn_profile'])
		for i in q:
			name=i.first_name+" "+i.last_name

		for i in q1:
			ans="<div class='row'><div class='row'><div class='col-md-12' style='text-align: center;align-content: center;'><img src='/static/img/demoimg1.gif' style='height: 100px;width: 100px;border-radius: 50%;object-fit: cover;background: linear-gradient(to top left, #ffffff -21%, #00BCD4  123%);'><br>			<label style='text-shadow: 1px 1px 1px black;font-weight: bolder;font-size: 20px;'>"+name+"</label></div></div></div><hr><div class='row'><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Address</div><div class='col-md-9'><label>: "+i.emp_address+"</label></div></div><div class='row'><div class='col-md-3'>DOB</div><div class='col-md-9'><label>: "+str(i.emp_dob)+"</label></div></div><div class='row'><div class='col-md-3'>Email</div><div class='col-md-9'><label>: "+i.emp_email+"</label></div></div><div class='row'><div class='col-md-3'>Phone</div><div class='col-md-9'><label>: "+str(i.emp_phone)+"</label></div></div></div><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Type</div><div class='col-md-9'><label>: "+i.emp_type+"</label></div></div><div class='row'><div class='col-md-3'>Quote</div><div class='col-md-9'><label>: "+i.emp_discriptin+"</label></div></div></div></div>"

	elif(request.POST.get('btn_view')!=None):
		q=User.objects.filter(id=request.POST['btn_view'])
		q1=tbl_profile.objects.filter(emp_id=request.POST['btn_view'])
		for i in q:
			name=i.first_name+" "+i.last_name

		for i in q1:
			ans="<div class='row'><div class='row'><div class='col-md-12' style='text-align: center;align-content: center;'><img src='/static/img/demoimg1.gif' style='height: 100px;width: 100px;border-radius: 50%;object-fit: cover;background: linear-gradient(to top left, #ffffff -21%, #00BCD4  123%);'><br>			<label style='text-shadow: 1px 1px 1px black;font-weight: bolder;font-size: 20px;'>"+name+"</label></div></div></div><hr><div class='row'><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Address</div><div class='col-md-9'><label>: "+i.emp_address+"</label></div></div><div class='row'><div class='col-md-3'>DOB</div><div class='col-md-9'><label>: "+str(i.emp_dob)+"</label></div></div><div class='row'><div class='col-md-3'>Email</div><div class='col-md-9'><label>: "+i.emp_email+"</label></div></div><div class='row'><div class='col-md-3'>Phone</div><div class='col-md-9'><label>: "+str(i.emp_phone)+"</label></div></div></div><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Type</div><div class='col-md-9'><label>: "+i.emp_type+"</label></div></div><div class='row'><div class='col-md-3'>Quote</div><div class='col-md-9'><label>: "+i.emp_discriptin+"</label></div></div></div></div>"

	print("\nAnswer profile :",ans)
	return ans
	# dic["ans"]=ans
	# dic["status"]=True
	# print(dic)
	# jsondata=json.dumps(dic)
	# return HttpResponse(jsondata,content_type="application/json")

def user_home(request):
	print("token 1")
	userauth(request)
	print("token 3")

	q=tbl_leave.objects.filter(l_status="Approved",emp_id=request.user.id).order_by("-id")
	q1=tbl_leave.objects.filter(l_status="Pending",emp_id=request.user.id).order_by("-id")
	q2=tbl_leave.objects.filter(l_status="Rejected",emp_id=request.user.id).order_by("-id")
	q3=tbl_leave.objects.filter(l_status="Rejected",emp_id=request.user.id).aggregate(Sum("l_days"))
	q3=tbl_leave.objects.filter(l_status="Rejected",emp_id=request.user.id).aggregate(Sum("l_days"))

	return render(request,"Usr_Home.html",{"pending":q1,"accepted":q,"reject":q2})

def userprofile(request):
	userauth(request)
	try:
		print(request.POST)
		qq=User.objects.get(username=request.user.username)
		empid=qq.id
		tbl_profile.objects.get_or_create(emp_id=empid)

		q1=tbl_profile.objects.get(emp_id=empid)
		fnam=qq.first_name
		lnam=qq.last_name
		address=q1.emp_address
		email=q1.emp_email
		dob=q1.emp_dob.strftime("%d-%m-%Y")
		number=q1.emp_phone
		quote=q1.emp_discriptin
		typ=q1.emp_type
		name1=fnam+" "+lnam
		print(fnam,lnam,address,email,dob,number,quote,typ,name1)

	except Exception as e:
		print("Error ::::",e)
		return render(request,"Usr_profile.html")

	return render(request,"Usr_profile.html",{"fnam":fnam,"lnam":lnam,"address":address,"email":email,"dob":dob,"number":number,"quote":quote,"typ":typ,"name":name1})
	

def user_profile_edit(request):
	userauth(request)
	try:
		print(request.POST)
		qq=User.objects.get(username=request.user.username)
		empid=qq.id
		tbl_profile.objects.get_or_create(emp_id=empid)

		if(request.POST.get("btn_update")!=None):
			fnam=request.POST["ufnam"]
			lnam=request.POST["ulnam"]
			address=request.POST["uaddres"]
			email=request.POST["uemail"]
			dob=request.POST["udob"]
			number=request.POST["unumber"]
			quote=request.POST["uquote"]
			typ=request.POST.getlist("type",None)

			q=tbl_profile.objects.get(emp_id=empid)
			q.emp_dob=dob
			q.emp_email=email
			q.emp_phone=int(number)
			print(number)
			q.emp_address=address
			q.emp_type=typ[0]
			q.emp_discriptin=quote
			q.emp_last_edit=datetime.today().strftime("%Y-%m-%d")

			q.save()

			if(fnam!="" and lnam!=""):
				qq.first_name=fnam
				qq.last_name=lnam
				print(fnam,lnam)
				qq.save()

			if(request.FILES.get('img')):
				upimage=Proj_img(request.FILES["img"])
				print("inside upload image",upimage," request.files :",request.FILES["img"])
				print("  ..........",request.FILES)

				print("\n upimage :",upimage)
				if upimage.is_valid(): 
					print("inside image validation")
					upimage.save() 
					# return redirect('success') 
				else: 
					print("else in image validation")
					upimage = Proj_img() 
    			# return render(request, 'hotel_image_form.html', {'upimage' : upimage})


				# image=request.FILES["img"]
				# # fs=FileSystemStorage()
				# # uploaded_file_url = fs.url(filename)
				# print("image upload demo :",image)
				# # print(" i think path :",fs)
				# q.emp_img=image
				# q.save()

		q1=tbl_profile.objects.get(emp_id=empid)
		fnam=qq.first_name
		lnam=qq.last_name
		name1=fnam+" "+lnam
		address=q1.emp_address
		email=q1.emp_email
		dob=q1.emp_dob
		number=q1.emp_phone
		quote=q1.emp_discriptin
		typ=q1.emp_type
		print(fnam,lnam,address,email,dob,number,quote,typ,name1)

	except Exception as e:
		print("error :::::::",e)
		return render(request,"Edit_profile.html")

	return render(request,"Edit_profile.html",{"fnam":fnam,"lnam":lnam,"address":address,"email":email,"dob":dob,"number":number,"quote":quote,"typ":typ,"name":name1})
	
def applay_leave(request):
	userauth(request)
	lastleave,pending="",""
	print(request.POST)
	qq=User.objects.get(username=request.user.username)
	empid=qq.id
	fnam=qq.first_name
	lnam=qq.last_name
	name1=fnam+" "+lnam

	if(request.POST!={}):
		l_typ=request.POST.getlist("levae_type",None)
		l_from=datetime.strptime(request.POST["from_date"],'%Y-%m-%d').date()
		l_to=datetime.strptime(request.POST["to_date"],'%Y-%m-%d').date()
		l_reason=request.POST["reason"]
		status="Pending"
		emp_name=request.session["user_username"]
		l_year=datetime.today().year

		if(l_typ[0]=="Sick Leave"):
			status="Approved"

		end_date=date(l_to.year,l_to.month,l_to.day)
		start_date=date(l_from.year,l_from.month,l_from.day)
		wekday=np.busday_count(start_date,end_date)+1
		j=(end_date-start_date).days+1
		if(l_typ[0] in ['Sick Leave','Maternity Leave','Marriage Leave']):
			j=wekday

		q1=tbl_leave.objects.create(emp_id=empid,emp_name=emp_name,l_type=l_typ[0],l_reason=l_reason,l_days=int(j),l_status=status,l_year=l_year,l_from=l_from,l_to=l_to)
		q1.save()

	q=tbl_leave.objects.filter(emp_id=empid).order_by("-id")[:5]
	s1=tbl_leave.objects.filter(emp_id=empid,l_status="Pending").order_by("-id")
	s2=tbl_leave.objects.filter(emp_id=empid,l_status="Approved").order_by("-id")[:1]
	for i in s2:
		print(i.l_days,i.id)
		lastleave=i.l_type+": From "+str(i.l_from)+" To "+str(i.l_to)+"<br>&nbsp&nbsp "+i.l_reason+" For "+str(i.l_days)+" Days"
	for i in s1:
		print(i.l_days,i.id)
		pending=pending+i.l_type+": From "+str(i.l_from)+" To "+str(i.l_to)+"<br>&nbsp&nbsp "+i.l_reason+"<br> For "+str(i.l_days)+" Days<hr>"

	return render(request,"applay_leave.html",{"q":q,"lastleave":lastleave,"pending":pending,"name":name1})

def msg(request):
	print(request.POST)
	dic={}
	ans=""
	t_days=""
	qq=User.objects.get(username=request.user.username)
	empid=qq.id

	l_typ=request.POST.getlist("levae_type",None)
	l_from=datetime.strptime(request.POST["from_date"],'%Y-%m-%d').date()
	l_to=datetime.strptime(request.POST["to_date"],'%Y-%m-%d').date()
	l_reason=request.POST["reason"]

	end_date=date(l_to.year,l_to.month,l_to.day)
	start_date=date(l_from.year,l_from.month,l_from.day)
	wekday=np.busday_count(start_date,end_date)+1
	j=(end_date-start_date).days+1
	q=tbl_leave.objects.filter(emp_id=empid,l_type=l_typ[0],l_year=datetime.today().year).aggregate(Sum("l_days"))
	if(q["l_days__sum"]!=None and l_typ[0] in ['Sick Leave','Maternity Leave','Marriage Leave']):
		t_days=int(wekday)+int(q["l_days__sum"])
		j=str(wekday)
	elif(q["l_days__sum"]!=None):
		t_days=int(q["l_days__sum"])+int(j)
	else:
		if(l_typ[0] in ['Sick Leave','Maternity Leave','Marriage Leave']):
			j=str(wekday)
			t_days=int(wekday)
		else:
			t_days=int(j)

	if(l_from<datetime.today().date() or t_days<1):
		ans="You Can't Apply Leave for These Days Please Check your Leave Start and End Dates"
		dic["status"]=False
	elif(t_days>12 and l_typ[0] in ['Sick Leave','Privilege/Annual Leave']):
		ans="Sorry We can't Allow The Leave\nBecause You Have Exceeded the Limit\nYour total Leave Including this is :"+str(t_days)+"\nYou are only allowed to take Max 12 Leaves in a calender year"
		dic["status"]=False
	elif(t_days>5 and l_typ[0]=="Marriage Leave"):
		ans="Sorry We can't Allow The Leave\nBecause You Have Exceeded the Limit\nYour total Leave Including this is :"+str(t_days)+"\nYou are only allowed to take Max 5 Leaves in a calender year"
		dic["status"]=False
	elif(t_days>30 and l_typ[0]=="Maternity Leave"):
		ans="Sorry We can't Allow The Leave\nBecause You Have Exceeded the Limit\nYour total Leave Including this is :"+str(t_days)+"\nYou are only allowed to take Max 30 Leaves in a calender year"
		dic["status"]=False
	else:
		ans="You are Applying for "+str(j)+" days Leave from "+str(datetime.strftime(l_from,'%d-%m-%Y'))+" to "+str(datetime.strftime(l_to,'%d-%m-%Y'))+"<br><hr>Reason :"+l_reason+"<hr>Is That Correct ?"
		dic["status"]=True
	dic["ans"]=ans
	print(dic)
	jsondata=json.dumps(dic)
	return HttpResponse(jsondata,content_type="application/json")

def leave_history(request):
	userauth(request)

	print(request.POST)
	qq=User.objects.get(username=request.user.username)
	empid=qq.id
	fnam=qq.first_name
	lnam=qq.last_name
	name1=fnam+" "+lnam

	q=tbl_leave.objects.filter(emp_id=empid,l_status="Approved").order_by("-id")
	q1=tbl_leave.objects.filter(emp_id=empid,l_status="Pending").order_by("-id")
	q2=tbl_leave.objects.filter(emp_id=empid,l_status="Rejected").order_by("-id")

	if(request.POST.get("btn_delete")!=None):
		q3=tbl_leave.objects.get(id=request.POST["btn_delete"])
		q3.delete()

	return render(request,"leave_history.html",{"name":name1,"approved":q,"pending":q1,"rejected":q2})