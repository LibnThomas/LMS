from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
import json
from .models import tbl_leave,tbl_profile
# from .forms import *
import numpy as np
import os
import datetime
from datetime import date,datetime
from django.utils.timezone import now

def userauth(request):
	print(request.POST)
	st=True
	if (request.user.is_authenticated):
		loguser=request.user.first_name+" "+request.user.last_name
		print("User :"+request.user.first_name+" "+request.user.last_name)
	else:
		st=False
		
	if(request.POST.get("logout")!=None):
		request.session.flush()
		logout(request)
		st=False
	return st

def login1(request):
	try:
		name=""
		print("Session values in username common :",request.session.get("user_username"))
		if(request.POST.get("login")!=None):
			user=authenticate(username=request.POST["unam"],password=request.POST["pass"])
			if(user!=None):
				q=User.objects.get(username=request.POST['unam'])
				name=q.first_name+" "+q.last_name
				q2=tbl_profile.objects.get(emp_id=q.id)
				if(q2.emp_auth=="Manager"):
					if(q2.status=="Approved"):
						# if(request.session.get("user_username")!=None):
						# 	return render(request,"home.html",{"msg":"One Session is already Running"})
						# else:
						request.session['user_username']=name
					else:
						return render(request,"home.html",{"msg":"Your Request is "+q2.status})

					login(request,user)
					return redirect("admin_home")
				elif(q2.emp_auth=="Staff"):
					if(q2.status=="Approved"):
						# if(request.session.get("user_username")!=None):
						# 	return render(request,"home.html",{"msg":"One Session is already Running"})
						# else:
						request.session['user_username']=name
					else:
						return render(request,"home.html",{"msg":"Your Request is "+q2.status})
					login(request,user)
					return redirect("user_home")
				elif(User.is_superuser):
					# if(request.session.get("user_username")!=None):
					# 	return render(request,"home.html",{"msg":"One Session is already Running"})
					# else:
					request.session['user_username']=name
					login(request,user)
					return redirect("Main_Admin")

			else:
				return render(request,"home.html",{"msg":"Incorrect User Name/Password"})

		if(request.POST.get("btn_signin")!=None):
			try:
				a=User.objects.get(username=request.POST["uname"])
				return render(request,"home.html",{"msg":"User Name Exists"})
			except:
				if(request.POST["pass"]==request.POST["conf_pass"]):
					typ=request.POST.getlist("stafftype",None)[0]
					q=User.objects.create_user(username=request.POST["uname"],password=request.POST["pass"],first_name=request.POST["fname"],last_name=request.POST["lname"])
					q.save()
					qq=User.objects.get(username=request.POST["uname"])
					q1=tbl_profile.objects.create(emp_id=qq.id,emp_auth=request.POST.getlist("stafftype",None)[0],status="Pending")
					q1.save()
				else:
					return render(request,"home.html",{"msg":"Password Doesn't Match"})

		return render(request,'home.html')
	except Exception as e:
		print("error : ",e)
		return render(request,'home.html')

# @login_required # djagno decorator for check user authentication
def p_admin(request):
	if(userauth(request)):
		if(request.POST.get("btn_approve")):
			q1=tbl_profile.objects.get(id=request.POST["btn_approve"])
			q1.status="Approved"
			q1.save()
		if(request.POST.get("btn_reject")):
			q1=tbl_profile.objects.get(id=request.POST["btn_reject"])
			q1.status="Rejected"
			q1.save()

		q=tbl_profile.objects.filter(status="Pending").order_by("-id")
		ans=""
		for i in q:
			q1=User.objects.get(id=i.emp_id)
			ans=ans+"<tr style='border-radius: 10px;'><td>"+q1.first_name+q1.last_name+"</td><td>"+q1.username+"</td><td>"+i.emp_auth+"</td><td>"+str(q1.date_joined)+"</td><td><button class='form-control btn-success' name='btn_approve' value='"+str(i.id)+"'>Approve</button></td><td><button class='form-control btn-danger' name='btn_reject' value='"+str(i.id)+"'>Reject</button></td></tr>"

		return render(request,'Main_Admin.html',{"ans":ans})
	else:
		return redirect('login1')

def admin_home(request):
	if(userauth(request)):
		try:
			q=tbl_leave.objects.filter(l_status="Approved").order_by("-id")
			q1=tbl_leave.objects.filter(l_status="Pending").order_by("-id")
			q2=tbl_leave.objects.filter(l_status="Rejected").order_by("-id")
			q3=User.objects.filter(is_superuser=0)


			if(request.POST.get("btn_profile")!=None):
				ans=admin_user_profile(request)
				employeeList=employee_view()
				return render(request,"admin_home.html",{"id":request.POST['btn_profile'],"approved":q,"pending":q1,"rejected":q2,"employes":employeeList,"ans":ans,"pag":"active in","display":"block;"})

			if(request.POST.get("btn_user_approve")!=None):
				q4=tbl_profile.objects.get(emp_id=request.POST["btn_user_approve"])
				q4.status="Approved"
				q4.save()
				employeeList=employee_view()
				return render(request,"admin_home.html",{"approved":q,"pending":q1,"rejected":q2,"employes":employeeList,"pag":"active in"})

			if(request.POST.get("btn_user_reject")!=None):
				q4=tbl_profile.objects.get(emp_id=request.POST["btn_user_reject"])
				q4.status="Rejected"
				q4.save()
				employeeList=employee_view()
				return render(request,"admin_home.html",{"approved":q,"pending":q1,"rejected":q2,"employes":employeeList,"pag":"active in"})

			if(request.POST.get("btn_approve")!=None):
				q4=tbl_leave.objects.get(id=request.POST["btn_approve"])
				q4.l_status="Approved"
				q4.save()

			if(request.POST.get("btn_reject")!=None):
				q4=tbl_leave.objects.get(id=request.POST["btn_reject"])
				q4.l_status="Rejected"
				q4.l_r_reason=request.POST["reject_reason"]
				q4.save()


		except Exception as e:
			print("Error ::::",e)
			return render(request,"admin_home.html")
		employeeList=employee_view()
		return render(request,"admin_home.html",{"approved":q,"pending":q1,"rejected":q2,"employes":employeeList,"pag1":"active in"})
	else:
		return redirect('login1')
		
def employee_view():

	q4=tbl_profile.objects.filter(emp_auth="Staff")
	employeeList = []
	for i in q4:
		emp=i.emp_id
		q5=User.objects.get(id=emp)
		empDct = {}
		empDct['first_name'] = q5.first_name
		empDct['last_name'] = q5.last_name
		empDct['last_login'] = q5.last_login
		empDct['emp_id'] = i.emp_id
		empDct['username'] = q5.username
		empDct['status'] = i.status
		employeeList.append(empDct)
	return employeeList
def admin_user_profile(request):
	# print("hello")
	if(request.POST.get('btn_profile')!=None):
		q1=tbl_profile.objects.filter(emp_id=request.POST['btn_profile'])
		q=User.objects.filter(id=request.POST['btn_profile'])
		for i in q:
			name=i.first_name+" "+i.last_name

		for i in q1:
			# print("1st")
			ans="<div class='row'><div class='row'><div class='col-md-12' style='text-align: center;align-content: center;'><img src='/media/"+str(i.emp_img)+"' style='height: 100px;width: 100px;border-radius: 50%;object-fit: cover;background: linear-gradient(to top left, #ffffff -21%, #00BCD4  123%);'><br><label style='text-shadow: 1px 1px 1px black;font-weight: bolder;font-size: 20px;'>"+name+"</label></div></div></div><hr><div class='row'><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Address</div><div class='col-md-9'><label>: "+i.emp_address+"</label></div></div><div class='row'><div class='col-md-3'>DOB</div><div class='col-md-9'><label>: "+str(i.emp_dob)+"</label></div></div><div class='row'><div class='col-md-3'>Email</div><div class='col-md-9'><label>: "+i.emp_email+"</label></div></div><div class='row'><div class='col-md-3'>Phone</div><div class='col-md-9'><label>: "+str(i.emp_phone)+"</label></div></div></div><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Type</div><div class='col-md-9'><label>: "+i.emp_type+"</label></div></div><div class='row'><div class='col-md-3'>Quote</div><div class='col-md-9'><label>: "+i.emp_discriptin+"</label></div></div></div></div>"

	# elif(request.POST.get('btn_view')!=None):
	# 	q=User.objects.filter(id=request.POST['btn_view'])
	# 	q1=tbl_profile.objects.filter(emp_id=request.POST['btn_view'])
	# 	for i in q:
	# 		name=i.first_name+" "+i.last_name

	# 	for i in q1:
	# 		print("2nd")
	# 		ans="<div class='row'><div class='row'><div class='col-md-12' style='text-align: center;align-content: center;'><img src='/media/"+str(i.emp_img)+"' style='height: 100px;width: 100px;border-radius: 50%;object-fit: cover;background: linear-gradient(to top left, #ffffff -21%, #00BCD4  123%);'><br><label style='text-shadow: 1px 1px 1px black;font-weight: bolder;font-size: 20px;'>"+name+"</label></div></div></div><hr><div class='row'><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Address</div><div class='col-md-9'><label>: "+i.emp_address+"</label></div></div><div class='row'><div class='col-md-3'>DOB</div><div class='col-md-9'><label>: "+str(i.emp_dob)+"</label></div></div><div class='row'><div class='col-md-3'>Email</div><div class='col-md-9'><label>: "+i.emp_email+"</label></div></div><div class='row'><div class='col-md-3'>Phone</div><div class='col-md-9'><label>: "+str(i.emp_phone)+"</label></div></div></div><div class='col-md-6' style='padding-left: 50px;padding-top: 20px;font-weight: bold;text-align: left;'><div class='row'><div class='col-md-3'>Type</div><div class='col-md-9'><label>: "+i.emp_type+"</label></div></div><div class='row'><div class='col-md-3'>Quote</div><div class='col-md-9'><label>: "+i.emp_discriptin+"</label></div></div></div></div>"
	# print("hello1")
	# print(ans)
	return ans


def user_home(request):
	if(userauth(request)):

		q=tbl_leave.objects.filter(l_status="Approved",emp_id=request.user.id).order_by("-id")
		q1=tbl_leave.objects.filter(l_status="Pending",emp_id=request.user.id).order_by("-id")
		q2=tbl_leave.objects.filter(l_status="Rejected",emp_id=request.user.id).order_by("-id")
		q3=tbl_leave.objects.filter(l_status="Approved",emp_id=request.user.id).aggregate(Sum("l_days"))
		q4=tbl_leave.objects.filter(l_status="Rejected",emp_id=request.user.id).aggregate(Sum("l_days"))
		q5=tbl_profile.objects.get(emp_id=request.user.id)

		return render(request,"Usr_Home.html",{"u_img":q5.emp_img,"name":request.user.first_name+" "+request.user.last_name,"pending":q1,"accepted":q,"reject":q2,"l_acc":q3["l_days__sum"],"l_rej":q4["l_days__sum"]})
	else:
		return redirect('login1')

def userprofile(request):
	if(userauth(request)):
		try:
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

		except Exception as e:
			print("Error ::::",e)
			return render(request,"Usr_profile.html")

		return render(request,"Usr_profile.html",{"u_img":q1.emp_img,"fnam":fnam,"lnam":lnam,"address":address,"email":email,"dob":dob,"number":number,"quote":quote,"typ":typ,"name":name1})
	else:
		return redirect('login1')
	

def user_profile_edit(request):
	if(userauth(request)):
		try:
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
				q.emp_phone=number
				q.emp_address=address
				q.emp_type=typ[0]
				q.emp_discriptin=quote
				q.emp_last_edit=datetime.today().strftime("%Y-%m-%d")


				if(fnam!="" and lnam!=""):
					qq.first_name=fnam
					qq.last_name=lnam
					qq.save()

				if(request.FILES.get('img')):
					imgpath=str(q.emp_img).split("/")[-1]
					path_img="\\media\\img\\"+imgpath
					abs_path= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
					abs_path=abs_path+path_img
					if(os.path.exists(abs_path) and imgpath!=""):
						os.remove(abs_path)
					q.emp_img=request.FILES["img"]
					q.save()
				else:
					q.save()


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
			u_img=q1.emp_img

		except Exception as e:
			print("error :::::::",e)
			return render(request,"Edit_profile.html")

		return render(request,"Edit_profile.html",{"u_img":u_img,"fnam":fnam,"lnam":lnam,"address":address,"email":email,"dob":dob,"number":number,"quote":quote,"typ":typ,"name":name1})
	else:
		return redirect('login1')
	
def applay_leave(request):
	if(userauth(request)):
		lastleave,pending="",""
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


			end_date=date(l_to.year,l_to.month,l_to.day)
			start_date=date(l_from.year,l_from.month,l_from.day)
			ll=tbl_leave.objects.filter(emp_id=empid,l_type=l_typ[0],l_year=datetime.today().year).aggregate(Sum("l_days"))
			wekday=np.busday_count(start_date,end_date)+1
			j=(end_date-start_date).days+1
			leave_days_t=int(ll["l_days__sum"])+int(j)

			if(j>12 and l_typ[0] in ['Sick Leave']):
				status="Pending"
			elif(l_typ[0]=="Sick Leave"):
				status="Approved"

			if(l_typ[0] in ['Sick Leave','Maternity Leave','Marriage Leave']):
				j=wekday

			q1=tbl_leave.objects.create(emp_id=empid,emp_name=emp_name,l_type=l_typ[0],l_reason=l_reason,l_days=int(j),l_status=status,l_year=l_year,l_from=l_from,l_to=l_to)
			q1.save()

		q=tbl_leave.objects.filter(emp_id=empid).order_by("-id")[:5]
		s1=tbl_leave.objects.filter(emp_id=empid,l_status="Pending").order_by("-id")
		s2=tbl_leave.objects.filter(emp_id=empid,l_status="Approved").order_by("-id")[:1]
		for i in s2:
			lastleave=i.l_type+": From "+str(i.l_from)+" To "+str(i.l_to)+"<br>&nbsp&nbsp "+i.l_reason+" For "+str(i.l_days)+" Days"
		for i in s1:
			pending=pending+i.l_type+": From "+str(i.l_from)+" To "+str(i.l_to)+"<br>&nbsp&nbsp "+i.l_reason+"<br> For "+str(i.l_days)+" Days<hr>"

		s3=tbl_profile.objects.get(emp_id=empid)
		return render(request,"applay_leave.html",{"u_img":s3.emp_img,"q":q,"lastleave":lastleave,"pending":pending,"name":name1})
	else:
		return redirect('login1')

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
	elif(t_days>12 and l_typ[0] in ['Sick Leave']):
		ans="You Have Exceeded the Limit, If you are Extremely sick, We can forward the leave to Manager Approval<br><br>You are Applying for "+str(j)+" days Leave from "+str(datetime.strftime(l_from,'%d-%m-%Y'))+" to "+str(datetime.strftime(l_to,'%d-%m-%Y'))+"<br>Reason :"+l_reason+" <hr> Do You want To Forward this Leave to Manager?"
		dic["status"]=True
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
	jsondata=json.dumps(dic)
	return HttpResponse(jsondata,content_type="application/json")

def leave_history(request):
	if(userauth(request)):

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

		q3=tbl_profile.objects.get(emp_id=empid)
		return render(request,"leave_history.html",{"u_img":q3.emp_img,"name":name1,"approved":q,"pending":q1,"rejected":q2})
	else:
		return redirect('login1')