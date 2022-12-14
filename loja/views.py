from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Produto, User, Cart, Categorias
from django.template import loader
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
import mercadopago
import json
import ast
import requests

def index(request):
    latest_produto_list = Produto.objects.order_by('id')
    template = loader.get_template('loja/index.html')
    context = {
        'latest_produto_list': latest_produto_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'loja/detail.html', {'produto': produto})

def promocoes(request):
    return render(request, 'loja/promocoes.html')

def categorias(request):
    categorias_list = Categorias.objects.order_by('id')
    template = loader.get_template('loja/categorias.html')
    context = {
        'categorias_list': categorias_list,
    }
    return HttpResponse(template.render(context, request))

def categorias_filter(request, cat_id):
    produtos_list = Produto.objects.filter(categoria = cat_id)
    template = loader.get_template('loja/index.html')
    context = {
        'latest_produto_list': produtos_list,
    }
    return HttpResponse(template.render(context, request))


def perfil(request):
    return render(request, 'loja/perfil.html')

def cart(request, username):
    u = User.objects.get(username=username)
    cart = Cart.objects.filter(username = u)
    template = loader.get_template('loja/cart.html')
    context = {
        'cart': cart,
    }
    return HttpResponse(template.render(context, request))

def cart_add(request):
    if request.user.is_authenticated:
        u = User.objects.get(username= request.POST.get('username'))
        p = Produto.objects.get(id= request.POST.get('product_id'))
        n = Produto.objects.get(id= request.POST.get('product_id')).nome
        img = Produto.objects.get(id= request.POST.get('product_id')).prod_img
        v = Produto.objects.get(id= request.POST.get('product_id')).pre??o
        if len(Cart.objects.filter(username=u, produtos_id=p ))>0:
            cart_exists = Cart.objects.get(username=u, produtos_id=p )
            img = Produto.objects.get(id= request.POST.get('product_id')).prod_img
            p = Produto.objects.get(id= request.POST.get('product_id'))
            q = request.POST.get('qtd')
            v = Produto.objects.get(id= request.POST.get('product_id')).pre??o 
            update_cart = Cart(pk=int(cart_exists.pk), username=u, produtos_id=p, qtd = cart_exists.qtd + int(q), prod_img=img, pre??o = float(v), produtos_nome = n )
            update_cart.save()
        else:
            img = Produto.objects.get(id= request.POST.get('product_id')).prod_img
            u = User.objects.get(username= request.POST.get('username'))
            p = Produto.objects.get(id= request.POST.get('product_id'))
            q = request.POST.get('qtd')
            v = Produto.objects.get(id= request.POST.get('product_id')).pre??o
            n = Produto.objects.get(id= request.POST.get('product_id')).nome
            cart_instance = Cart.objects.create(username=u, produtos_id = p, qtd=q, prod_img = img, pre??o = float(v), produtos_nome = n )
    else:
        return redirect('/accounts/login')
    return redirect('/loja/cart/'+str(u))


def update_cart(request):
    #query_dict = request.POST
    #print(query_dict)
    qtds = request.POST.getlist('number')
    product_ids = request.POST.getlist('product_id')
    produtos_id = request.POST.getlist('produto_nome')
    
    u = User.objects.get(username= request.POST.get('username'))

    for a in product_ids:
        index = product_ids.index(a)
        p = Produto.objects.get(id = produtos_id[index])
        cart_exists = Cart.objects.get(username=u, produtos_id=p)
        update_cart = Cart(pk=int(cart_exists.pk), username=u, produtos_id=p, qtd = int(qtds[index]), pre??o = cart_exists.pre??o, prod_img = cart_exists.prod_img, produtos_nome=p.nome)
        update_cart.save()

    return redirect('/loja/checkout/'+str(u))


def checkout(request, username):
    u = User.objects.get(username=username)
    cart_items = Cart.objects.filter(username = u)
    total = 0
    for a in cart_items:
        subtotal = a.pre??o * a.qtd
        total += subtotal
    template = loader.get_template('loja/checkout.html')
    context = {
        'cart_items': cart_items,
        'total' : total,
    }
    return HttpResponse(template.render(context, request))


def submit_payment(request):

    query_dict = request.body    
    teste = ast.literal_eval(request.body.decode('utf-8'))
    print("----------Payment info----------")
    print("Card token: ", teste['token'])
    print("Issuer ID: ", teste['issuer_id'])
    print("Payment method: ", teste['payment_method_id'])
    print("Transaction amount: ", teste['transaction_amount'])
    print("Installments: ", teste['installments'])
    print("----------Payer info----------")
    print("Payer email: ", teste['payer']['email'])
    print("Payer identification type: ", teste['payer']['identification']['type'])
    print("Payer identification number: ", teste['payer']['identification']['number'])
    
    return redirect('/loja')
