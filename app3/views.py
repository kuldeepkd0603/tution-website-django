from django.shortcuts import render,redirect
#for call models
from . import models

#for file uploading ......................
from django.core.files.storage import FileSystemStorage

#for display image
from django.conf import settings
media_url=settings.MEDIA_URL

#for date
import datetime

#for logout
from django.contrib.auth import logout

def home(request):
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
     fnm=request.POST.get("fnm")
     mno=request.POST.get("mno")
     emailid=request.POST.get("emailid")
     pwd=request.POST.get("pwd")
     role="student"
     obj=models.mstuser(fnm=fnm,mno=mno,emailid=emailid,pwd=pwd,role=role)
     obj.save() #save like insert query
     return render(request,"register.html")
    else:
     return render(request,"register.html") 

def userlist(request):
    #for fetch all record from mstuser table
    res=models.mstuser.objects.filter(role="student")   
    return render(request,"userlist.html",{'res':res}) 

def login(request):
   if request.method=="POST":
    emailid=request.POST.get("emailid")
    pwd=request.POST.get("pwd")
    res=models.mstuser.objects.filter(emailid=emailid,pwd=pwd)
    if len(res)>0:
     role=res[0].role
     #for create session .....................
     request.session["emailid"]=emailid
     request.session["role"]=role 
     #.........................................
     print(role)
     if role=="admin":
       #print("welcome admin")
       return redirect("/adminhome/")
     else:
       return redirect("/studenthome/") 
    return render(request,"login.html")    
   else:
    return render(request,"login.html")  

def adminhome(request):
    return render(request,"adminhome.html")   
   
def addcourse(request):
    if request.method=="POST":
        nm=request.POST.get("nm")
        duration=request.POST.get("duration")
        fees=request.POST.get("fees")
        #for file uploading .................................
        courseicon=request.FILES["courseicon"]
        fs=FileSystemStorage()
        courseimg=fs.save(courseicon.name,courseicon)  
        #....................................................  
        obj=models.course(nm=nm,duration=duration,
        fees=fees,courseicon=courseicon)
        obj.save()
        return render(request,"addcourse.html")
    else:
        return render(request,"addcourse.html")

def courselist1(request):
    #for fetch all record from course table
    res=models.course.objects.all()    
    return render(request,"courselist1.html",
    {'res':res,'media_url':media_url}) 

def addbatch(request):
    if request.method=="POST":
        nm=request.POST.get("nm")
        startdate=request.POST.get("startdate")
        batchtime=request.POST.get("batchtime")
        facultyname=request.POST.get("facultyname")
        obj=models.batch(nm=nm,startdate=startdate,
        batchtime=batchtime,facultyname=facultyname)
        obj.save()
        return render(request,"addbatch.html")
    else:
        return render(request,"addbatch.html")

def studenthome(request):
    return render(request,"studenthome.html")    

def batchlist1(request):
    #for fetch all record from batch table
    res=models.batch.objects.all()    
    return render(request,"batchlist1.html",
                  {'res':res}) 
def batchlist2(request):
    #for fetch all record from batch table
    res=models.batch.objects.all()    
    return render(request,"batchlist2.html",
                  {'res':res}) 

def courselist2(request):
    #for fetch all record from course table
    res=models.course.objects.all()    
    return render(request,"courselist2.html",
    {'res':res,'media_url':media_url}) 

def admission(request):
    if request.method=="GET":
     batchid=request.GET.get("batchid")   
     print("batch id",batchid)
     res=models.batch.objects.filter(batchid=batchid)
     print(type(res))
     return render(request,"admission.html",{'res':res})
    else:
      batchid=request.POST.get("batchid")   
      nm=request.POST.get("nm")
      x=datetime.datetime.now()
      dt1=x.strftime("%Y-%m-%d")
      #fetch data from session
      emailid=request.session["emailid"] 
      #for store data in admission table .............
      obj=models.addmision(nm=nm,dt1=dt1,
                           emailid=emailid)  
      obj.save()
      #...............................................
      return redirect("/batchlist1/")

def logout1(request):
   logout(request)
   return redirect("http://localhost:8000/")
       