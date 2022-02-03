from django.db import models

# Create your models here.


class Dealer(models.Model):
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Email = models.EmailField()
    Place = models.CharField(max_length=100)
    Phone = models.IntegerField()
    Password = models.CharField(max_length=8)
    Confirmpassword =models.CharField(max_length=8)
    Status = models.BooleanField(default=False)

    def __str___(self):
        return self.Firstname

    
choice=(
    ('male','Male'),
    ('female','Female')
)

district=(
    ('kasaragod','Kasaragod'),
    ('kannur', 'Kannur'),
    ('kozhikode', 'Kozhikode'),
    ('wayanad', 'Wayanad'),
    ('malappuram', 'Malappuram'),
    ('palakkad', 'Palakkad'),
    ('thrissur', 'Thrissur')
)

class Farmer(models.Model):
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100,choices=choice)
    Address = models.CharField(max_length=100)
    Email = models.EmailField()
    Place = models.CharField(max_length=100)
    Phone = models.IntegerField()
    Village = models.CharField(max_length=100)
    District = models.CharField(max_length=100,choices=district)
    Password = models.CharField(max_length=8)
    Confirmpassword = models.CharField(max_length=8)
    Status = models.BooleanField(default=False)


    def __str___(self):
        return self.Firstname

class Category(models.Model):
    Name = models.CharField(max_length=50)
    Photo = models.ImageField()


    def __str___(self):
        return self.Name


class Product(models.Model):
    OwnerId = models.PositiveIntegerField()
    OwnerName = models.CharField(max_length=100)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    Name = models.CharField(max_length=40)
    Price = models.PositiveIntegerField()
    Rent_Amount = models.PositiveIntegerField()
    Quantity = models.PositiveIntegerField()
    Photo = models.ImageField()
    Use = models.TextField()

    def __str__(self):
        return self.Name

class Order(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField()
    Total_Amount = models.PositiveIntegerField()
    Farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE)
    Dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE)
    Type = models.CharField(max_length=50)
    Status = models.CharField(max_length=50,default="Pending")

    def __str__(self):
        return self.Product.Name


class DealerNotification(models.Model):
    DealerId = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    Notification = models.TextField()

    def __str__(self):
        return self.Notification


class KnowledgeCenterNotification(models.Model):
    Notification = models.TextField()

    def __str__(self):
        return self.Notification

class KnowledgeCenterService(models.Model):
    Service = models.TextField()

    def __str__(self):
        return self.Service


class Complaint(models.Model):
    Farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    Query = models.TextField()
    Query_Date = models.DateField()
    Reply = models.TextField(null=True)
    Reply_Date = models.DateField(null=True)
    
class Question(models.Model):
    Farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Quest = models.TextField()
    Quest_Date=models.DateTimeField()
    Reply = models.TextField(null=True)
    Reply_Dtae = models.DateTimeField(null=True)

    def __str__(self):
        return self.Quest

class Rent(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    No_of_Days = models.PositiveIntegerField()
    Farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE)
    Total_Amount = models.PositiveIntegerField()
    Rent_Date = models.DateTimeField(null=True)
    Return_Date = models.DateTimeField(blank=True,null=True)
    Status = models.CharField(max_length=50,default="Pending")

    def __str__(self):
        return self.Product.Name



    
