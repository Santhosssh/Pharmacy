from django.shortcuts import render,HttpResponseRedirect, redirect
import json
from django.http import JsonResponse
from .models import table1_user,table2_products,table3_orders,table4_cart,table5_ReportCollection
from django.http import JsonResponse

# Create your views here.

def landpage(request):
    products = table2_products.objects.all()
    return render(request,"landpage.html", {"products": products})

def front(request):
    return render(request,"front.html")

def adregister(request):
    if request.method == "POST":
        username = request.POST["name"]
        password = request.POST["pas"]
        mobile = request.POST["mobile"]
        obj=table1_user()
        obj.username=username
        obj.password=password
        obj.mobile=mobile
        obj.save()
    return render(request,"front.html")

def login(request):
    if request.method == "POST":
        username = request.POST["name"]
        password = request.POST["pas"]
        if username == "admin" and password == "admin":
            return render(request, "admin.html")
        user = table1_user.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.user_id
            request.session['username'] = user.username
            res = table2_products.objects.all()
            return render(request, "user.html", {"res": res, "res1": user})
        else:
            return render(request, "front.html", {"msg": "Invalid Login"})
    return render(request, "front.html")

def logout(request):
    request.session.flush()
    return redirect('landpage')

def api_stock(request):
    products = table2_products.objects.all().order_by('-id')
    data = []
    for product in products:
        data.append({
            "id": product.id,
            "productname": product.productname,
            "description": product.description,
            "price": product.price,
            "product_type": product.product_type,
            "photo": product.photo.url if product.photo else None,  # ✅ important
        })
    return JsonResponse(data, safe=False)

def api_orders(request):
    orders = table3_orders.objects.all().order_by('-order_id')
    data = []
    for o in orders:
        data.append({
            "id": o.order_id,
            "productname": o.productname,
            "quantity": o.quantity,
            "name": o.name,
            "user_id": o.user_id,
            "mobile": o.mobile,
            "address": o.address,
            "pincode": o.pincode,
            "product_type": o.product_type,
            "status": o.status,
            "orderdate": o.orderdate.strftime("%Y-%m-%d"),
            "prescription": o.prescription.url if o.prescription else None,
        })
    return JsonResponse(data, safe=False)

def update_status(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order = table3_orders.objects.get(order_id=order_id)
            order.status = data.get("status")
            order.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False})

def api_users(request):
    users = list(table1_user.objects.values().order_by('-user_id'))
    return JsonResponse(users, safe=False)

def api_delete_product(request, id):
    table2_products.objects.filter(id=id).delete()
    return JsonResponse({"success": True})

def addproduct(request):
    if request.method == "POST":
        table2_products.objects.create(
            productname=request.POST.get('productname'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            product_type=request.POST.get('product_type'),
            photo=request.FILES.get('photo') 
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
    
def product_update(request, id):
    product = table2_products.objects.get(id=id)
    if request.method == "POST":
        product.productname = request.POST.get('productname')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.product_type = request.POST.get('product_type')
        if request.FILES.get('photo'):
            product.photo = request.FILES['photo']
        product.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
    
def single_product(request, id):
    product = table2_products.objects.get(id=id)
    data = {
        "id": product.id,
        "productname": product.productname,
        "description": product.description,
        "price": product.price,
        "product_type": product.product_type,
        "photo": product.photo.url if product.photo else None, 
    }
    return JsonResponse(data)

def admin_reports(request):
    reports = table5_ReportCollection.objects.select_related("user").order_by("-id")
    data = []
    for r in reports:
        data.append({
            "id": r.id,
            "user_id": r.user.user_id if r.user else "",
            "name": r.name,
            "mobile": r.mobile,
            "email": r.email,
            "message": r.message,
            "date": r.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return JsonResponse({"reports": data})

def user_profile(request):
    user = table1_user.objects.get(user_id=request.session['user_id'])
    if request.method == "POST":
        user.username = request.POST.get('username')
        user.customername = request.POST.get('customername')
        user.mobile = request.POST.get('mobile')
        user.pincode = request.POST.get('pincode')
        user.address = request.POST.get('address')
        user.save()
    return redirect('home')


def place_order(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        prescription_file = request.FILES.get("prescription")

        cart_data = request.POST.get("cart_data")

        if cart_data:
            try:
                cart_items = json.loads(cart_data)
            except:
                return redirect("home")
        else:
            cart_items = [{
                "product": request.POST.get("productname"),
                "quantity": request.POST.get("quantity"),
                "product_type": request.POST.get("product_type"),
            }]

        for item in cart_items:
            product_type = item.get("product_type", "").lower()
            if product_type == "doctor_prescription":
                prescription_to_save = prescription_file
            else:
                prescription_to_save = None
            table3_orders.objects.create(
                name=name,
                mobile=mobile,
                address=address,
                pincode=pincode,
                productname=item["product"],
                quantity=item["quantity"],
                product_type=product_type,
                prescription=prescription_to_save,
                user_id=user_id,
                status="pending"
            )
        return redirect("home")
    
def place_prescription(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")
        product_id = request.POST.get("product_id")
        prescription_file = request.FILES.get("prescription")
        try:
            user = table1_user.objects.get(pk=user_id)
            product = table2_products.objects.get(pk=product_id)
        except:
            return redirect("home")
        requires_prescription = (
            product.product_type and
            product.product_type.lower() == "doctor_prescription"
        )
        if requires_prescription and not prescription_file:
            return redirect("home") 
        cart_item = table4_cart.objects.filter(
            user=user,
            product=product
        ).first()

        if cart_item:
            cart_item.quantity += 1
            if prescription_file:
                cart_item.prescription = prescription_file
            cart_item.save()
        else:
            table4_cart.objects.create(
                user=user,
                product=product,
                quantity=1,
                prescription=prescription_file if requires_prescription else None
            )
        return redirect("home")

def home(request):
    if not request.session.get("user_id"):
        return redirect("login")
    user = table1_user.objects.get(pk=request.session.get("user_id"))
    res = table2_products.objects.all()
    return render(request, "user.html", {"res": res, "res1": user})

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product_type = request.POST.get("product_type") 
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse({"status": "error", "message": "Login required"})
        user = table1_user.objects.get(pk=user_id)
        product = table2_products.objects.get(pk=product_id)
        try:
            cart_item = table4_cart.objects.get(user=user, product=product)
            cart_item.quantity += quantity
            cart_item.product_type = product_type 
        except table4_cart.DoesNotExist:
            cart_item = table4_cart(
                user=user,
                product=product,
                quantity=quantity,
                product_type=product_type 
            )

        cart_item.save()
        return JsonResponse({"status": "success"})

def check_product_type(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        try:
            product = table2_products.objects.get(id=product_id)
            return JsonResponse({
                "status": "success",
                "product_type": product.product_type})
        except table2_products.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Product not found"})
        
def get_cart_items(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"cart": []})
    cart_items = table4_cart.objects.filter(user_id=user_id)
    data = []
    for item in cart_items:
        data.append({
            "cart_id": item.cart_id,
            "product": item.product.productname,
            "price": float(item.product.price),
            "quantity": item.quantity,
            "product_type": item.product.product_type,
            "image": item.product.photo.url if item.product.photo else ""
        })
    return JsonResponse({"cart": data})

def get_orders_ajax(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"redirect": "/login"}) 
    orders = table3_orders.objects.filter(user_id=user_id).order_by("-orderdate")
    orders_list = []

    for order in orders:
        orders_list.append({
            "productname": order.productname,
            "quantity": order.quantity,
            "name": order.name,
            "mobile": order.mobile,
            "address": order.address,
            "pincode": order.pincode,
            "status": order.status,
            "orderdate": order.orderdate.strftime("%Y-%m-%d %H:%M:%S"),
            "prescription": order.prescription.url if order.prescription else "",
        })
    return JsonResponse({"orders": orders_list})

def search_medicines(request):
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"results": []})
    products = table2_products.objects.filter(productname__icontains=query)
    results = []
    for product in products:
        results.append({
            "id": product.id,
            "name": product.productname,
            "price": product.price,
            "type": product.product_type,
            "image": product.photo.url if product.photo else "",
        })
    return JsonResponse({"results": results})

def submit_report(request):
    if request.method == "POST":
        try:
            user_id = request.session.get("user_id")
            if not user_id:
                return JsonResponse({"status": "error", "message": "User not logged in"})
            user = table1_user.objects.get(user_id=user_id) 
            data = json.loads(request.body)
            table5_ReportCollection.objects.create(
                user=user,
                name=data.get("name"),
                mobile=data.get("mobile"),
                email=data.get("email"),
                message=data.get("message"))
            return JsonResponse({"status": "success"})
        except table1_user.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "failed"})

def update_cart_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart_id = data.get("cart_id")
            action = data.get("action")
            if not cart_id:
                return JsonResponse({"status": "error", "message": "Cart ID missing"})
            cart_item = table4_cart.objects.get(cart_id=cart_id)
            if action == "increase":
                cart_item.quantity += 1
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({"status": "success"})
        except table4_cart.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cart item not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "failed"})

def delete_cart_item(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        cart_id = data.get("cart_id")
        try:
            cart_item = table4_cart.objects.get(cart_id=cart_id)
            cart_item.delete()
            return JsonResponse({"status": "success"})
        except table4_cart.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cart item not found"})
    return JsonResponse({"status": "failed"})