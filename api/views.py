from django.shortcuts import render
from rest_framework.views import APIView
from core.models import *
from api.serializers import *
from rest_framework.response import Response
from dateutil import parser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
import string
from rest_framework.permissions import AllowAny
import random
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken,TokenError
from rest_framework_simplejwt.settings import api_settings


class CreateUserView(generics.GenericAPIView):                  
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser :
            user = serializer.save()
            if request.data.get('is_staff'):
                user.is_staff = True
                user.save()
            if request.data.get('is_superuser'):
                user.is_superuser = True
                user.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
            })
        else:
            return Response("Only admin can create Staff or admin user...",400)

    def get(self, request):
        if request.user.is_superuser:
            if "id" in request.data:
                try:
                    user = User.objects.get(id=request.data['id'])
                    serializer = UserSerializer(instance=user)
                    return Response(serializer.data)
                except User.DoesNotExist:
                    return Response("User not found.", 400)
            else:
                try:
                    user = User.objects.all()
                    serializer = UserSerializer(instance=user,many=True)
                    return Response(serializer.data)
                except User.DoesNotExist:
                    return Response("User not found.", 400)

        else:
            return Response("Only admin users can retrieve user data.")

    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                user = User.objects.get(id=id)
                user.delete()
                return Response("Success")
            except User.DoesNotExist:
                return Response("user not found")
        else:
            return Response("Only Admin can delete the data")

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    token_class = RefreshToken
    def validate(self, attrs):
        data = super().validate(attrs)
        expiration_time = datetime.now() + timedelta(minutes=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        refresh = self.get_token(self.user)
        refresh.access_token.set_exp(expiration_time)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

class BusApi(APIView):
    def post(self,request):
        if request.user.is_superuser or request.user.is_staff:
                serilizer=BusSerializers(data=request.data)
                if serilizer.is_valid():
                    serilizer.save()
                    return Response(serilizer.data)
                else:
                    return Response("Invalid Data",400)
        else:
            return Response("Only Admin or Staff User can add the bus.")    

    def get(self,request):
        if request.user.is_superuser:
                bus=Bus.objects.all()
                serilizer=BusSerializers(instance=bus,many=True)
                return Response(serilizer.data) 
        else:
            return Response("Only Admin can show the data.")        
      

    def put(self,request,id):
        if request.user.is_superuser:
            try:
                bus=Bus.objects.get(id=id)
                serilizer=UpdateBusSerializers(data=request.data, instance=bus, partial=True)
                if serilizer.is_valid():
                    serilizer.save()
                    return Response(serilizer.data,200) 
            except Bus.DoesNotExist:
                return Response("Bus not found")
        else:
            return Response("Only Admin can update data.")

    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                bus = Bus.objects.get(id=id)
                bus.delete()
                return Response("Success")
            except Bus.DoesNotExist:
                return Response("Bus not found")    
        else:
            return Response("Only Admin can delete the data")

class  JourneyRootApi(APIView):
    def post(self,request):
        if request.user.is_superuser or request.user.is_staff:
            price=int(request.data['kilometer'])*int(request.data['one_kilometer_price'])
            departure_datetime_str = parser.parse(f"{request.data['departure_date']} {request.data['departure_time']}")
            arrival_datetime_str = parser.parse(f"{request.data['arrival_date']} {request.data['arrival_time']}")
            duration = arrival_datetime_str - departure_datetime_str

            serializer = JourneyRootSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(price=price, duration=str(duration))
            return Response({"success": serializer.data})
        else:
            return Response("only superuser or staffuser can add the data..",400)
            
            
    def get(self,request):
        if request.user.is_superuser:
            root=JourneyRoot.objects.all()
            serilizer=JourneyRootSerializer(instance=root,many=True)
            return Response(serilizer.data)
        else:
            return Response("only superuser can get the data..",400)


    def put(self,request,id):
        if request.user.is_superuser:
            try:
                price=int(request.data['kilometer'])*int(request.data['one_kilometer_price'])
                departure_datetime_str = parser.parse(f"{request.data['departure_date']} {request.data['departure_time']}")
                arrival_datetime_str = parser.parse(f"{request.data['arrival_date']} {request.data['arrival_time']}")
                duration = arrival_datetime_str - departure_datetime_str
                root=JourneyRoot.objects.get(id=id)
                serializer = UpdateJourneyRootSerializer(data=request.data,instance=root, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(price=price, duration=str(duration))
                    return Response({"success": serializer.data})
                else:
                    return Response("Inavlid Data",400)
            except JourneyRoot.DoesNotExist:
                return Response("Root not found")
        else:
            return Response("only superuser can update the data..",400)


    def delete(self,request,id):
        if request.user.is_superuser:
            try:
                root = JourneyRoot.objects.get(id=id)
                root.delete()
                return Response("Success")
            except JourneyRoot.DoesNotExist:
                return Response("Root not found")
        else:
            return Response("only superuser can delete the data..",400)
    
class BookBusApi(APIView):
    def post(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return Response("Only common users can add the data.", 400  )
        
        total_seats = eval(request.data["slected_seat"])
        # selected_seat_str = ",".join(str(seat) for seat in total_seats)
        journey_id = request.data.get("journey")
        journey = JourneyRoot.objects.get(id=journey_id)
        departure_datetime_str = parser.parse(f"{journey.departure_date} {journey.departure_time}")
        arrival_datetime_str = parser.parse(f"{journey.arrival_date} {journey.arrival_time}")
        duration = arrival_datetime_str - departure_datetime_str
        
        bus=journey.bus.get()
        print(bus)
        available_seats = bus.bus_seat
        for i in total_seats:
            if i > int(available_seats):
                return Response("Seats are not availabe")

        booked_seats = BookTicket.objects.filter(journey=journey).values_list('slected_seat', flat=True)
        already_booked_seats = [int(seat) for seats in booked_seats for seat in seats.split(',')]
        if any(seat in already_booked_seats for seat in total_seats):
            return Response("These seats are already booked")
        serializer = BookTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                bus=bus,
                seats=len(total_seats),
                slected_seat=total_seats,
                departure_time=str(departure_datetime_str),
                arrival_time=str(arrival_datetime_str), 
                duration=str(duration),
                fare=float(journey.price) * len(total_seats)
            )
            return Response({"success": serializer.data})
        else:
            return Response({"Error": serializer.errors}, 400)


    def get(self,request):
        if request.user.is_superuser==False and request.user.is_staff==False:
            root=BookTicket.objects.all()
            serilizer=BookTicketSerializer(instance=root,many=True)
            return Response(serilizer.data)
        else:
            return Response("only common-user can get the data..",400)


    def put(self,request,id):
        if request.user.is_superuser==False and request.user.is_staff==False:
            try:
                total_seats = eval(request.data["slected_seat"])
                journey_id = request.data.get("journey")
                journey = JourneyRoot.objects.get(id=journey_id)
                departure_datetime_str = parser.parse(f"{journey.departure_date} {journey.departure_time}")
                arrival_datetime_str = parser.parse(f"{journey.arrival_date} {journey.arrival_time}")
                duration = arrival_datetime_str - departure_datetime_str
                
                bus=journey.bus.get()
                user = request.user
                price = float(journey.price)
                seats = len(total_seats)
                fare = price * seats

                root=BookTicket.objects.get(id=id)
                booked_seats = BookTicket.objects.filter(journey=journey).values_list('slected_seat', flat=True)
                already_booked_seats = [int(seat) for seats in booked_seats for seat in seats.split(',')]
                if any(seat in already_booked_seats for seat in total_seats):
                    return Response("These seats are already booked")
                serializer = UpdateBookTicketSerializer(data=request.data,instance=root, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(
                        user=user,
                        bus=bus,
                        seats=str(seats),
                        slected_seat=str(request.data['slected_seat']),
                        departure_time=str(departure_datetime_str),
                        arrival_time=str(arrival_datetime_str),
                        duration=str(duration),
                        fare=str(fare)
                    )
                    return Response({"sucess":serializer.data})
                else:
                    return Response({"Error":serializer.errors})
            except BookTicket.DoesNotExist:
                return Response("root  not found")
        else:
            return Response("only common user can update the data...",400)
    
    def delete(self,request,id):
        if request.user.is_superuser==False and request.user.is_staff==False:
            try:
                ticket = BookTicket.objects.get(id=id)
                ticket.delete()
                return Response("Success")
            except BookTicket.DoesNotExist:
                return Response("Ticket not found")
        else:
            return Response("only common user can delete the data...",400)
        
class SearchBusApi(APIView):
    def post(self,request):
        start_point = request.data.get('start_point')
        end_point = request.data.get('end_point')
        departure_date = request.data.get('departure_date')
        try:
            datetime.strptime(departure_date, '%Y-%m-%d')
        except ValueError:
            return Response("Invalid date format. Use YYYY-MM-DD.", 400)
        availble_bus=JourneyRoot.objects.filter(start_point=start_point,end_point=end_point,departure_date=departure_date)
        if availble_bus:
            serializer=BusSearchSerializer(availble_bus,many=True)
            journey_id = availble_bus.last().id 
            return Response({"data":serializer.data,"journey_id": journey_id})
        else:                                                                                           
            return Response("Bus Not Found...",400)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'detail': 'Invalid old password'}, 400)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password successfully changed'},400)
        return Response(serializer.errors, 400)
    
class SendPasswordResetLinkView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        user = User.objects.filter(email=request.data['email'], username = request.data['username']).first()
        print('user: ', user)
        if user:
            N = 7
            tempass = str(''.join(random.choices(string.ascii_letters, k=N)))
            user.set_password(tempass)
            user.save()
            message = get_template("mail.html").render({
                
                "Temprory_password":tempass,
            })
            mail = EmailMessage(
                subject="Temprory Password Information",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[request.data['email']],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=False)
            return Response({"Success":f"Mail sending on this mail is: {request.data['email']}"})    
        else:
            return Response({"Error":f"User Not availble"})

  