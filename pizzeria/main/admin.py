from django.contrib import admin
from .models import Filling, Dough, PizzaConstr, Users, Orders, Sauce, PizzaConstrFilling, OrdersPizzaConstr

# Register your models here.

admin.site.register(Filling)
admin.site.register(Dough)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(PizzaConstr)
admin.site.register(Sauce)

admin.site.register(OrdersPizzaConstr)
admin.site.register(PizzaConstrFilling)
