from django.db import models

# Create your models here.

class table1_user(models.Model):
    user_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    customername=models.CharField(max_length=50,default="")
    mobile = models.CharField(max_length=50, default="")
    pincode = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=250, default="")

    def __str__(self):
        return self.username


class table2_products(models.Model):
    productname = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    description = models.CharField(max_length=100) 
    TYPE_CHOICES = [
        ('Regular', 'regular'),
        ('Doctor Prescription', 'doctor prescription'),
    ]
    product_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='regular') 
    photo = models.ImageField(upload_to='pharmacy/', blank=True, null=True)

    def __str__(self):
        return self.productname



class table3_orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(table1_user, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    status = models.CharField(max_length=100, default="pending")
    pincode = models.CharField(max_length=10)
    product_type = models.CharField(max_length=50, default="Regular")  # ✅ New field
    prescription = models.ImageField(upload_to="prescriptions/", blank=True, null=True)
    productname = models.CharField(max_length=100)
    orderdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    

class table4_cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(table1_user, on_delete=models.CASCADE)
    product = models.ForeignKey(table2_products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    product_type = models.CharField(max_length=50, default="Regular")

    def __str__(self):
        return f"{self.user.username} - {self.product.productname}"

class table5_ReportCollection(models.Model):
    user = models.ForeignKey(
        table1_user,
        on_delete=models.CASCADE,
        related_name="reports",
        db_column="user_id" )
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
        