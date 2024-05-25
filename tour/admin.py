# tours/admin.py
from django.contrib import admin

from .models import Coupon, Image, Itinerary, Tour, TourAvailability


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class TourAvailabilityInline(admin.TabularInline):
    model = TourAvailability
    extra = 1

class CouponInline(admin.TabularInline):
    model = Coupon
    extra = 1

class TourAdmin(admin.ModelAdmin):
    inlines = [ItineraryInline, ImageInline, TourAvailabilityInline, CouponInline]

admin.site.register(Tour, TourAdmin)