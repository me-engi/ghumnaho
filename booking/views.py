from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Booking, BookingPerson
from .serializers import (BookingCreateSerializer, BookingDetailSerializer,
                          BookingPersonSerializer)


class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer

class BookingPersonListView(generics.ListCreateAPIView):
    queryset = BookingPerson.objects.all()
    serializer_class = BookingPersonSerializer

    def get_queryset(self):
        booking_id = self.kwargs.get('pk')
        return BookingPerson.objects.filter(booking_id=booking_id)

    def create(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')  # Adjust the key according to your data
        if booking_id is None:
            return Response({"error": "Booking ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        print(request.data)

        request.data['booking'] = booking.id
        serializer = BookingPersonSerializer(data=request.data, context={'booking': booking})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




class BookingPersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingPerson.objects.all()
    serializer_class = BookingPersonSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
