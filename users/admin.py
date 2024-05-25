from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, ShopOwner, Tourguide, UserPro


class CustomUserAdmin(UserAdmin):
    # Define the common fields for all user types
    list_display = ['username', 'email', 'phone_number', 'address', 'date_joined', 'is_active']
    search_fields = ['username', 'email', 'phone_number', 'address']
    list_filter = ['date_joined', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number', 'address')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'address', 'password1', 'password2'),
        }),
    )

class UserProAdmin(CustomUserAdmin):
    model = UserPro
    filter_horizontal = []  # Remove 'groups' and 'user_permissions'

class CustomerAdmin(CustomUserAdmin):
    model = Customer
    filter_horizontal = []  # Remove 'groups' and 'user_permissions'

class DeliveryBoyAdmin(CustomUserAdmin):
    model = Tourguide
    
    filter_horizontal = []  # Remove 'groups' and 'user_permissions'

class ShopOwnerAdmin(CustomUserAdmin):
    model = ShopOwner
    filter_horizontal = []  # Remove 'groups' and 'user_permissions'

# Register the models with their respective admin classes
admin.site.register(UserPro, UserProAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Tourguide, DeliveryBoyAdmin)
admin.site.register(ShopOwner, ShopOwnerAdmin)