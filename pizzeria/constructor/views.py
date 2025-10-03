from datetime import date

from django.shortcuts import render
from django.db import connection


# Create your views here.


def order(request):


    try:
        # ПРОВЕРКА НА НАЛИЧИЕ УЖЕ ИМЕЮЩИХСЯ ПИЦЦ -----------------------------------------
        fillings = doOrderPizzas(request.COOKIES.get('pizzas'))
        response = render(request, 'constructor/order.html', context=fillings)

        # ВЫБОРКА ВСЕХ НЕОБХОДИМЫХ ДАННЫХ О ПИЦЦЕ ----------------------------------------
        name = request.GET.get("name")
        size = request.GET.get("size")
        filling = request.COOKIES.get('filling')
        sauce = request.COOKIES.get('sauce')
        session = request.COOKIES.get('session')

        # УДАЛЕНИЕ ПИЦЦЫ -----------------------------------------------------------------
        try:
            del_pizza = request.COOKIES.get('deletingPizza')
            response.delete_cookie('deletingPizza', path='/constructor')
            all_pizzas = request.COOKIES.get('pizzas').replace(f'{del_pizza}', '')

            cursor = connection.cursor()
            cursor.execute(f'delete from pizza_constr where id_pizza={del_pizza};')

            response.set_cookie('pizzas', ''.join(all_pizzas).strip())
            response.set_cookie('isLoad', 'true')
            return response
        except:
            pass

        # ФИЧА
        if (name == None or size == None or filling == None or sauce == None or session == None):
            response.delete_cookie('isLoad')
            return response


        # ПОИСК ПОСЛЕДНЕЙ ДОБАВЛЕННОЙ ПИЦЦЫ ----------------------------------------------
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM pizza_constr ORDER BY id_pizza DESC LIMIT 1')
        # ПРОВЕРКА, ДОБАВЛЕНА ЛИ ОНА УЖЕ
        if (cursor.fetchall()[0][1] == name):
            return render(request, 'constructor/order.html', context=fillings)

        # ДОБАВЛЕНИЕ ПИЦЦЫ ---------------------------------------------------------------
        cursor.execute(f'select cost_index from dough where id_dough = {size};')
        cursor.execute(f'select * from add_pizza(\'{name}\', (select id_user from users '
                       f'where session_id = {session}), {size}, {sauce}, (select (select * from calculate_total_cost(\'{filling}\'))*{cursor.fetchall()[0][0]}::INT+120));')
        cursor.fetchall()
        cursor.execute(f'SELECT * FROM pizza_constr ORDER BY id_pizza DESC LIMIT 1;')
        cursor.execute(f'select * from insert_fillings({cursor.fetchall()[0][0]}, \'{filling}\');')
        cursor.fetchall()

        # ОБНОВЛЕНИЕ ДАННЫХ В COOKIE -----------------------------------------------------
        # ДЛЯ КОНСТРУКТОРА
        response.delete_cookie('filling', path='/constructor')
        response.delete_cookie('sauce', path='/constructor')
        cursor.execute(f'SELECT * FROM pizza_constr ORDER BY id_pizza DESC LIMIT 1;')
        id_pizza = cursor.fetchall()[0][0]
        # ДЛЯ СПИСКА ПИЦЦ
        try:
            pizzas = request.COOKIES.get('pizzas')
            if (pizzas is not None): response.set_cookie('pizzas', f'{pizzas} {id_pizza}')
            else: raise Exception('fuck you')
        except:
            response.set_cookie('pizzas', id_pizza)
        response.set_cookie('isLoad', 'true')
        return response
    except:
        return render(request, 'constructor/order.html')


def index(request):
    fillings = doIngridients()
    return render(request, 'constructor/constructor.html', context=fillings)


def doIngridients():
    # Select all fillings
    cursor = connection.cursor()
    cursor.execute(f'select * from filling;')
    all_fillings = cursor.fetchall()

    # Making dict
    result_fillings = dict()
    for index in range(len(all_fillings)):
        result_fillings[f'{all_fillings[index][0]}'] = {'name': all_fillings[index][1],
                                  'type': all_fillings[index][2],
                                  'cost': all_fillings[index][3],
                                  'img': all_fillings[index][4]}


    cursor.execute(f'select * from sauce;')
    all_fillings = cursor.fetchall()
    result_sauces = dict()
    for index in range(len(all_fillings)):
        result_sauces[f'{all_fillings[index][0]}'] = {'name': all_fillings[index][1],
                                  'cost': all_fillings[index][2],
                                  'img': all_fillings[index][3]}

    cursor.execute(f'select * from dough;')
    all_fillings = cursor.fetchall()
    result_dough = dict()
    for index in range(len(all_fillings)):
        result_dough[f'{index}'] = {'id': all_fillings[index][0],
                                     'size': all_fillings[index][1]}

    return {'fillings': result_fillings, 'sauces': result_sauces, 'dough': result_dough}


def doOrderPizzas(idPizzas):

    cursor = connection.cursor()
    cursor.execute(f'select id_pizza from pizza_constr as pc join users as u on pc.id_user = u.id_user where session_id = 5653556479863543808;')
    numbers = cursor.fetchall()
    res = ''
    for el in numbers:
            res += f'{el[0]} '

    ids = idPizzas.split()
    result_fill = dict()
    result_sauce = dict()
    result_cost = dict()
    result_names = dict()
    result_pizza_id = dict()

    cursor = connection.cursor()
    cursor.execute(f'select id_pizza, photo_name from pizza_constr_filling as pcf join filling as f on pcf.id_filling = f.id_filling;')
    constr_pizza = cursor.fetchall()


    for i in range(0, len(ids)):
        pizza_fills = list()
        for j in range(0, len(constr_pizza)):
            if (f'{constr_pizza[j][0]}' == f'{ids[i]}'):
                pizza_fills.append(constr_pizza[j][1])


        result_fill.setdefault(i, []).extend(pizza_fills)
        pizza_fills.clear()


    for i in range(0, len(ids)):
        cursor.execute(f'select id_sauce from pizza_constr where id_pizza={ids[i]};')
        pizza_sauce = cursor.fetchall()[0][0]

        if (pizza_sauce == 2):
            result_sauce[i] = 'tomato_sauce'
        else:
            result_sauce[i] = 'cream_sauce'

    for i in range(0, len(ids)):
        cursor.execute(f'select pizza_cost from pizza_constr where id_pizza={ids[i]};')
        pizza_cost = cursor.fetchall()[0][0]
        result_cost[i] = int(pizza_cost.split(',')[0])

    for i in range(0, len(ids)):
        cursor.execute(f'select pizza_name from pizza_constr where id_pizza={ids[i]};')
        pizza_name = cursor.fetchall()[0][0]
        result_names[i] = pizza_name

    for i in range(0, len(ids)):
        cursor.execute(f'select id_pizza from pizza_constr where id_pizza={ids[i]};')
        pizza_id = cursor.fetchall()[0][0]
        result_pizza_id[i] = pizza_id


    return {'filling': result_fill, 'sauces': result_sauce, 'cost': result_cost, 'summa': sum(result_cost.values()), 'names': result_names, 'ids': result_pizza_id}