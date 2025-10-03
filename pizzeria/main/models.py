from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dough(models.Model):
    id_dough = models.AutoField(primary_key=True)
    dough_size = models.IntegerField()
    cost_index = models.FloatField()

    class Meta:
        managed = False
        db_table = 'dough'


class Filling(models.Model):
    id_filling = models.AutoField(primary_key=True)
    filling_name = models.CharField(max_length=50)
    filling_type = models.TextField()  # This field type is a guess.
    filling_cost = models.TextField()  # This field type is a guess.
    photo_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'filling'


class Orders(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_user = models.OneToOneField('Users', models.DO_NOTHING, db_column='id_user')
    orders_cost = models.TextField()  # This field type is a guess.
    review_description = models.CharField(blank=True, null=True, max_length=500)
    review_rate = models.SmallIntegerField(blank=True, null=True)
    address = models.CharField(max_length=500)
    comment = models.CharField(blank=True, null=True, max_length=500)
    date = models.DateField()


    class Meta:
        managed = False
        db_table = 'orders'


class OrdersPizzaConstr(models.Model):
    id_order = models.OneToOneField(Orders, models.DO_NOTHING, db_column='id_order', primary_key=True)  # The composite primary key (id_order, id_pizza) found, that is not supported. The first column is selected.
    id_pizza = models.ForeignKey('PizzaConstr', models.DO_NOTHING, db_column='id_pizza')

    class Meta:
        managed = False
        db_table = 'orders_pizza_constr'
        unique_together = (('id_order', 'id_pizza'),)


class PizzaConstr(models.Model):
    id_pizza = models.AutoField(primary_key=True)
    pizza_name = models.CharField(max_length=50)
    id_user = models.OneToOneField('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    id_dough = models.OneToOneField(Dough, models.DO_NOTHING, db_column='id_dough')
    id_sauce = models.OneToOneField('Sauce', models.DO_NOTHING, db_column='id_sauce')
    pizza_cost = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'pizza_constr'


class PizzaConstrFilling(models.Model):
    id_pizza = models.OneToOneField(PizzaConstr, models.DO_NOTHING, db_column='id_pizza', primary_key=True)  # The composite primary key (id_pizza, id_filling) found, that is not supported. The first column is selected.
    id_filling = models.ForeignKey(Filling, models.DO_NOTHING, db_column='id_filling')

    class Meta:
        managed = False
        db_table = 'pizza_constr_filling'
        unique_together = (('id_pizza', 'id_filling'),)


class Sauce(models.Model):
    id_sauce = models.AutoField(primary_key=True)
    sauce_name = models.CharField(max_length=50)
    photo = models.BinaryField(blank=True, null=True)
    sauce_cost = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sauce'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    session_id = models.CharField(max_length=50)
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'users'
