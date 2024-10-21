
from django.db import models

# Create your models here.


class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class Doctor(models.Model):
    dname=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    photo=models.CharField(max_length=500)
    phno=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
class Staff(models.Model):
    sname=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    photo=models.CharField(max_length=500)
    phno=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
class Therapist(models.Model):
    tname=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    photo=models.CharField(max_length=500)
    phno=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=100)



class User(models.Model):
    uname=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=20)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    photo=models.CharField(max_length=500)
    LOGIN=models.ForeignKey(Login, on_delete=models.CASCADE)



class Complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    USER=models.ForeignKey(Login, on_delete=models.CASCADE)

class Feedback(models.Model):
    date=models.DateField()
    Feedback=models.CharField(max_length=100)
    USER=models.ForeignKey(Login, on_delete=models.CASCADE)

class Reviews(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
    USER=models.ForeignKey(Login, on_delete=models.CASCADE)

class Schedule(models.Model):
    date=models.DateField()
    DOCTOR=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    fromtime=models.CharField(max_length=100)
    totime=models.CharField(max_length=100)

class Appointment(models.Model):
    date=models.DateField()
    USER=models.ForeignKey(User, on_delete=models.CASCADE)
    SCHEDULE=models.ForeignKey(Schedule,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

class Medicine(models.Model):
    mname=models.CharField(max_length=500)
    description=models.CharField(max_length=100)
    amount=models.IntegerField()
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)
class Medicine_stock(models.Model):
    stock = models.CharField(max_length=500)
    date=models.DateField()
    MEDICINCE = models.ForeignKey(Medicine, on_delete=models.CASCADE)
class Prescription(models.Model):
    prescription=models.CharField(max_length=500)
    APPOINTEMENT = models.ForeignKey(Appointment, on_delete=models.CASCADE)
class Therapist_Prescription(models.Model):
    prescription=models.CharField(max_length=500)
    APPOINTEMENT = models.ForeignKey(Appointment, on_delete=models.CASCADE)


class service(models.Model):
    service=models.CharField(max_length=500)
    amount=models.CharField(max_length=500)
    details=models.CharField(max_length=500)
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)

class Treatmentpackage(models.Model):
    Packagename=models.CharField(max_length=500)
    amount=models.CharField(max_length=500)
    details=models.CharField(max_length=500)
    image=models.CharField(max_length=500)
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)




class Booking(models.Model):
    DOCTOR=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date=models.DateField()

class ServiceBooking(models.Model):
    service=models.ForeignKey(service,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    date=models.DateField()

class Treatmentpackage_Booking(models.Model):
    TREATMENTPACKAGE=models.ForeignKey(Treatmentpackage,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    status = models.CharField(max_length=100)

class Assign_therapist(models.Model):
    THERAPIST=models.ForeignKey(Therapist,on_delete=models.CASCADE)
    APPOINTMENT=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    date=models.DateField()
    status = models.CharField(max_length=100)


class Billsdoc(models.Model):
    DOCBOOKING=models.ForeignKey(Booking,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=200)
    amount=models.CharField(max_length=200)
class Billservice(models.Model):
    SERVBOOKING=models.ForeignKey(ServiceBooking,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=200)
    amount=models.CharField(max_length=200)
class Billspackages(models.Model):
    PACKBOOKING=models.ForeignKey(Treatmentpackage_Booking,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=200)
    amount=models.CharField(max_length=200)

class Salary(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    Amount = models.CharField(max_length=100)
    Year = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    date=models.DateField()

class MedicalReport(models.Model):
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    DOCTOR = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    report = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    date=models.DateField()



class Paymentdoc(models.Model):
    BILLsDOC=models.ForeignKey(Billsdoc,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    amount=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
class Paymentserv(models.Model):
    BILLSERV=models.ForeignKey(Billservice,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    amount=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
class Paymentpack(models.Model):
    BILLSPACK=models.ForeignKey(Billspackages,on_delete=models.CASCADE)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    amount=models.CharField(max_length=200)
    status=models.CharField(max_length=200)