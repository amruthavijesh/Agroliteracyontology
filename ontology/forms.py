from .models import Farmer, Dealer, Category, Product, DealerNotification, KnowledgeCenterNotification, KnowledgeCenterService, Complaint, Question, Rent
from django import forms

class FarmerRegForm(forms.ModelForm):

    Password=forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=8)
    Confirmpassword=forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=8)
    class Meta():
        model = Farmer
        fields = ('Firstname','Lastname','Gender','Address','Email','Place','Phone','Village','District','Password','Confirmpassword')



class FarmerLoginForm(forms.ModelForm):
    Password= forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = Farmer
        fields = ('Email', 'Password')


class DealerRegForm(forms.ModelForm):

    Password=forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=8)
    Confirmpassword=forms.CharField(widget=forms.PasswordInput,min_length=8,max_length=8)
    class Meta():
        model = Dealer
        fields = ('Firstname','Lastname','Email','Place','Phone','Password','Confirmpassword')

class DealerLoginForm(forms.ModelForm):
    Password= forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = Dealer
        fields = ('Email', 'Password')

class FarmerUpdateForm(forms.ModelForm):
    class Meta():
        model = Farmer
        fields = ('Firstname','Lastname','Gender','Address','Email','Place','Phone','Village','District')

class DealerUpdateForm(forms.ModelForm):
    class Meta():
        model = Dealer
        fields = ('Firstname','Lastname','Email','Place','Phone') 

class CategoryForm(forms.ModelForm):
    class Meta():
        model = Product
        fields =('Category',)

class AddProductForm(forms.ModelForm):
    class Meta():
        model = Product
        fields = ('Name', 'Price', 'Rent_Amount', 'Quantity', 'Photo', 'Use')

class DealerNotificationForm(forms.ModelForm):
    class Meta():
        model = DealerNotification
        fields = ('Notification',)


class KnowledgeCenterNotificationForm(forms.ModelForm):
    class Meta():
        model = KnowledgeCenterNotification
        fields = ('Notification',)

class KnowledgeCenterServiceForm(forms.ModelForm):
    class Meta():
        model = KnowledgeCenterService
        fields = ('Service',)

class ComplaintForm(forms.ModelForm):
    class Meta():
        model = Complaint
        fields = ('Query',)

class ComplaintReplyForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('Reply',)

class QuestionForm(forms.ModelForm):
    class Meta():
        model = Question
        fields = ('Quest',)

class QuestionReplyForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('Reply',)


class PasswordChangeForm(forms.Form):
    OldPassword = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=8)
    NewPassword = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=8)
    ConfirmPassword = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=8)











