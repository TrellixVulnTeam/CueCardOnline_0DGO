from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib import auth
import django
from .models import Company,Cue,Press_cue_A,Press_cue_B,Press_cue_C

# Create your views here.
#def custom_page_not_found(request): ยังแก้ปัญหา 404 หลัง register ไม่ได้
#    return django.views.defaults.page_not_found(request, None)


def index(request):
    return render(request, 'index.html')

def info(request):
    return render(request, 'info.html')

def register(request):
    return render(request, 'register.html')
    #return render(request, 'request_cue_form.html')

def addUser(request):
    username = request.POST['username']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    password = request.POST['password']
    #repassword = request.POST['repassword']

    User.objects.create_user(
            username = username,
            password = password,
            email = email,
            first_name = firstname,
            last_name = lastname,
            )
    #User.save()
    return render(request, 'register_done.html')
'''
    if password == repassword : #เช็คว่า password 2 ช่องตรงกันมั้ย ถ้าตรงไปต่อ
        if User.objects.filter(username=username).exists(): #เช็คว่า username ซ้ำกับที่เคยลงไว้มั้ย
            messages.info(request,'Username นี้มีผู้ใช้แล้ว')
            print("Username นี้มีคนใช้แล้ว")
            return redirect('/register')
        elif User.objects.filter(email=email).exists(): #เช็คว่า email ซ้ำมั้ย
            messages.info(request, 'Email นี้มีผู้ใช้แล้ว')
            print("Email นี้มีผู้ใช้งานแล้ว")
            return redirect('/register')
        else:   #ถ้าไม่ซ้ำ ให้ทำการบันทึกข้อมูล
            User.objects.create_user(
            username = username,
            password = password,
            email = email,
            first_name = firstname,
            last_name = lastname,
            )
            User.save()
            return render(request, 'register_done.html')
    else:   #password ไม่ตรงกัน ลงทะเบียนใหม่
        messages.info(request, 'Password ไม่ตรงกัน')
        return redirect('/register')
'''

def register_done(request):
    return render(request, 'register_done.html')

#Cue Table
def cue_table(request):
    return render(request, 'Cue_table.html')

def customer_cue(request):
    data = Cue.objects.all()
    return render(request, 'customer_cue.html',{'cues':data})

def shop_admin(request):
    #Query Data Cue Table
    data = Cue.objects.all()
    return render(request, 'shop_admin.html', {'cues':data})

#Change Cue A ติดอยู่ ยังแก้ไม่ได้
def change_cue_a(request):
    #Save Cue A for update data
    #data_a = Cue(cue_type='ฝาก ถอน โอน จ่าย',cue_number=2)
    change_cue_a = request.POST['change_cue_a']
    data_a = Cue.objects.filter.get(pk=1)(
        cue_number = change_cue_a
    )
    data_a.save()

# หน้าเลือกคิว
def shop_choose_cue(request):
    return render(request, 'shop_choose_cue.html')

# คำสั่งหน้าเลือกคิว
def press_cue_a(request):
    press_a = Press_cue_A(
        cue_type = 'ฝาก ถอน โอน จ่าย'
    )
    press_a.save()
    show_a = Press_cue_A.objects.last()
    return render(request,'customer_cue.html', {'currentA':show_a})

#Log in
def login(request):
    return render(request, 'login.html')
#Log in Success
def login_success(request):
    username = request.POST['username']
    password = request.POST['password']

    #check username + password ว่าตรงกับที่เคยบันทึกมั้ย
    user = auth.authenticate(username=username,password=password)

    if user is not None :   #ถ้า user ไม่เป็น ว่าง ถือว่าผ่าน
        auth.login(request,user)
        return redirect('/')
    else:   #ถ้า user เป็นว่าง คือ ไม่พบข้อมูลผู้ใช้
        messages.info(request, 'ไม่พบข้อมูลผู้ใช้ หรือ รหัสผ่านผิด')
        return redirect('/login')

#Log Out
def logout(request):
    auth.logout(request)
    return redirect('/login')

#Cue request form
def cue_request_form(request):
    return render(request, 'request_cue_form.html')

#Add Cue Request
def add_cue_request(request):
    company_name = request.POST['company']
    branch = request.POST['branch']
    requirement = request.POST['cuedetail']

    company = Company(
        company_name=company_name,
        branch=branch,
        requirement=requirement,
    )
    company.save()
    return redirect('/add_cue_request_done')

#Add Cue Request Done
def add_cue_request_done(request):
    return render(request, 'request_cue_done.html')