import base64
import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import *


def login(request):
    return render(request,"login.html")
def loginpost(request):
    username=request.POST['text']
    password=request.POST['password']

    lobj=Login.objects.filter(username=username,password=password)
    if lobj.exists():

        request.session['lid']=lobj[0].id
        if lobj[0].type=="admin":
            return redirect('/myapp/admin_home/')
        elif lobj[0].type == "doctor":
            return redirect('/myapp/doctor_home/')
        elif lobj[0].type=="therapist":
            return redirect('/myapp/therapist_home/')
        elif lobj[0].type=="staff":
            return redirect('/myapp/staff_home/')
        else:

            return HttpResponse("<script>alert('Invalid username and password');window.location='/myapp/login/'</script>")

    else:
        return HttpResponse("<script>alert('Invalid username and password');window.location='/myapp/login/'</script>")
def logout(request):
    request.session['lid']=''
    return HttpResponse("<script>alert('Logouted successfully');window.location='/myapp/login/'</script>")


##############admin
def admin_home(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:

        return render(request,"admin/adminhomeindex.html")
def admin_doctoradd(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"admin/doctoradd.html")

def admin_adddoctor_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        Name=request.POST['name']
        DOB=request.POST['textfield2']
        Gender=request.POST['RadioGroup1']
        Place=request.POST['place']
        Post=request.POST['post']
        Pin=request.POST['pin']
        Department=request.POST['dpt']
        Email=request.POST['email']
        Photo=request.FILES['photo']
        fs = FileSystemStorage()
        from datetime import datetime
        s = "doctor/" + datetime.now().strftime("%Y%m%d%H%M%S") + Photo.name
        fn = fs.save(s, Photo)

        Qualification=request.POST['textfield3']
        Phone=request.POST['phone']



        lobj=Login()
        lobj.username=Email
        lobj.password=Phone
        lobj.type='doctor'
        lobj.save()

        sobj=Doctor()
        sobj.dname=Name
        sobj.gender=Gender
        sobj.dob=DOB
        sobj.place=Place
        sobj.post=Post
        sobj.pin=Pin
        sobj.department=Department
        sobj.email=Email
        sobj.photo=fs.url(s)
        sobj.phno=Phone
        sobj.qualification=Qualification
        sobj.LOGIN=lobj
        sobj.save()
        return HttpResponse('''<script>alert("successfully registered");window.location='/myapp/admin_doctoradd/'</script>''')






def admin_viewdoctors(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj= Doctor.objects.all()


        return render(request,"admin/viewdoctors.html",{'data':dobj})

def admin_viewdoctorspost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name=request.POST['search']
        dobj = Doctor.objects.filter(dname__icontains=name)

        return render(request, "admin/viewdoctors.html", {'data': dobj})
def admin_doctoredit(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj= Doctor.objects.get(id=id)

        return render(request,"admin/doctoredit.html" ,{'data': dobj})

def admin_editdoctor_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        id = request.POST['id']
        Name = request.POST['name']
        DOB = request.POST['textfield2']
        Gender = request.POST['RadioGroup1']
        Place = request.POST['place']
        Post = request.POST['post']
        Pin = request.POST['pin']
        Department = request.POST['dpt']
        Email = request.POST['email']
        Qualification = request.POST['textfield3']
        Phone = request.POST['phone']

        if 'photo' in request.FILES:
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            from datetime import datetime
            s = "doctor/" + datetime.now().strftime("%Y%m%d%H%M%S") + Photo.name
            fn = fs.save(s, Photo)
            sobj = Doctor.objects.get(id=id)

            sobj.photo = fs.url(s)
            sobj.save()




            sobj = Doctor.objects.get(id=id)
            sobj.dname = Name
            sobj.gender = Gender
            sobj.dob = DOB
            sobj.place = Place
            sobj.post = Post
            sobj.pin = Pin
            sobj.department = Department
            sobj.email = Email
            sobj.phno = Phone
            sobj.qualification = Qualification
            sobj.save()
            return HttpResponse('''<script>alert("Updated successfully");window.location='/myapp/admin_viewdoctors/'</script>''')
def admin_delete_Doctor(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph =Doctor.objects.get(id=id)
        ph.delete()
        return HttpResponse(
            '''<script>alert("Deleted  successfully");window.location='/myapp/admin_viewdoctors/'</script>''')


def admin_viewcomplaint(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        r=Complaint.objects.all()

        return render(request,"admin/viewcomplaint.html",{'data':r})
def admin_viewcomplaintpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Complaint.objects.filter(date__range=[fromdate,todate])

        return render(request, "admin/viewcomplaint.html", {'data': r})

def admin_sendreply(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"admin/sendreply.html",{'id':id})

def admin_sendreplypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        reply=request.POST['textarea']
        id=request.POST['id']

        c=Complaint.objects.get(id=id)
        c.reply=reply
        c.status="Replied"
        c.save()

        return HttpResponse("<Script>alert('Replied successfully');window.location='/myapp/admin_viewcomplaint/'</script>")

def admin_add_staff(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"admin/staffadd.html")

def admin_add_staff_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        Name = request.POST['name']
        DOB = request.POST['textfield2']
        Gender = request.POST['RadioGroup1']
        Place = request.POST['place']
        Post = request.POST['post']
        Pin = request.POST['pin']
        Department = request.POST['dpt']
        Email = request.POST['email']
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        from datetime import datetime
        s = "staff/" + datetime.now().strftime("%Y%m%d%H%M%S") + Photo.name
        fn = fs.save(s, Photo)

        Qualification = request.POST['textfield3']
        Phone = request.POST['phone']

        lobj = Login()
        lobj.username = Email
        lobj.password = Phone
        lobj.type = 'staff'
        lobj.save()

        sobj = Staff()
        sobj.sname = Name
        sobj.gender = Gender
        sobj.dob = DOB
        sobj.place = Place
        sobj.post = Post
        sobj.pin = Pin
        sobj.department = Department
        sobj.email = Email
        sobj.photo = fs.url(s)
        sobj.phno = Phone
        sobj.qualification = Qualification
        sobj.LOGIN = lobj
        sobj.save()
        return HttpResponse(
            '''<script>alert("successfully registered");window.location='/myapp/admin_add_staff/'</script>''')


def admin_viewstaff(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj= Staff.objects.all()


        return render(request,"admin/viewstaff.html",{'data':dobj})

def admin_viewstaffpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name=request.POST['search']
        dobj = Staff.objects.filter(sname__icontains=name)

        return render(request,"admin/viewstaff.html",{'data':dobj})
def admin_staffedit(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj= Staff.objects.get(id=id)

        return render(request,"admin/staffedit.html",{'data':dobj})

def admin_editstaff_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        Name = request.POST['name']
        DOB = request.POST['textfield2']
        Gender = request.POST['RadioGroup1']
        Place = request.POST['place']
        Post = request.POST['post']
        Pin = request.POST['pin']
        Department = request.POST['dpt']
        Email = request.POST['email']
        id = request.POST['id']


        Qualification = request.POST['textfield3']
        Phone = request.POST['phone']

        if 'photo' in request.FILES:
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            from datetime import datetime
            s = "staff/" + datetime.now().strftime("%Y%m%d%H%M%S") + Photo.name
            fn = fs.save(s, Photo)
            sobj = Staff.objects.get(id=id)
            sobj.photo = fs.url(s)
            sobj.save()

        sobj=Staff.objects.get(id=id)

        sobj.sname = Name
        sobj.gender = Gender
        sobj.dob = DOB
        sobj.place = Place
        sobj.post = Post
        sobj.pin = Pin
        sobj.department = Department
        sobj.email = Email
        sobj.phno = Phone
        sobj.qualification = Qualification
        sobj.save()
        return HttpResponse(
            '''<script>alert("successfully Updated");window.location='/myapp/admin_viewstaff/'</script>''')


def admin_delete_staff(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
            ph =Staff.objects.get(id=id)
            ph.delete()
            return HttpResponse(
                '''<script>alert("Deleted  successfully");window.location='/myapp/admin_viewstaff/'</script>''')

def admin_add_therapist(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"admin/therapistadd.html")

def admin_add_therapist_post(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        Name = request.POST['name']
        DOB = request.POST['textfield2']
        Gender = request.POST['RadioGroup1']
        Place = request.POST['place']
        Post = request.POST['post']
        Pin = request.POST['pin']
        Department = request.POST['dpt']
        Email = request.POST['email']
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        from datetime import datetime
        s = "therapist/" + datetime.now().strftime("%Y%m%d%H%M%S") + Photo.name
        fn = fs.save(s, Photo)

        Qualification = request.POST['textfield3']
        Phone = request.POST['phone']

        lobj = Login()
        lobj.username = Email
        lobj.password = Phone
        lobj.type = 'therapist'
        lobj.save()

        sobj = Therapist()
        sobj.tname = Name
        sobj.gender = Gender
        sobj.dob = DOB
        sobj.place = Place
        sobj.post = Post
        sobj.pin = Pin
        sobj.department = Department
        sobj.email = Email
        sobj.photo = fs.url(s)
        sobj.phno = Phone
        sobj.qualification = Qualification
        sobj.LOGIN = lobj
        sobj.save()
        return HttpResponse(
            '''<script>alert("successfully registered");window.location='/myapp/admin_add_therapist/'</script>''')


def admin_viewtherapist(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj= Therapist.objects.all()


        return render(request,"admin/viewtherapist.html",{'data':dobj})

def admin_viewtherapistpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name=request.POST['search']
        dobj = Therapist.objects.filter(sname__icontains=name)

        return render(request,"admin/viewtherapist.html",{'data':dobj})
def admin_therapistedit(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj= Therapist.objects.get(id=id)

        return render(request,"admin/therapistedit.html",{'data':dobj})

def admin_edittherapist_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        Name = request.POST['name']
        DOB = request.POST['textfield2']
        Gender = request.POST['RadioGroup1']
        Place = request.POST['place']
        Post = request.POST['post']
        Pin = request.POST['pin']
        Department = request.POST['dpt']
        Email = request.POST['email']
        id = request.POST['id']


        Qualification = request.POST['textfield3']
        Phone = request.POST['phone']

        if 'photo' in request.FILES:
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            from datetime import datetime
            s = "therapist/" + datetime.now().strftime("%Y%m%d%H%M%S") + Photo.name
            fn = fs.save(s, Photo)
            sobj = Therapist.objects.get(id=id)
            sobj.photo = fs.url(s)
            sobj.save()

        sobj=Therapist.objects.get(id=id)

        sobj.tname = Name
        sobj.gender = Gender
        sobj.dob = DOB
        sobj.place = Place
        sobj.post = Post
        sobj.pin = Pin
        sobj.department = Department
        sobj.email = Email
        sobj.phno = Phone
        sobj.qualification = Qualification
        sobj.save()
        return HttpResponse(
            '''<script>alert("successfully Updated");window.location='/myapp/admin_viewtherapist/'</script>''')


def admin_delete_therapist(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph =Therapist.objects.get(id=id)
        ph.delete()
        return HttpResponse(

            '''<script>alert("Deleted  successfully");window.location='/myapp/admin_viewtherapist/'</script>''')


def admin_Addsalary(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:

        return render(request,"admin/Addsalary.html",{'id':id})
def admin_Addsalarypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        year=request.POST['textfield']
        month=request.POST['textfield2']
        date=request.POST['textfield3']
        amount=request.POST['textfield4']
        id=request.POST['id']


        s=Salary()
        s.LOGIN_id=id
        s.Year=year
        s.month=month
        s.date=date
        s.Amount=amount
        s.save()
        return HttpResponse('''<script>alert("successfully added");window.location='/myapp/admin_home/'</script>''')


def adminviewsalary(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Salary.objects.filter(LOGIN_id=id)
        return render(request,"admin/viewsalary.html",{'data':dr,'id':id})



def adminviewsalarypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate = request.POST['from']
        todate = request.POST['to']
        id = request.POST['id']
        ds = Salary.objects.filter(date__range=[fromdate, todate],DOCTOR__LOGIN_id=request.session['lid'])
        return render(request,"admin/viewsalary.html",{'data':ds,'id':id})



def admindelete_salary(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph =Salary.objects.get(id=id)
        ph.delete()
        return HttpResponse(
            '''<script>alert("Deleted  successfully");window.location='/myapp/admin_home/'</script>''')

# def doctor_editschedule(request,id):
#     doc = Schedule.objects.get(id=id)
#     return render(request,"doctor/doctoreditschedule.html",{'data':doc})
#
# def doctor_editschedulepost(request):
#     date = request.POST['textfield']
#     fromtime = request.POST['textfield2']
#     totime = request.POST['textfield3']
#     id = request.POST['id']
#
#     s = Schedule.objects.get(id=id)
#     s.DOCTOR = Doctor.objects.get(LOGIN_id=request.session['lid'])
#     s.date = date
#     s.fromtime = fromtime
#     s.totime = totime
#     s.save()
#
#     return HttpResponse('''<script>alert("Edited successfully");window.location='/myapp/doctor_Doctorviewschedule/'</script>''')
#




def admin_Doctorviewschedule(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Schedule.objects.filter(DOCTOR__LOGIN_id=request.session['lid'])
        return render(request,"admin/viewsdoctorchedule.html",{'data':dr})



def admin_Doctorviewschedulepost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate = request.POST['from']
        todate = request.POST['to']
        ds = Schedule.objects.filter(date__range=[fromdate, todate],DOCTOR__LOGIN_id=request.session['lid'])
        return render(request,"admin/viewsdoctorchedule.html",{'data':ds})



def admin_viewregisterduser(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        uobj=User.objects.all()

        return render(request,"admin/viewregisterduser.html",{'data':uobj})

def admin_viewregisterduserpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name = request.POST['search']
        uobj = User.objects.filter(uname__icontains=name)
        return render(request,"admin/viewregisterduser.html",{'data':uobj})

def admin_viewdoctorbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Booking.objects.all()
        return render(request,"admin/Viewbooking.html",{'data':dr})

def admin_viewdoctorbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Booking.objects.filter(date__range=[fromdate,todate])
        return render(request,"admin/Viewbooking.html",{'data':dr,'id':id})


def admin_viewservicebookingreports(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=ServiceBooking.objects.all()
        return render(request,"admin/Viewservicebooking.html",{'data':dr})

def admin_viewservicebookingreports_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=ServiceBooking.objects.filter(date__range=[fromdate,todate])
        return render(request,"admin/Viewservicebooking.html",{'data':dr})

def admin_viewreviews(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        r=Reviews.objects.all()

        return render(request,"admin/View reviews.html",{'data':r})
def admin_viewreviews_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Reviews.objects.filter(date__range=[fromdate,todate])

        return render(request, "admin/View reviews.html", {'data': r})

def admin_viewappfeedback(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        r=Feedback.objects.all()

        return render(request,"admin/viewfeedback.html",{'data':r})
def admin_viewappfeedback_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Feedback.objects.filter(date__range=[fromdate,todate])

        return render(request, "admin/viewfeedback.html", {'data': r})
def admin_viewmedicinestock(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        r=Medicine_stock.objects.all()

        return render(request,"admin/view medicinestock.html",{'data':r})
def admin_viewmedicinestock_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Medicine_stock.objects.filter(date__range=[fromdate,todate])

        return render(request,"admin/view medicinestock.html",{'data':r})
def admin_viewpaymentdoc_reports(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        r=Paymentdoc.objects.all()


        return render(request,"admin/viewPayments.html",{'data':r})
def admin_viewpaymentdoc_reports_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Paymentdoc.objects.filter(date__range=[fromdate,todate])

    return render(request, "admin/viewPayments.html", {'data': r})
def admin_viewpaymentserv_reports(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        r1=Paymentserv.objects.all()

        return render(request,"admin/viewPaymentsserv.html",{'data1':r1})
def admin_viewpaymentserv_reports_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Paymentserv.objects.filter(date__range=[fromdate,todate])

        return render(request, "admin/viewPaymentsserv.html", {'data1': r})
def admin_viewpaymentpack_reports(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:

        r2=Paymentpack.objects.all()

        return render(request,"admin/viewPaymentspack.html",{'data2':r2})
def admin_viewpaymentpack_reports_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['s']
        todate=request.POST['todate']
        r = Paymentdoc.objects.filter(date__range=[fromdate,todate])

        return render(request, "admin/viewPaymentspack.html", {'data2': r})


#####################
def doctor_home(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"doctor/doctorhomeindex.html")
def doctor_viewprofile(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr = Doctor.objects.get(LOGIN_id=request.session['lid'])
        return render(request,"doctor/viewprofile.html",{'data':dr})

def doctor_changepassword(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"doctor/changepassword.html")


def doctor_changepasswordpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        oldpassword=request.POST['oldp']
        newp=request.POST['newp']
        cp=request.POST['cp']

        res=Login.objects.filter(id=request.session['lid'],password=oldpassword)
        if res.exists():
            log = Login.objects.get(id=request.session['lid'], password=oldpassword)
            if log is not None:
                if newp==cp:
                    log=Login.objects.filter(id=request.session['lid'],password=oldpassword).update(password=cp)
                    return HttpResponse('''<script>alert("Password changed successfully");window.location='/myapp/login/'</script>''')
                else:
                    return HttpResponse('''<script>alert("Password miss matched");window.location='/myapp/doctor_changepassword/'</script>''')
            else:
                return HttpResponse( '''<script>alert("User not found");window.location='/myapp/doctor_changepassword/'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid");window.location='/myapp/doctor_changepassword/'</script>''')


def doctor_Addschedule(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"doctor/Addschedule.html")
def doctor_Addschedulepost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        date=request.POST['textfield']
        fromtime=request.POST['textfield2']
        totime=request.POST['textfield3']


        s=Schedule()
        s.DOCTOR=Doctor.objects.get(LOGIN_id=request.session['lid'])
        s.date=date
        s.fromtime=fromtime
        s.totime=totime
        s.save()
        return HttpResponse('''<script>alert("successfully added");window.location='/myapp/doctor_Addschedule/'</script>''')


def doctor_Doctorviewschedule(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Schedule.objects.filter(DOCTOR__LOGIN_id=request.session['lid'])
        return render(request,"doctor/Doctorviewschedule.html",{'data':dr})



def doctor_Doctorviewschedulepost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate = request.POST['from']
        todate = request.POST['to']
        ds = Schedule.objects.filter(date__range=[fromdate, todate],DOCTOR__LOGIN_id=request.session['lid'])
        return render(request, "doctor/Doctorviewschedule.html", {'data': ds})



def doctor_Doctordelete_schedule(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph =Schedule.objects.get(id=id)
        ph.delete()
        return HttpResponse(
            '''<script>alert("Deleted Schedule successfully");window.location='/myapp/doctor_Doctorviewschedule/'</script>''')

def doctor_editschedule(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        doc = Schedule.objects.get(id=id)
        return render(request,"doctor/doctoreditschedule.html",{'data':doc})

def doctor_editschedulepost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        date = request.POST['textfield']
        fromtime = request.POST['textfield2']
        totime = request.POST['textfield3']
        id = request.POST['id']

        s = Schedule.objects.get(id=id)
        s.DOCTOR = Doctor.objects.get(LOGIN_id=request.session['lid'])
        s.date = date
        s.fromtime = fromtime
        s.totime = totime
        s.save()

        return HttpResponse('''<script>alert("Edited successfully");window.location='/myapp/doctor_Doctorviewschedule/'</script>''')

def doctor_viewdoctorbookingappoinment(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Appointment.objects.filter(SCHEDULE_id=id)
        return render(request,"doctor/Viewdoctorappoinments.html",{'data':dr,'id':id})

def doctor_viewdoctorbookingappoinment_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        id=request.POST['id']
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Appointment.objects.filter(SCHEDULE_id=id,date__range=[fromdate,todate])
        return render(request,"doctor/Viewdoctorappoinments.html",{'data':dr,'id':id})
def doctor_addprescription(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"doctor/addprescription.html",{'id':id})

def doctor_addprescriptionppost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        prescription=request.POST['textarea']
        id=request.POST['id']

        p=Prescription()
        p.APPOINTEMENT_id=id
        p.prescription=prescription
        p.save()

        return HttpResponse('''<script>alert("Successfully prescription added");window.location='/myapp/doctor_Doctorviewschedule/'</script>''')
def doctor_viewprescription(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj=Prescription.objects.filter(APPOINTEMENT=id)
        return render(request,"doctor/viewprescription.html",{'data':dobj})

def doctor_assign_therapist(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dd=Therapist.objects.all()
        print(id)
        return render(request,"doctor/addprescription.html",{'id':id,'data':dd})

def doctor_assign_therapist_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        THERAPIST=request.POST['textarea']
        id=request.POST['id']
        print(id)
        p=Assign_therapist()
        p.APPOINTMENT_id=id
        from datetime import datetime
        p.date=datetime.now()
        p.status='assigned'
        p.THERAPIST_id=THERAPIST
        p.save()

        return HttpResponse('''<script>alert("Assigned Therapist");window.location='/myapp/doctor_Doctorviewschedule/'</script>''')
def doctor_viewassigned_therapist(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj=Assign_therapist.objects.filter(APPOINTMENT_id=id)
        return render(request,"doctor/viewassignedtherapist.html",{'data':dobj})
def dovtor_viewsalary(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Salary.objects.filter(LOGIN_id=request.session['lid'])
        return render(request,"doctor/viewsalary.html",{'data':dr})


def doctorviewsalarypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate = request.POST['from']
        todate = request.POST['to']
        ds = Salary.objects.filter(date__range=[fromdate, todate],LOGIN_id=request.session['lid'])
        return render(request,"doctor/viewsalary.html",{'data':ds})


##################therapist
def therapist_home(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"therapist/therapisthomeindex.html")

def therapist_viewprofile(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr = Therapist.objects.get(LOGIN_id=request.session['lid'])
        return render(request,"therapist/viewprofile.html",{'data':dr})

def therapist_changepassword(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"therapist/changepassword.html")



def therapist_changepasswordpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        oldpassword = request.POST['oldp']
        newp = request.POST['newp']
        cp = request.POST['cp']

        res = Login.objects.filter(id=request.session['lid'], password=oldpassword)
        if res.exists():
            log = Login.objects.get(id=request.session['lid'], password=oldpassword)
            if log is not None:
                if newp == cp:
                    log = Login.objects.filter(id=request.session['lid'], password=oldpassword).update(password=cp)
                    return HttpResponse(
                        '''<script>alert("Password changed successfully");window.location='/myapp/login/'</script>''')
                else:
                    return HttpResponse(
                        '''<script>alert("Password miss matched");window.location='/myapp/therapist_changepassword/'</script>''')
            else:
                return HttpResponse(
                    '''<script>alert("User not found");window.location='/myapp/therapist_changepassword/'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid");window.location='/myapp/therapist_changepassword/'</script>''')


def therapist_viewsalary(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Salary.objects.filter(LOGIN_id=request.session['lid'])
        return render(request,"therapist/viewsalary.html",{'data':dr})


def therapistviewsalarypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate = request.POST['from']
        todate = request.POST['to']
        ds = Salary.objects.filter(date__range=[fromdate, todate],LOGIN_id=request.session['lid'])
        return render(request,"therapist/viewsalary.html",{'data':ds})




# def therapist_viewreviews(request):
#     r=Complaint.objects.all()
#
#     return render(request,"admin/viewcomplaint.html",{'data':r})
# def therapist_viewreviews_post(request):
#     fromdate=request.POST['s']
#     todate=request.POST['todate']
#     r = Complaint.objects.filter(date__range=[fromdate,todate])
#
#     return render(request, "admin/viewcomplaint.html", {'data': r})
def therapist_viewassigneduser(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        uobj=Assign_therapist.objects.filter(THERAPIST__LOGIN_id=request.session['lid'])

        return render(request,"therapist/viewassigneduser.html",{'data':uobj})

def therapist_viewassigneduser_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name = request.POST['search']
        uobj = User.objects.filter(uname__icontains=name)
        return render(request,"therapist/viewassigneduser.html",{'data':uobj})
def therapist_addprescription(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"therapist/addprescription.html",{'id':id})

def therapist_addprescriptionppost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        prescription=request.POST['textarea']
        id=request.POST['id']

        p=Therapist_Prescription()
        p.APPOINTEMENT_id=id
        p.prescription=prescription
        p.save()

        return HttpResponse('''<script>alert("Successfully prescription added");window.location='/myapp/therapist_viewassigneduser/'</script>''')
def therapist_viewprescription(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj=Therapist_Prescription.objects.filter(APPOINTEMENT=id)
        return render(request,"therapist/viewprescription.html",{'data':dobj})


####################staff
def staff_home(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"staff/staffhomeindex.html")
def staff_viewprofile(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr = Staff.objects.get(LOGIN_id=request.session['lid'])
        return render(request,"doctor/viewprofile.html",{'data':dr})
def staff_viewsalary(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Salary.objects.filter(LOGIN_id=request.session['lid'])
        return render(request,"staff/viewsalary.html",{'data':dr})


def staffviewsalarypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate = request.POST['from']
        todate = request.POST['to']
        ds = Salary.objects.filter(date__range=[fromdate, todate],LOGIN_id=request.session['lid'])
        return render(request,"staff/viewsalary.html",{'data':ds})



def staff_changepassword(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"staff/changepassword.html")



def staff_changepasswordpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        oldpassword = request.POST['oldp']
        newp = request.POST['newp']
        cp = request.POST['cp']

        res = Login.objects.filter(id=request.session['lid'], password=oldpassword)
        if res.exists():
            log = Login.objects.get(id=request.session['lid'], password=oldpassword)
            if log is not None:
                if newp == cp:
                    log = Login.objects.filter(id=request.session['lid'], password=oldpassword).update(password=cp)
                    return HttpResponse(
                        '''<script>alert("Password changed successfully");window.location='/myapp/login/'</script>''')
                else:
                    return HttpResponse(
                        '''<script>alert("Password miss matched");window.location='/myapp/staff_changepassword/'</script>''')
            else:
                return HttpResponse(
                    '''<script>alert("User not found");window.location='/myapp/staff_changepassword/'</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid");window.location='/myapp/staff_changepassword/'</script>''')
def staff_addmedicine_entry(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"staff/add_medicine.html")
def staff_addmedicine_entry_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        Medicinename=request.POST['textfield']
        Amount=request.POST['textfield2']
        Description=request.POST['textarea']


        mobj=Medicine()
        mobj.mname=Medicinename
        mobj.description=Description
        mobj.amount=Amount
        mobj.STAFF_id=Staff.objects.get(LOGIN_id=request.session['lid']).id
        mobj.save()
        return HttpResponse('''<script>alert("successfully added");window.location='/myapp/staff_addmedicine_entry/'</script>''')

def staff_deletemedicine_entry(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph = Medicine.objects.get(id=id)
        ph.delete()
        return HttpResponse(
            '''<script>alert("Deleted medicine successfully");window.location='/myapp/staff_viewmedicine_entry/'</script>''')


def staff_editmedicine(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph = Medicine.objects.get(id=id)
        return render(request,"Staff/edit_medicine.html",{'data':ph})

def staff_editmedicineentypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        mname=request.POST['textfield']
        amount=request.POST['textfield2']
        description=request.POST['textarea']
        id=request.POST["id"]

        pobj = Medicine.objects.get(id=id)
        pobj.mname=mname
        pobj.amount=amount
        pobj.description=description
        pobj.save()

        return HttpResponse('''<script>alert("Edited successfully");window.location='/myapp/staff_viewmedicine_entry/'</script>''')


def staff_viewmedicine_entry(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        data=Medicine.objects.all()
        return render(request,"staff/view_medicine.html",{'data':data})

def staff_viewmedicine_entrypost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name = request.POST['textfield']
        pobj = Medicine.objects.filter( mname__icontains=name,PHARMACY__LOGIN_id= request.session['lid'])
        return render(request, "staff/view_medicine.html", {'data': pobj})


def staff_addService_entry(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"staff/add_services .html")
def staff_addService_entry_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        sservice=request.POST['textfield']
        Amount=request.POST['textfield2']
        Description=request.POST['textarea']


        mobj=service()
        mobj.service=sservice
        mobj.details=Description
        mobj.amount=Amount
        mobj.STAFF_id=Staff.objects.get(LOGIN_id=request.session['lid']).id
        mobj.save()
        return HttpResponse('''<script>alert("successfully added");window.location='/myapp/staff_addService_entry/'</script>''')

def staff_deleteService_entry(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph = service.objects.get(id=id)
        ph.delete()
        return HttpResponse(
            '''<script>alert("Deleted medicine successfully");window.location='/myapp/staff_ViewService_entry/'</script>''')


def staff_editService_entry(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph = service.objects.get(id=id)
        return render(request,"staff/edit_services .html",{'data':ph})

def staff_editService_entry_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        sservice=request.POST['textfield']
        amount=request.POST['textfield2']
        description=request.POST['textarea']
        id=request.POST["id"]

        pobj = service.objects.get(id=id)
        pobj.service=sservice
        pobj.amount=amount
        pobj.details=description
        pobj.save()

        return HttpResponse('''<script>alert("Edited successfully");window.location='/myapp/staff_ViewService_entry/'</script>''')


def staff_ViewService_entry(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        data=service.objects.all()
        return render(request,"staff/view_service.html",{'data':data})

def staff_ViewService_entry_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        name = request.POST['textfield']
        pobj = Medicine.objects.filter( mname__icontains=name,PHARMACY__LOGIN_id= request.session['lid'])
        return render(request, "staff/view_service.html", {'data': pobj})





def staff_viewbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Appointment.objects.filter(status='pending')
        return render(request,"staff/Viewappiontment.html",{'data':dr})

def staff_viewbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Appointment.objects.filter(date__range=[fromdate,todate],status='pending')
        return render(request,"staff/Viewappiontment.html",{'data':dr})
def staff_viewapprovedbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Appointment.objects.filter(status='approved')
        return render(request,"staff/Viewapprovedappiontment.html",{'data':dr})

def staff_viewapprovedbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Appointment.objects.filter(date__range=[fromdate,todate],status='approved')
        return render(request,"staff/Viewapprovedappiontment.html",{'data':dr})
def staff_viewrejectedbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Appointment.objects.filter(status='rejected')
        return render(request,"staff/Viewrejectedappiontment.html",{'data':dr})

def staff_viewrejectedbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Appointment.objects.filter(date__range=[fromdate,todate],status='rejected')
        return render(request,"staff/Viewrejectedappiontment.html",{'data':dr})
def staff_approvebooking(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Appointment.objects.filter(id=id).update(status='approved')
        return HttpResponse('''<script>alert("Approved successfully");window.location='/myapp/staff_viewbooking/'</script>''')
def staff_rejectbooking(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Appointment.objects.filter(id=id).update(status='rejected')
        return HttpResponse('''<script>alert("Rejected successfully");window.location='/myapp/staff_viewbooking/'</script>''')



def staff_reschedule(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        doc = Schedule.objects.get(id=id)
        return render(request,"doctor/doctoreditschedule.html",{'data':doc})

def staff_reschedulepost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        date = request.POST['textfield']
        fromtime = request.POST['textfield2']
        totime = request.POST['textfield3']
        id = request.POST['id']

        s = Schedule.objects.get(id=id)
        s.DOCTOR = Doctor.objects.get(LOGIN_id=request.session['lid'])
        s.date = date
        s.fromtime = fromtime
        s.totime = totime
        s.save()

        return HttpResponse('''<script>alert("Edited successfully");window.location='/myapp/doctor_Doctorviewschedule/'</script>''')


def staff_viewpatientsmedicalhistoryreports(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Prescription.objects.all()
        return render(request,"staff/viewpatientmedicalreport.html",{'data':dr})

def staff_viewpatientsmedicalhistoryreports_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Prescription.objects.filter(APPOINTEMENT__date__range=[fromdate,todate])
        return render(request,"staff/viewpatientmedicalreport.html",{'data':dr})
# def staff_viewmedicine_entry(request):
#     data=Medicine.objects.all()
#     return render(request,"pharmacy/view_medicine.html",{'data':data})
#
# def staff_viewmedicine_entrypost(request):
#     name = request.POST['textfield']
#     pobj = Medicine.objects.filter( mname__icontains=name,PHARMACY__LOGIN_id= request.session['lid'])
#     return render(request, "pharmacy/view_medicine.html", {'data': pobj})
def staff_viewservicebooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        data=ServiceBooking.objects.filter(status='pending')
        return render(request,"staff/Viewserviceensuredtopatientbydoctor.html",{'data':data})

def staff_viewservicebookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromd= request.POST['textfield']
        tod = request.POST['textfield2']
        pobj = ServiceBooking.objects.filter(date___range=[fromd,tod],status='pending')
        return render(request, "staff/Viewserviceensuredtopatientbydoctor.html", {'data': pobj})
def staff_viewapprovedservicebooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=ServiceBooking.objects.filter(status='approved')
        return render(request,"staff/Viewapprovedserviceensuredtopatientbydoctor.html",{'data':dr})

def staff_viewapprovedservicebookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=ServiceBooking.objects.filter(date__range=[fromdate,todate],status='approved')
        return render(request,"staff/Viewapprovedserviceensuredtopatientbydoctor.html",{'data':dr})
def staff_viewrejectedservicebooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=ServiceBooking.objects.filter(status='rejected')
        return render(request,"staff/Viewrejectedserviceensuredtopatientbydoctor.html",{'data':dr})

def staff_viewrejectedservicebookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=ServiceBooking.objects.filter(date__range=[fromdate,todate],status='rejected')
        return render(request,"staff/Viewrejectedserviceensuredtopatientbydoctor.html",{'data':dr})
def staff_approveservicebooking(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=ServiceBooking.objects.filter(id=id).update(status='approved')
        return HttpResponse('''<script>alert("Approved successfully");window.location='/myapp/staff_viewservicebooking/'</script>''')
def staff_rejectservicebooking(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=ServiceBooking.objects.filter(id=id).update(status='rejected')
        return HttpResponse('''<script>alert("Rejected successfully");window.location='/myapp/staff_viewservicebooking/'</script>''')

def staff_viewtpbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        data=Treatmentpackage_Booking.objects.filter(status='pending')
        return render(request,"staff/Viewtreatmentpackagebookingand schedule.html",{'data':data})

def staff_viewtpbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromd= request.POST['textfield']
        tod = request.POST['textfield2']
        pobj = Treatmentpackage_Booking.objects.filter(date__range=[fromd,tod],status='pending')
        return render(request,"staff/Viewtreatmentpackagebookingand schedule.html",{'data':pobj})
def staff_viewapprovetpbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Treatmentpackage_Booking.objects.filter(status='approved')
        return render(request,"staff/Viewapprovedtreatmentpackagebookingand schedule.html",{'data':dr})

def staff_viewapprovedtpbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Treatmentpackage_Booking.objects.filter(date__range=[fromdate,todate],status='approved')
        return render(request,"staff/Viewapprovedtreatmentpackagebookingand schedule.html",{'data':dr})
def staff_viewrejectedtpbooking(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Treatmentpackage_Booking.objects.filter(status='rejected')
        return render(request,"staff/Viewrejectedtreatmentpackagebookingand schedule.html",{'data':dr})

def staff_viewrejectedtpbookingpost(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        fromdate=request.POST['textfield']
        todate=request.POST['textfield2']
        dr=Treatmentpackage_Booking.objects.filter(date__range=[fromdate,todate],status='rejected')
        return render(request,"staff/Viewrejectedtreatmentpackagebookingand schedule.html",{'data':dr})
def staff_approvetpbooking(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Treatmentpackage_Booking.objects.filter(id=id).update(status='approved')
        return HttpResponse('''<script>alert("Approved successfully");window.location='/myapp/staff_viewtpbooking/'</script>''')
def staff_rejecttpbooking(request,id):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dr=Treatmentpackage_Booking.objects.filter(id=id).update(status='rejected')
        return HttpResponse('''<script>alert("Rejected successfully");window.location='/myapp/staff_viewtpbooking/'</script>''')



# def View_therapist_booking_entryfor_patients(request,id):
#     if request.session['lid']=='':
#         return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
#     else:
#         dr=Appointment.objects.filter(SCHEDULE_id=id)
#         return render(request,"doctor/Viewdoctorbooking.html",{'data':dr,'id':id})
#
# def View_therapist_booking_entryfor_patients_post(request):
#     if request.session['lid']=='':
#         return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
#     else:
#         id=request.POST['id']
#         fromdate=request.POST['textfield']
#         todate=request.POST['textfield2']
#         dr=Appointment.objects.filter(SCHEDULE_id=id,date__range=[fromdate,todate])
#         return render(request,"doctor/Viewdoctorbooking.html",{'data':dr,'id':id})


def staff_addtreatmentpackages(request,):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"staff/add_treatmentpackages.html")

def staff_addtreatmentpackages_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        tpname = request.POST['textfield']
        Amount = request.POST['textfield2']
        Description = request.POST['textarea']
        image = request.FILES['image']
        fs = FileSystemStorage()
        from datetime import datetime
        s = "treatpack/" + datetime.now().strftime("%Y%m%d%H%M%S") + image.name
        fn = fs.save(s, image)
        mobj = Treatmentpackage()
        mobj.Packagename = tpname
        mobj.details = Description
        mobj.amount = Amount
        mobj.image = fs.url(s)
        mobj.STAFF_id = Staff.objects.get(LOGIN_id=request.session['lid']).id
        mobj.save()
        return HttpResponse(
            '''<script>alert("successfully added");window.location='/myapp/staff_addtreatmentpackages/'</script>''')


def staff_View_treatmentpackages(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj=Treatmentpackage.objects.all()
        return render(request,"staff/view_treatmentpackages.html",{'data':dobj})
def staff_View_treatmentpackages_post(request):
    if request.session['lid']=='':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj=Treatmentpackage.objects.filter(id=id)
        return render(request,"staff/view_treatmentpackages.html",{'data':dobj})

def staff_edit_treatmentpackages(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph = Treatmentpackage.objects.get(id=id)
        return render(request, "staff/edit_treatmentpackages.html", {'data': ph})


def staff_edit_treatmentpackages_post(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        tpname = request.POST['textfield']
        Amount = request.POST['textfield2']
        Description = request.POST['textarea']
        id = request.POST["id"]
        if 'image' in request.FILES:
            image = request.FILES['image']

            fs = FileSystemStorage()
            from datetime import datetime
            s = "treatpack/" + datetime.now().strftime("%Y%m%d%H%M%S") + image.name
            fn = fs.save(s, image)
            pobj = Treatmentpackage.objects.get(id=id)
            pobj.image = fs.url(s)
            pobj.save()

        pobj = Treatmentpackage.objects.get(id=id)
        pobj.service = tpname
        pobj.amount = Amount
        pobj.details = Description
        pobj.save()

        return HttpResponse(
            '''<script>alert("Edited successfully");window.location='/myapp/staff_View_treatmentpackages/'</script>''')


def staff_delete_treatmentpackages(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        ph = service.objects.get(id=id)
        ph.delete()
        return HttpResponse(
            '''<script>alert("Deleted  successfully");window.location='/myapp/staff_View_treatmentpackages/'</script>''')
def staff_addstock(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        return render(request,"staff/addstock.html",{'id':id})

def staff_addstockpost(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        stockk=request.POST['textarea']
        id=request.POST['id']

        p=Medicine_stock()
        p.MEDICINCE_id=id
        p.stock=stockk
        from datetime import datetime
        p.date=datetime.now()
        p.save()

        return HttpResponse('''<script>alert("Successfully stock added");window.location='/myapp/staff_viewmedicine_entry/'</script>''')
def staff_viewstock(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Already Logouted');window.location='/myapp/login/'</script>")
    else:
        dobj=Medicine_stock.objects.filter(MEDICINCE_id=id)
        return render(request,"staff/viewstock.html",{'data':dobj})


##################################user

def user_signup(request):
    uname=request.POST['uname']
    gender=request.POST['gender']
    dob=request.POST['dob']
    phonenumber=request.POST['phonenumber']
    email=request.POST['email']
    place=request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    district=request.POST['district']
    photo=request.POST['photo']
    pswd=request.POST['pswd']
    cpswd=request.POST['cpswd']
    lobj = Login()
    lobj.username = email
    lobj.password = cpswd
    lobj.type = 'user'
    lobj.save()
    import datetime
    import base64
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    a = base64.b64decode(photo)
    fh = open(r"C:\\Users\\Microsoft\\PycharmProjects\\KDproject\\media\\user\\" + date + ".jpg", "wb")
    path = "/media/user/" + date + ".jpg"
    fh.write(a)
    fh.close()
    sobj = User()
    sobj.uname = uname
    sobj.gender = gender
    sobj.dob = dob
    sobj.place = place
    sobj.post = post
    sobj.district = district
    sobj.pin = pin
    sobj.email = email
    sobj.photo =path
    sobj.phonenumber = phonenumber
    sobj.status = 'pending'
    sobj.LOGIN = lobj
    sobj.save()
    return JsonResponse({'status':'ok'})
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    obj = Login.objects.filter(username=username, password=password)
    if obj.exists():
        obj = Login.objects.get(username=username, password=password)
        lid = obj.id
        if obj.type == 'user':
            return JsonResponse({'status': 'ok', 'lid': lid, 'type': obj.type})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})
def user_view_profile(request):
    lid = request.POST['lid']
    oo = User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': 'ok', 'uname': oo.uname, 'gender': oo.gender,
                         'dob': oo.dob, 'phonenumber': oo.phonenumber, 'email': oo.email,
                         'place': oo.place, 'post': oo.post, 'pin': oo.pin,'district':oo.district,'photo':oo.photo})
def user_edit_profile(request):
    lid = request.POST['lid']
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    email = request.POST['email']
    phone = request.POST['phone']

    experience = request.POST['experience']
    qualification = request.POST['qualification']
    place = request.POST['place']
    district = request.POST['district']
    state = request.POST['state']

    photo = request.POST['photo']

    print(photo, "hellloooooooo", "")
    if len(photo) > 0:
        a = base64.b64decode(photo)
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fh = open(r"C:\Users\Microsoft\PycharmProjects\Evcharging\media\photo\\" + date + ".jpg", "wb")
        path = "/media/photo/" + date + ".jpg"
        fh.write(a)
        fh.close()
        res = User.objects.filter(LOGIN=lid).update(wname=name, dob=dob, gender=gender, phone=phone, email=email,
                                                       experience=experience, qualification=qualification,
                                                       photo=path, place=place, state=state, district=district)


    else:
        res = User.objects.filter(LOGIN=lid).update(wname=name, dob=dob, gender=gender, phone=phone, email=email,
                                                       experience=experience, qualification=qualification,
                                                       place=place, state=state, district=district)

    return JsonResponse({'status':'ok'})
def user_change_password(request):
    lid = request.POST['lid']
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']
    if newpassword == confirmpassword:
        obj = Login.objects.filter(id=lid, password=oldpassword)
        if obj.exists():
            obj = Login.objects.get(id=lid, password=oldpassword)
            obj.password = confirmpassword
            obj.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})
def user_view_doctors(request):
    oo = Doctor.objects.all()
    l = []
    for i in oo:
        l.append({'id': i.id, 'dname': i.dname,
                  'gender': i.gender, 'dob': i.dob,
                  'place': i.place, 'post': i.post,'department':i.department,'email':i.email,'photo':i.photo,'phno':i.phno,})
    return JsonResponse({'status':'ok','data':l})
def user_view_therapist(request):
    lid=request.POST['lid']
    oo = Assign_therapist.objects.filter(APPOINTMENT__USER__LOGIN_id=lid)
    l = []
    for i in oo:
        l.append({'id': i.id, 'THERAPIST_name': i.THERAPIST.tname,'THERAPIST_department': i.THERAPIST.department,'THERAPIST_qualification': i.THERAPIST.qualification,'photo': i.THERAPIST.photo,
                  'APPOINTMENT_date': i.APPOINTMENT.date, 'assigneddate': i.date,
                  'SCHEDULE_date': i.APPOINTMENT.SCHEDULE.date, 'DOCTOR': i.APPOINTMENT.SCHEDULE.DOCTOR.dname
                   })
        print(l)
    return JsonResponse({'status': 'ok', 'data': l})
def user_view_doctorschedule(request):
    did=request.POST['sid']
    oo = Schedule.objects.filter(DOCTOR_id=did)
    l = []
    for i in oo:
        l.append({'id': i.id, 'date': i.date,
                  'fromtime': i.fromtime, 'totime': i.totime,
                   })
    return JsonResponse({'status': 'ok', 'data': l})
def user_make_appointment(request):
    lid = request.POST['lid']
    res = User.objects.get(LOGIN__id=lid)
    sid = request.POST['sid']
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    aobj = Appointment()
    aobj.date = date
    aobj.USER = res
    aobj.SCHEDULE_id = sid
    aobj.status='pending'
    aobj.save()
    return JsonResponse({'status': "ok"})
def usr_send_complaint(request):
    lid = request.POST['lid']
    # res = User.objects.get(LOGIN__id=lid)
    sid = request.POST['complaint']
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    aobj = Complaint()
    aobj.date = date
    aobj.status = 'pending'
    aobj.reply = 'pending'
    aobj.USER_id = User.objects.get(LOGIN__id=lid).id
    aobj.complaint = sid
    aobj.save()
    return JsonResponse({'status': "ok"})
def usr_send_feedback(request):
    lid = request.POST['lid']
    # res = User.objects.get(LOGIN__id=lid)
    sid = request.POST['Feedback']
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    aobj = Feedback()
    aobj.date = date
    aobj.USER_id = User.objects.get(LOGIN__id=lid).id
    aobj.Feedback = sid
    aobj.save()
    return JsonResponse({'status': "ok"})
def Cust_Send_reviews(request):
    lid = request.POST['lid']
    res = User.objects.get(LOGIN__id=lid).id
    sid = request.POST['review']
    rid = request.POST['rating']
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    aobj = Reviews()
    aobj.date = date

    aobj.USER_id = res
    aobj.review = sid
    aobj.rating = rid
    aobj.save()
    return JsonResponse({'status': "ok"})


def user_view_appoinmentstatus(request):
    lid = request.POST['lid']
    res = User.objects.get(LOGIN__id=lid)
    ress = Appointment.objects.filter(USER=res)
    l = []
    for i in ress:
        l.append({'id': i.id, 'dname': i.SCHEDULE.DOCTOR.dname, 'date': i.date,
                  'fromtime': i.SCHEDULE.fromtime, 'totime': i.SCHEDULE.totime,'status': i.status, })
    return JsonResponse({'status': "ok", "data": l})

def user_view_medical_history(request):
    lid = request.POST['lid']
    res = User.objects.get(LOGIN__id=lid)
    ress = Prescription.objects.filter(USER=res)
    l = []
    for i in ress:
        l.append({'id': i.id, 'dname': i.SCHEDULE.DOCTOR.dname, 'date': i.APPOINTEMENT.date,
                  'fromtime': i.SCHEDULE.fromtime, 'totime': i.SCHEDULE.totime,'totime': i.SCHEDULE.totime, })
    return JsonResponse({'status': "ok", "data": l})
def user_view_service_history(request):
    lid = request.POST['lid']
    res = User.objects.get(LOGIN__id=lid)
    ress = Sericebooking.objects.filter(USER=res)
    l = []
    for i in ress:
        l.append({'id': i.SCHEDULE.DOCTOR.LOGIN_id, 'dname': i.SCHEDULE.DOCTOR.dname, 'date': i.date,
                  'fromtime': i.SCHEDULE.fromtime, 'totime': i.SCHEDULE.totime, })
def user_view_service(request):

    ress = service.objects.all()
    l = []
    for i in ress:
        l.append({'id': i.id, 'service': i.service, 'amount': i.amount,
                  'details': i.details })
    return JsonResponse({'status': "ok", "data": l})
def user_view_packages(request):

    ress = Treatmentpackage.objects.all()
    l = []
    for i in ress:
        l.append({'id': i.id, 'Packagename': i.Packagename, 'amount': i.amount,
                  'details': i.details,'image': i.image })
    return JsonResponse({'status': "ok", "data": l})
def user_view_service_schedule_to_him_its_added_by_staff(request):

    return JsonResponse({'status':'ok'})
def usr_view_reply(request):
    lid=request.POST['lid']
    res = User.objects.get(LOGIN=lid).id

    oo=Complaint.objects.filter(USER=res)
    l=[]
    for i in oo:
        l.append({'id':i.id,'date':i.date,'complaint':i.complaint,'status':i.status,'reply':i.reply})

    return JsonResponse({'status':'ok','data':l})
