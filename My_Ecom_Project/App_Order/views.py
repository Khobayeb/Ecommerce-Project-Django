from django.shortcuts import render, get_object_or_404,redirect


# Authenticate
from django.contrib.auth.decorators import login_required

#models
from App_Order.models import Cart, Order
from App_Shop.models import Product
#message
from django.contrib import messages

from App_Shop.models import Product
# Create your views here.

@login_required
def add_to_card(request, pk):      # je item card a add korbo sei item er primary key accept korbe
    item= get_object_or_404(Product, pk=pk) # add kora item call korbe
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False) # item check korbe cart a add kora ace ki na
    order_qs= Order.objects.filter(user=request.user, ordered=False)  # add kora item order a ace ki na check kora
    if order_qs.exists():   # present user er incomplete order ace kina
        order = order_qs[0] # 1st object order a save hobe . object view theke dictionary te convert korci order name
        if order.orderitems.filter(item=item).exists(): # order er item er vitore (item) ace  ki na check korci. new j item order krci seta age order korci ki na check kora hobe
            order_item[0].quantity += 1  # if true then 1 barbe
            order_item[0].save()
            messages.info(request, "This item quantity was updated.") #  after save then send message by messages and item add korle then quantity barbe
            return redirect("App_Shop:home")

        else:  
            order.orderitems.add(order_item[0])  # if not true . add kora item jodi kothao na thake cart/ order . new item add korte hbe.
            messages.info(request, "This item wass added to your cart")
            return redirect("App_Shop:home")

    else:
        order= Order(user=request.user) # cart a jodi kno add/ order kora na thake thn create korte hbe
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, "This item wass added to your card")
        return redirect("App_Shop:home")

@login_required
def cart_view(request):
    carts= Cart.objects.filter(user=request.user, purchased=False)
    orders= Order.objects.filter(user= request.user, ordered=False)
    if carts.exists() and orders.exists():
        order= orders[0]
        return render(request, 'App_Order/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect("App_Shop:home")

# remove cart item
@login_required
def remove_from_cart(request, pk):
    item= get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order= order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user = request.user, purchased=False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was remove from your cart!")
            return redirect("App_Order:cart")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")

@login_required
def increase_cart(request, pk):
    item= get_object_or_404(Product, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
          order_item = Cart.objects.filter(item=item,user=request.user, purchased=False)[0]
          if order_item.quantity >=1:
              order_item.quantity +=1
              order_item.save()
              messages.info(request, f"{item.name} quantity has been updated")
              return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not your cart")
            return redirect("App_Shop:home")


    else:
        messages.info(request, "YOu Don't have an active Order")
        return redirect("App_Shop:home")
        
@login_required
def decrease_cart(request, pk):
    item= get_object_or_404(Product, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order= order_qs[0]
        if order.orderitems.filter(item=item).exists():
             order_item = Cart.objects.filter(item=item,user=request.user, purchased=False)[0]
             if order_item.quantity>1:
                 order_item.quantity -=1
                 order_item.save()
                 messages.info(request,f"{item.name} quantity has been updates")
                 return redirect("App_Order:cart")
             else:
                 order.orderitems.remove(order_item)
                 order_item.delete()
                 messages.warning(request, f"{item.name} item has been removed from your cart")
                 return redirect("App_Shop:home")

        else:
            messages.info(request, f"{item.name} is not your cart")
            return redirect("App_Shop:home")


    else:
     messages.info(request, "YOu Don't have an active Order")
     return redirect("App_Shop:home")