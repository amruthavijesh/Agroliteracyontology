from django.contrib import admin
from .models import Farmer, Dealer, Category, Product, Order, KnowledgeCenterNotification, DealerNotification, KnowledgeCenterService, Complaint, Question, Rent 
# Register your models here.


admin.site.register(Farmer)
admin.site.register(Dealer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(KnowledgeCenterNotification)
admin.site.register(DealerNotification)
admin.site.register(KnowledgeCenterService)
admin.site.register(Complaint)
admin.site.register(Question)
admin.site.register(Rent)
