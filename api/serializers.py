from rest_framework import serializers
from core.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class BusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Bus
        fields=['bus_name','bus_number','bus_category','bus_type','bus_seat']

class UpdateBusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Bus
        fields=['bus_name','bus_number','bus_category','bus_type','bus_seat']



class JourneyRootSerializer(serializers.ModelSerializer):
    class Meta:
        model=JourneyRoot
        fields=['start_point','end_point','kilometer','one_kilometer_price','price','departure_date','departure_time','arrival_date',
                'arrival_time','duration','via','bus']
        
class UpdateJourneyRootSerializer(serializers.ModelSerializer):
    class Meta:
        model=JourneyRoot
        fields=['start_point','end_point','kilometer','one_kilometer_price','price','departure_date','departure_time','arrival_date',
                'arrival_time','duration','via','bus']


class BookTicketSerializer(serializers.ModelSerializer):
    journey = serializers.PrimaryKeyRelatedField(queryset=JourneyRoot.objects.all())

    class Meta:
        model = BookTicket
        fields = ['user', 'bus', 'journey', 'seats', 'slected_seat', 'fare', 'phone', 'address', 'book_date_time', 'departure_time', 'arrival_time', 'duration']



class UpdateBookTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookTicket
        fields=['user','bus','journey','seats','slected_seat','fare','phone','address','book_date_time','departure_time','arrival_time'
                ,'duration']
        

        
class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

class BusSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Bus
        fields=['id','bus_name','bus_type']

class BusSearchSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    bus = serializers.SerializerMethodField()

    class Meta:
        model=JourneyRoot
        fields=['id','start_point','end_point','departure_date','arrival_time', 'duration', 'bus']


    def get_id(self, obj):
        return f"{obj.id}"
    
    def get_bus(self, obj):
        bus_serializer = BusSerializer1(obj.bus.all(), many=True)
        return bus_serializer.data


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

