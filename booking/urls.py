from django.urls import path
from .views import BookingListView, BookingDetailView, BookingPersonListView, BookingPersonDetailView

urlpatterns = [
    # Bookings URLs
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # Booking Persons URLs
    path('bookings/<int:pk>/persons/', BookingPersonListView.as_view(), name='booking-person-list'),
    path('bookings/persons/<int:pk>/', BookingPersonDetailView.as_view(), name='booking-person-detail'),
]
