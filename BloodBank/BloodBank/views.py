from django.shortcuts import render,redirect
from user.models import User
from random import randint
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def verifyuser(request):
    msg = ""    
    email = request.GET.get('email')
    otp = int(request.GET.get('otp'))

    lst = User.objects.filter(email=email,otp=otp)
    if len(lst)==0:
        msg = "Invalid Email or OTP !"
    else:
        user = lst[0]    
        user.isverify = True
        user.save()
        msg = "Your Verification Successfully Done !"
    return render(request,'verify.html',{
            'msg' : msg
        })        

def saveuser(request):
    try:
        otp = generateOTP(5)

        ob = User()
        ob.username = request.POST.get('name')
        ob.email = request.POST.get('email')
        ob.password = request.POST.get('password')
        ob.bloodgroup = request.POST.get('group')
        ob.otp = otp
        ob.isverify=False
        ob.profilepic = "logo.png"
        ob.save() 
        request.session['regstatus'] = True       
        sendMail(ob.username,ob.email,otp)
        request.session['regstatus'] = True       
    except Exception as ex:
        print("Register Error : ",ex)   
        request.session['regstatus'] = False 
    return redirect("/register")

def home(request):
    return render(request,'index.html')
def contact(request):
    return render(request,'contact.html')  

def register(request):
    regmsg = ""      
    if 'regstatus' in request.session:        
        if request.session.get('regstatus'):
            regmsg = "Registeration Successfully Done !"
        else:
            regmsg = "Registeration Failed !"
        del request.session['regstatus']                        
    return render(request,'register.html',{
            'msg' : regmsg
    })      

def login(request):
    if request.method=="GET":
        loginmsg = ""      
        if 'loginstatus' in request.session:
            loginmsg = "Invalid Id or Password !"
            del request.session['loginstatus'] 
        elif 'verifystatus' in request.session:
            loginmsg = "Please Verify First  !"
            del request.session['verifystatus'] 
        return render(request,'login.html',{
                'msg' : loginmsg
            })      
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        userlist = User.objects.filter(email=email,password=password)  
        if len(userlist)==0:
            request.session['loginstatus'] = False 
            return redirect("/login")
        else:
            user = userlist[0]
            if user.isverify:
                request.session['loginuser'] = {
                    'userid' : user.id,
                    'name' : user.username,
                    'profilepic' : user.profilepic
                }                
                return redirect("/user/home")      
            else:
                request.session['verifystatus'] = False            
                return redirect("/login")

def sendMail(name,mail,otp):    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)  
    # start TLS for security
    s.starttls()

    message = MIMEMultipart("alternative")
    message["Subject"] = "BloodBank Verification Mail"
    message["From"] = "kamleshmohabe519@gmail.com"
    message["To"] = mail


    link = "http://localhost:8000/verifyuser?email={}&otp={}".format(mail,otp)
    # message to be sent
    msg = """
        <html>
            <body>
                <h1 style='color:red'>BloodBank Verification</h1>
                <hr>
                <b>Hello {} ,</b>
                <p>
                    Thanks for registeration in Blood Bank. This is a verification mail for your account. Please verify your account to click the below link : 
                </p>
                <br><br>
                <b> {} </b>
                <br><br>
                <hr>
            </body>
        </html>
    """.format(name,link)

    part = MIMEText(msg, "html")
    message.attach(part)
  

    # Authentication
    s.login("", "")  
    # sending the mail
    s.sendmail("", mail, message.as_string())
  
    # terminating the session
    s.quit()  

def generateOTP(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)                
