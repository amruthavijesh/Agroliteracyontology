from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Farmer, Dealer, Category, Product, Order, KnowledgeCenterNotification, DealerNotification, KnowledgeCenterService, Complaint, Question, Rent
from django.contrib.auth.forms import AuthenticationForm
from .forms import FarmerRegForm, DealerRegForm, FarmerLoginForm, DealerLoginForm, FarmerUpdateForm, DealerUpdateForm, CategoryForm, AddProductForm
from .forms import KnowledgeCenterNotificationForm, DealerNotificationForm, KnowledgeCenterServiceForm, ComplaintForm, ComplaintReplyForm, QuestionForm, QuestionReplyForm, PasswordChangeForm
from django.contrib import messages
from django.contrib import auth
from datetime import date
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'ontology/index.html')

def admin_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session['email'] = username
                request.session['sid'] = user.id
                return redirect('ontology:knowledge_center_home')
            else:
                messages.error(request, 'Error wrong username/password')
                msg = "wrong username or password"
                args = {'form': form, 'error': msg}
                return render(request, 'ontology/sales_point_login.html', args)
    else:
        form = AuthenticationForm()
    return render(request, 'ontology/admin_page.html', {'form': form})


def knowledge_center_home(request):
    if request.session.has_key:
        username = request.session['email']
        sid = request.session['sid']
        return render(request, 'ontology/knowledge_center_home.html', {'name':username, 'sid':sid})

def manage_farmer(request):
    farmers = Farmer.objects.all()
    return render(request, 'ontology/manage_farmer.html', {'farmers':farmers})

def approve_farmer(request, id):
    farmer = Farmer.objects.get(id=id)
    farmer.Status=1
    farmer.save()
    return redirect('/manage_farmer')

def reject_farmer(request, id):
    farmer = Farmer.objects.get(id=id)
    farmer.Status=0
    farmer.save()
    return redirect('/manage_farmer')



def view_all_farmers(request):
    viewall = Farmer.objects.filter(Status=True)
    return render(request, 'ontology/view_all_farmers.html', {'viewall':viewall})



def knowledge_center_view_all_products(request):
    admin = User.objects.all()
    product = Product.objects.all()
    return render(request, 'ontology/knowledge_center_view_all_products.html', {'admin':admin, 'product':product})



def add_knowledge_center_notification(request):
    admin = User.objects.all()
    if request.method == 'POST':
        form = KnowledgeCenterNotificationForm(request.POST)
        if form.is_valid():
            notification = form.cleaned_data['Notification']
            res = KnowledgeCenterNotification(Notification=notification)
            res.save()
            messages.success(request, "Notification Added successfully")
            return redirect('ontology:knowledge_center_home')
    else:
        form = KnowledgeCenterNotificationForm()
    return render(request, 'ontology/add_knowledge_center_notification.html', {'admin':admin, 'form':form})
    

def admin_view_notification(request):
    dealer = Dealer.objects.all()
    notification = DealerNotification.objects.all()
    return render(request, 'ontology/admin_view_notification.html', {'dealer':dealer, 'notification':notification}) 


def add_knowledge_center_service(request):
    admin = User.objects.all()
    if request.method == 'POST':
        form = KnowledgeCenterServiceForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['Service']
            res = KnowledgeCenterService(Service=service)
            res.save()
            messages.success(request, "Service Added successfully")
            return redirect('ontology:knowledge_center_home')
    else:
        form = KnowledgeCenterServiceForm()
    return render(request, 'ontology/add_knowledge_center_service.html', {'admin':admin, 'form':form})
    

def admin_view_complaints(request):
    complaint = Complaint.objects.all()
    return render(request, 'ontology/admin_view_complaints.html', {'complaint':complaint})


def send_complaint_reply(request, id):
    aid = request.session['sid']
    #admin = User.objects.get(id=aid)
    complaint = Complaint.objects.get(id=id)
    farmer = Farmer.objects.get(id=complaint.Farmer_id)
    if request.method == 'POST':
        form = ComplaintReplyForm(request.POST)
        if form.is_valid():
            reply = form.cleaned_data['Reply']
            complaint.Reply_Date=date.today()
            complaint.Reply=reply
            complaint.save()
            messages.success(request,"Reply send!")
            return redirect('/admin_view_complaints')
    else:
        form = ComplaintReplyForm()
    return render(request, 'ontology/send_complaint_reply.html', {'complaint':complaint, 'farmer':farmer})


def admin_view_questions(request):
    question = Question.objects.all()
    return render(request, 'ontology/admin_view_questions.html', {'question':question})


            

def send_question_reply(request, id):
    aid = request.session['sid']
    question = Question.objects.get(id=aid)
    farmer = Farmer.objects.get(id=question.Farmer_id)
    product = Product.objects.get(id=question.Product_id)
    if request.method == 'POST':
        form = QuestionReplyForm(request.POST)
        if form.is_valid():
            reply = form.cleaned_data['Reply']
            question.Reply_Dtae=date.today()
            question.Reply=reply
            question.save()
            messages.success(request, "Reply send")
            return redirect('/admin_view_questions')

    else:
        form = QuestionReplyForm()
    return render(request, 'ontology/send_question_reply.html', {'question':question, 'farmer':farmer, 'product':product, 'form':form})



def farmer_reg(request):
    if request.method == 'POST':
        form = FarmerRegForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['Firstname']
            lastname = form.cleaned_data['Lastname']
            gender = form.cleaned_data['Gender']
            address = form.cleaned_data['Address']
            email = form.cleaned_data['Email']
            place = form.cleaned_data['Place']
            phone = form.cleaned_data['Phone']
            village = form.cleaned_data['Village']
            district = form.cleaned_data['District']
            password = form.cleaned_data['Password']
            confirmpassword = form.cleaned_data['Confirmpassword']
            

            fr = Farmer.objects.filter(Email=email).exists()

            if fr:
                messages.warning(request,"Farmer with same email is already exist!")
                return redirect('/farmer_reg')

            elif password!=confirmpassword:
                messages.warning(request,"Password Mismatch")
                return redirect('/farmer_reg')

            else:
                res=Farmer(Firstname=firstname,Lastname=lastname,Gender=gender,Address=address,Email=email,Place=place,
                            Phone=phone,Village=village,District=district,Password=password,Confirmpassword=confirmpassword)
                res.save()
                messages.success(request,"Account created successfully!")
                return redirect('/farmer_page')
    else:
        form=FarmerRegForm()
    return render(request,'ontology/farmer_reg.html',{'form':form})


def farmer_page(request):
    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']

            try:
                fr = Farmer.objects.get(Email=email,Status=True)

                if not fr:
                    messages.warning(request,"Invalid User!")
                    return redirect('/farmer_page')

                elif password!=fr.Password:
                    messages.warning(request,"Invalid password!")
                    return redirect('/farmer_page')

                else:
                    request.session['email'] = email
                    request.session['sid']=fr.id
                    messages.success(request,"Login Successfull")
                    return redirect('/farmer_home/%s' % fr.id)
            except:
                messages.warning(request,"User does not exist")
                return redirect('/farmer_page')
    else:
        form=FarmerLoginForm()
    return render(request,'ontology/farmer_page.html',{'form':form})


    


def farmer_home(request, id):
    if request.session.has_key:
        email = request.session['email']
        fid = request.session['sid']
        fmr = Farmer.objects.get(Email=email) 
        return render(request, 'ontology/farmer_home.html', {'fmr':fmr})


def view_farmer_profile(request, id):
    email = request.session['email']
    farmer = Farmer.objects.get(id=id)
    form = FarmerUpdateForm(request.POST or None,instance=farmer )
    if form.is_valid():
        firstname = form.cleaned_data['Firstname']
        lastname = form.cleaned_data['Lastname']
        gender = form.cleaned_data['Gender']
        address = form.cleaned_data['Address']
        email = form.cleaned_data['Email']
        place = form.cleaned_data['Place']
        phone = form.cleaned_data['Phone']
        village = form.cleaned_data['Village']
        district = form.cleaned_data['District']
        form.save()
        messages.success(request, "Upadated successfully")
        return redirect('/farmer_home/%s' %id)
    return render(request,'ontology/view_farmer_profile.html',{'form':form,'farmer':farmer})


def view_product_cat(request):
    fmr = request.session['sid']
    farmer = Farmer.objects.get(id=fmr)
    category = Category.objects.all()
    return render(request, 'ontology/view_product_cat.html', {'farmer':farmer, 'category':category})

def show_products(request, id):
    fmr = request.session['sid']
    farmer = Farmer.objects.get(id=fmr)
    category = Category.objects.get(id=id)
    product = Product.objects.filter(Category_id=id)
    return render(request, 'ontology/show_products.html', {'farmer':farmer, 'category':category, 'product':product})


def show_single_product(request, id):
    fmr = request.session['sid']
    farmer = Farmer.objects.get(id=fmr)
    product = Product.objects.get(id=id)
    return render(request, 'ontology/show_single_product.html', {'farmer':farmer, 'product':product})



def farmer_buy_product(request, id):
    fmr = request.session['sid']
    farmer = Farmer.objects.get(id=fmr)
    product = Product.objects.get(id=id)
    dealer = Dealer.objects.get(id=product.OwnerId)
    quantity = int(request.POST.get('quantity'))
    payment_type = request.POST.get('type')
    price = product.Price
    total = quantity * price
    res = Order(Product=product, Farmer=farmer, Quantity=quantity, Dealer=dealer, Total_Amount=total, Type=payment_type)
    res.save()
    product.Quantity = product.Quantity - quantity
    product.save()

    if payment_type=='standard':
        args={'farmer':farmer,'product':product,'dealer':dealer,'quantity':quantity,'price':price,'total':total}
        return render(request,'ontology/farmer_buy_product.html',args)
    elif payment_type=='online':
        request.session['amount']=total
        return redirect('/online_payment/%s' %id)
    else:
        return HttpResponse("You Must Select One Type of Delivery")



def rent_equipment(request):
    fid = request.session['sid']
    farmer = Farmer.objects.get(id=fid)
    category = Category.objects.filter(Name='Equipments')
    product = Product.objects.filter(Category_id=4)
    args={'farmer':farmer,'category':category,'product':product}
    return render(request,'ontology/rent_equipment.html',args)



def show_single_equipment(request,id):
    fid = request.session['sid']
    farmer = Farmer.objects.get(id=fid)
    product = Product.objects.get(id=id)
    return render(request,'ontology/show_single_equipment.html',{'farmer': farmer,'product': product})



def farmer_rent_equipment(request, id):
    fmr = request.session['sid']
    farmer = Farmer.objects.get(id=fmr)
    product = Product.objects.get(id=id)
    dealer = Dealer.objects.get(id=product.OwnerId)
    no_of_days = int(request.POST.get('No_of_Days'))
    return_date = request.POST.get('Return_Date')
    rent_amount = product.Rent_Amount
    total = no_of_days * rent_amount
    res = Rent(Product=product, Farmer=farmer, No_of_Days=no_of_days, Total_Amount=total, Rent_Date=date.today(), Return_Date=return_date)
    res.save()
    args={'farmer':farmer,'product':product,'dealer':dealer,'no_of_days':no_of_days,'Rent_Amount':rent_amount,'total':total,'return_date':return_date}
    return render(request,'ontology/farmer_rent_equipment.html',args)



def online_payment(request, id):
    fmr = request.session['sid']
    farmer = Farmer.objects.get(id=fmr)
    product = Product.objects.get(id=id)
    amount = request.session['amount']
    return render(request,'ontology/online_payment.html', {'farmer':farmer, 'product':product, 'amount':amount})



def farmer_view_notification(request):
    fid = request.session['sid']
    dnotification = DealerNotification.objects.all()
    anotification = KnowledgeCenterNotification.objects.all()
    return render(request, 'ontology/farmer_view_notification.html', {'dnotification':dnotification, 'anotification':anotification})


def farmer_view_payment_detail(request):
    fid = request.session['sid']
    order = Order.objects.all()
    return render(request, 'ontology/farmer_view_payment_detail.html', {'order':order})


def farmer_view_services(request):
    fid = request.session['sid']
    service = KnowledgeCenterService.objects.all()
    return render(request, 'ontology/farmer_view_services.html', {'service':service})


def send_complaint(request, id):
    fid = request.session['sid']
    farmer = Farmer.objects.get(id=id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['Query']
            res = Complaint(Farmer=farmer, Query=query, Query_Date=date.today())
            res.save()
            messages.success(request, "send query success")
            return redirect('/send_complaint/%s' % id)
    else:
        form = ComplaintForm()
    return render(request, 'ontology/send_complaint.html', {'farmer':farmer, 'form':form} )



def add_question(request, id):
    fid= request.session['sid']
    farmer = Farmer.objects.get(id=fid)
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            quest = form.cleaned_data['Quest']
            res = Question(Farmer=farmer, Product=product, Quest=quest, Quest_Date=date.today())
            res.save()
            messages.success(request, "Question send successfully")
            return redirect('/add_question/%s' % id)
    else:
        form = QuestionForm()
    return render(request, 'ontology/add_question.html', {'form':form, 'farmer':farmer, 'product':product})



def farmer_change_password(request, id):
    fid = request.session['sid']
    farmer = Farmer.objects.get(id=id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data['OldPassword']
            newpassword = form.cleaned_data['NewPassword']
            confirmpassword = form.cleaned_data['ConfirmPassword']
            if oldpassword!=farmer.Password:
                msg = "Enter Correct Password"
                return render(request, 'ontology/farmer_change_password.html', {'form':form, 'error':msg, 'farmer':farmer})
            elif newpassword!=confirmpassword:
                msg = "Password Does Not Match"
                return render(request, 'ontology/farmer_change_password.html', {'form':form, 'error':msg, 'farmer':farmer})
            else:
                farmer.Password = newpassword
                farmer.Confirmpassword = confirmpassword
                farmer.save()
                msg = "Password Changed Successfully"
                return render(request, 'ontology/farmer_change_password.html', {'form':form, 'error':msg, 'farmer':farmer})
    else :
        form = PasswordChangeForm()
    return render(request, 'ontology/farmer_change_password.html', {'form':form, 'farmer':farmer})
                                                     
                                                                                                                                                                                                                                                                                          
def dealer_reg(request):
    if request.method == 'POST':
        form = DealerRegForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['Firstname']
            lastname = form.cleaned_data['Lastname']
            email = form.cleaned_data['Email']
            place = form.cleaned_data['Place']
            phone = form.cleaned_data['Phone']
            password = form.cleaned_data['Password']
            confirmpassword = form.cleaned_data['Confirmpassword']
            

            dr=Dealer.objects.filter(Email=email).exists()

            if dr:
                msg="Dealer with same email is already exist!"
                args={'form':form,'error':msg}
                return render(request,'ontology/dealer_reg.html',args)

            elif password!=confirmpassword:
                msg="Enter correct password! passwword mismatch"
                args={'form':form,'error':msg}
                return render(request,'ontology/dealer_reg.html',args)

            else:
                res=Dealer(Firstname=firstname,Lastname=lastname,Email=email,Place=place,
                            Phone=phone,Password=password,Confirmpassword=confirmpassword)
                res.save()
                return redirect('ontology:dealer_reg')
    else:
        form=DealerRegForm()
    return render(request,'ontology/dealer_reg.html',{'form':form})



def dealer_page(request):
    if request.method == 'POST':
        form = DealerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']

            try:
                dr =Dealer.objects.get(Email=email,Status=True)

                if not dr:
                    messages.warning(request,"Invalid User")
                    return redirect('/dealer_page')

                elif password!=dr.Password:
                    messages.warning(request,"Invalid Password")
                    return redirect('/dealer_page')

                else:
                    request.session['email'] = email
                    request.session['sid'] = dr.id
                    messages.success(request,"Login Successfully")
                    return redirect('/dealer_home/%s' % dr.id)

            except:
                messages.warning(request,"Invalid User or Password")
                return redirect('/dealer_page')

    else:
        form = DealerLoginForm()
    return render(request,'ontology/dealer_page.html', {'form':form})
            




def dealer_home(request, id):
    if request.session.has_key:
        email = request.session['email']
        did = request.session['sid']
        dlr = Dealer.objects.get(Email=email) 
        return render(request, 'ontology/dealer_home.html', {'dlr':dlr})


def view_dealer_profile(request, id):
    email = request.session['email']
    dealer = Dealer.objects.get(id=id)
    form = DealerUpdateForm(request.POST or None, instance=dealer)
    if form.is_valid():
        firstname = form.cleaned_data['Firstname']
        lastname = form.cleaned_data['Lastname']
        email = form.cleaned_data['Email']
        place = form.cleaned_data['Place']
        phone = form.cleaned_data['Phone']
        form.save()
        messages.success(request, "Updated successfully")
        return redirect('/dealer_home/%s' %id)
    return render(request, 'ontology/view_dealer_profile.html', {'form':form, 'dealer':dealer})

def select_category(request,id):
    did = request.session['sid']
    dealer = Dealer.objects.get(id=did)
    category = Category.objects.all()
    return render(request, 'ontology/select_category.html', {'dealer':dealer, 'category':category})


def add_product(request, id):
    form = AddProductForm()
    cat = request.POST.get('Category')
    category = Category.objects.get(id=id)
    did = request.session['sid']
    dealer = Dealer.objects.get(id=did)
    if request.method=='POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['Name']
            price = form.cleaned_data['Price']
            rent_amount = form.cleaned_data['Rent_Amount']
            quantity = form.cleaned_data['Quantity']
            photo = form.cleaned_data['Photo']
            use = form.cleaned_data['Use']

            res = Product(OwnerId=did, OwnerName=dealer.Firstname, Category=category, Name=name, Price=price, Rent_Amount=rent_amount, Quantity=quantity, Photo=photo, Use=use)
            res.save()            
            messages.success(request, "Added Successfully")
            return redirect('/select_category/%s' %dealer.id)
    else:
        form = AddProductForm()
    return render(request, 'ontology/add_product.html', {'form':form, 'dealer':dealer, 'category':category})


def view_all_products(request):
    did = request.session['sid']
    dealer = Dealer.objects.get(id=did)
    product = Product.objects.filter(OwnerId=dealer.id, OwnerName=dealer.Firstname)
    return render(request,'ontology/view_all_products.html',{'dealer':dealer,'product':product})


def update_product_stock(request, id):
    did = request.session['sid']
    dealer = Dealer.objects.get(id=did)
    product = Product.objects.get(id=id)
    form = AddProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('/view_all_products')
    return render(request, 'ontology/update_product_stock.html', {'product':product, 'form':form})


def add_dealer_notification(request, id):
    dealer = Dealer.objects.get(id=id)
    if request.method == 'POST':
        form = DealerNotificationForm(request.POST)
        if form.is_valid():
            notification = form.cleaned_data['Notification']
            res = DealerNotification(DealerId=dealer, Notification=notification)
            res.save()
            messages.success(request, "Notification Added successfully")
            return render(request, 'ontology/add_dealer_notification.html', {'dealer':dealer, 'form':form})
    else:
        form = DealerNotificationForm()
    return render(request, 'ontology/add_dealer_notification.html', {'dealer':dealer, 'form':form})
    

def dealer_view_notification(request):
    did = request.session['sid']
    notification = KnowledgeCenterNotification.objects.all()
    return render(request, 'ontology/dealer_view_notification.html', {'notification':notification})


def dealer_view_payment_detail(request):
    did = request.session['sid']
    order = Order.objects.all()
    return render(request, 'ontology/dealer_view_payment_detail.html', {'order':order})



def dealer_change_password(request, id):
    did = request.session['sid']
    dealer = Dealer.objects.get(id=id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data['OldPassword']
            newpassword = form.cleaned_data['NewPassword']
            confirmpassword = form.cleaned_data['ConfirmPassword']
            if oldpassword!=dealer.Password:
                msg = "Enter Correct Password"
                return render(request, 'ontology/dealer_change_password.html', {'form':form, 'error':msg, 'dealer':dealer})
            elif newpassword!=confirmpassword:
                msg = "Password Does Not Match"
                return render(request, 'ontology/dealer_change_password.html', {'form':form, 'error':msg, 'dealer':dealer})
            else:
                dealer.Password = newpassword
                dealer.Confirmpassword = confirmpassword
                dealer.save()
                msg = "Password Changed Successfully"
                return render(request, 'ontology/dealer_change_password.html', {'form':form, 'error':msg, 'dealer':dealer})
    else :
        form = PasswordChangeForm()
    return render(request, 'ontology/dealer_change_password.html', {'form':form, 'dealer':dealer})
                                                     




def logout(request):
    try:
        del request.session['email']
        return redirect('/')
    except:
        pass




    
