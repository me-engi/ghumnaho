from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.models import Permission as AuthPermission
from django.db import models


class UserPro(AbstractUser):
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    groups = models.ManyToManyField(
        AuthGroup,
        through='UserGroup',
        related_name='users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        AuthPermission,
        through='UserPermission',
        related_name='users',
        blank=True,
    )

class Customer(UserPro):
    pass

class Tourguide(UserPro):
    pass

class ShopOwner(UserPro):
    pass

class UserGroup(models.Model):
    user = models.ForeignKey(UserPro, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(UserPro, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)