from django.contrib import admin
from .models import Booking, BookingPerson, PaymentStatus

class BookingPersonInline(admin.TabularInline):
    model = BookingPerson
    extra = 1

class PaymentStatusInline(admin.StackedInline):
    model = PaymentStatus

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'total_travelers', 'payment_status', 'pay_total_amount')
    search_fields = ('tour__name',)
    list_filter = ('total_travelers', 'payment_status')
    inlines = [BookingPersonInline, PaymentStatusInline]

@admin.register(BookingPerson)
class BookingPersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'traveler_number', 'traveler_name', 'phone_number', 'email')
    search_fields = ('booking__tour__name', 'traveler_name', 'phone_number', 'email')
    list_filter = ('booking__total_travelers',)

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'payment_successful')
    search_fields = ('booking__tour__name',)
    list_filter = ('payment_successful',)
