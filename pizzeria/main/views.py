from datetime import date
from http.client import responses

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection

from .models import Users
import psycopg2, urllib.request



def index(request):
    try:
        address = request.GET.get("address")
        comment = request.GET.get("comment")
        cost = request.GET.get("cost")

        cursor = connection.cursor()
        cursor.execute(f'insert into orders (id_user, orders_cost, address, comment, date) '
              f'values ({findUserBySessionToOrder(request.COOKIES["session"])}, {cost}, \'{address}\', \'{comment}\', \'{date.today()}\');')

        pizzas = request.COOKIES.get('pizzas').split()
        cursor.execute(f'SELECT id_order FROM orders ORDER BY id_order DESC LIMIT 1;')
        current_order = cursor.fetchall()[0][0]
        for i in range(0, len(pizzas)):
            cursor.execute(f'insert into orders_pizza_constr values ({current_order}, {pizzas[i]});')

        response = render(request, 'main/mainPage.html', {'order_done': True})
        response.delete_cookie('pizzas')

        return response
    except Exception as e: print(e)

    return render(request, 'main/mainPage.html')

def about(request):
    return render(request, 'main/about.html')

def account(request):
    try:
        request.COOKIES["session"]
    except:
        # Take input data------------------------------------------------
        users = Users.objects.all()
        user_id = 0
        email, password, phone, name = 'None'
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                phone = request.POST.get("phone")
                name = request.POST.get("name")
            except:
                pass

        # Search for the desired user
        if (phone == None and name == None):  # If Log In
            for user in users:
                if user.email == email and user.user_password == password:
                    user_id = user.id_user



        else:  # If Registration
            cursor = connection.cursor()
            cursor.execute(f'select * from create_user(\'{name}\', \'{email}\', \'{phone}\', \'{password}\');')
            cursor.fetchall()
        cursor = connection.cursor()
        if (phone != None and name != None): # If Registration (2)
            cursor.execute(f'SELECT id_user FROM users ORDER BY id_user DESC LIMIT 1;')
            user_id = cursor.fetchall()[0][0]
        cursor.execute(f'select * from generate_session_id({user_id});')
        cursor.fetchall()


        response = render(request, 'main/account.html')
        if (user_id != 0):
            response.set_cookie('session', findUserByID(Users.objects.all(), user_id).session_id, max_age=260000)
            return response
        else:
            return render(request, 'main/mainPage.html', {'alert_flag': True})


    response = render(request, 'main/account.html', context=findUserBySession(request.COOKIES["session"]))

    cursor = connection.cursor()
    cursor.execute(f'select id_pizza from pizza_constr as pc join users as u on pc.id_user = u.id_user where session_id = {request.COOKIES["session"]};')
    pizza_numbers = cursor.fetchall()
    res = ''
    for el in pizza_numbers:
        cursor.execute(f'select id_order from orders_pizza_constr where id_pizza = {el[0]};')
        if (cursor.fetchall() == []):
            res += f'{el[0]} '
    response.set_cookie('pizzas', f'{res.lstrip()}')

    return response

def findUserByID(users, userID):
    for user in users:
        if (user.id_user == userID):
            return user

def findUserBySession(sessionID):
    cursor = connection.cursor()
    cursor.execute(f'select * from users where session_id = {sessionID};')
    currentUser = cursor.fetchall()[0]
    user_dictionary = {'name': currentUser[1], 'email': currentUser[2], 'phone': currentUser[3]}
    return user_dictionary

def findUserBySessionToOrder(sessionID):
    cursor = connection.cursor()
    cursor.execute(f'select id_user from users where session_id = {sessionID};')
    currentUser = cursor.fetchall()[0][0]
    return currentUser