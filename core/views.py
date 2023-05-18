from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import User,Bus,JourneyRoot,BookTicket
from .form import ProfileDetails,AdminUpdate,StaffUpdate,BusListUpdateForm,CommonUserUpdate
from django.contrib.auth.decorators import login_required,permission_required
from .constants import *
from django.views.generic import TemplateView, View,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.decorators import method_decorator
import json
import ast
from pathlib import Path
from django.urls import reverse
data_file_path = Path(__file__).parent / "static/json/city.json"
f=open(data_file_path)
all_city=[]
data=json.load(f)
for j in data:  
    all_city.append(j['name'])
f.close()


class HomeView(TemplateView):
    template_name = 'index.html'
    success_url = reverse_lazy('home')

class LoginView(View):
    
    def get(self,request):
        return render(request,"auth-login-basic.html")

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        check_user = authenticate(username=username, password=password)
        if check_user:
            login(request, check_user)
            messages.success(request,"login successfully..........")  
            return redirect('home')
        else:
            messages.info(request,ALL_FIELD)
            return redirect("login1")
        
class MainRegister(View):
    def get(self,request):
        if request.user.is_superuser:
            return render(request,"main_register.html")
        else:
            return render(request,"main_register.html")


    def post(self,request):
    
            if request.POST['role'] == 'admin':
                if request.POST['password'] ==  request.POST['confirmpassword']: 
                    usr=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['firstname'],last_name=request.POST['lastname'],is_staff=False,is_superuser=True)
                    usr.set_password(request.POST['password'])
                    usr.save()  
                    messages.success(request,"Admin User created successfully....")  
                    return redirect("register1")
                else:
                    messages.info(request,"Password Does Not Match....")  
                    return redirect("register1")
            else:
                if request.POST['password'] ==  request.POST['confirmpassword']: 
                    usr=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['firstname'],last_name=request.POST['lastname'],is_staff=True,is_superuser=False)
                    usr.set_password(request.POST['password'])
                    usr.save()
                    messages.success(request,"Staff User created successfully....")  
                    return redirect("register1")
                else:
                    messages.info(request,"Password Does Not Match....")  
                    return redirect("register1")
            # else:
                  
class MainForgetPassword(View):
    def get(self,request):
      return render(request,"main_forget_password.html")
    
class Account(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            profile=User.objects.get(id=id)
            form=ProfileDetails(instance=profile)
            return render(request,"pages-account-settings-account.html",{"form":form})
        else:
            return redirect('login1')         
    def post(self,request,id):
        try:
            profile = User.objects.get(id=id)
            form=ProfileDetails(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                messages.success(request,"Account Detais Updated successfully....")  
                form.save()
                return redirect("home")
        except:
             print("Invalid Input........!!")

class Register(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,"auth-register-basic.html")
        else:
            return redirect('login1')
  
    def post(self,request):
            if request.POST['role'] == 'admin':
                if request.POST['username'] and request.POST['email'] and request.POST['firstname'] and request.POST['lastname'] and request.POST['password'] is not None:
                    usr=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['firstname']
                                                 ,last_name=request.POST['lastname'],is_staff=False,is_superuser=True)
                    usr.set_password(request.POST['password'])
                    if request.POST['password'] ==  request.POST['confirmpassword']: 
                        usr.save()  
                        messages.success(request,"Admin User created successfully....")  
                        return redirect("register")
                    else:
                        messages.info(request,"Password Does Not Match....")  
                        return redirect("register")
                else:
                    messages.info(request,ALL_FIELD)  
                    return redirect("register")
               
            else:
                if request.POST['username'] and request.POST['email'] and request.POST['firstname'] and request.POST['lastname'] and request.POST['password'] is not None:
                    usr=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['firstname'],last_name=request.POST['lastname'],is_staff=True,is_superuser=False)
                    usr.set_password(request.POST['password'])
                    if request.POST['password'] ==  request.POST['confirmpassword']: 
                        usr.save()
                        messages.success(request,"Staff User created successfully....")  
                        return redirect("register")
                    else:
                        messages.info(request,"Password Does Not Match....")  
                        return redirect("register")
                else:
                    messages.info(request,ALL_FIELD)  
                    return redirect("register")
      
class ChangePassword(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,"auth-change-password-basic.html")
        else:
            return redirect('login1')

    def post(self,request):
            password=request.POST['password']
            newpassword=request.POST['newpassword']
            confirmnewpassword=request.POST['confirmnewpassword']

            if not password or not newpassword or not confirmnewpassword:
                messages.info(request, ALL_FIELD)
                return redirect("change_password")

            usr= User.objects.get(id=request.user.id)
            pass_check = usr.check_password(password)
            if pass_check and newpassword==confirmnewpassword:
                        usr.set_password(newpassword)
                        usr.save()
                        messages.success(request,PASSWORD_SUCCESS)      
                        return redirect("login1")
            else:
                    messages.info(request,"Password Does Not Match....")
                    return redirect("change_password")
          
def logout1(request):
    try:
        del request.session['user']
    except:
        return redirect('login1')
    return redirect('login1')

class BusAdd(View):
    def get(self,request):
        if request.user.is_authenticated:
                return render(request,"form-layouts-horizontal.html")
        else:
            return redirect('login1')
    
    def post(self,request):
        try:
                bus_name=request.POST['bus_name']
                bus_number=request.POST['bus_number']
                bus_category=request.POST['bus_category']
                bus_type=request.POST['bus_type']
                bus_seat=request.POST['bus_seat']
                if bus_name and bus_number and bus_category and bus_type and bus_seat is not None:
                    bus=Bus(bus_name=bus_name,bus_number=bus_number,bus_category=bus_category,bus_type=bus_type,bus_seat=bus_seat)
                    messages.success(request,"Bus Added Successfully......")
                    bus.save()
                    return redirect("form1")
                else:
                    messages.info(request,ALL_FIELD)  
                    return redirect("form1")
        except:
             print("Invalid Input........!!")
    
class JourneyAdd(View):
    def get(self,request):
        if request.user.is_authenticated:
            all_bus=Bus.objects.all()
            return render(request,"journey_root.html",{"all_bus":all_bus,"city":all_city})
        else:
            return redirect('login1')
        
    def post(self,request):
        try:
            start_point=request.POST['start_point']
            end_point=request.POST['end_point']
            buses=request.POST.getlist('bus')
            kilometer=request.POST['kilometer']
            one_kilometer_price=request.POST['one_kilometer_price']
            price=request.POST['price']
            departure_date=request.POST['departure_date']
            departure_time=request.POST['departure_time']
            arrival_date=request.POST['arrival_date']
            arrival_time=request.POST['arrival_time']
            duration=request.POST['duration']
            via=request.POST['via']
            # for i in buses:
            #     bus=Bus.objects.get(id=i)
            #     bus.bus_status = False
            #     bus.save()
            if start_point and end_point and buses and kilometer and one_kilometer_price and price and departure_date and departure_time and departure_time and arrival_date and arrival_time and duration and via is not None:
                Journey=JourneyRoot.objects.create(start_point=start_point,end_point=end_point,kilometer=kilometer,one_kilometer_price=one_kilometer_price,price=price
                                                   ,departure_date=departure_date,departure_time=departure_time,arrival_date=arrival_date,arrival_time=arrival_time,
                                                   via=via,duration=duration)
                Journey.bus.add(*buses)
                Journey.save()    
                messages.success(request,"Journeyroot Added Successfully......")
                return redirect('form2')
            else:
                messages.info(request,ALL_FIELD)
                return redirect('form2')
        except:
             print("Invalid Input........!!")

class AdminUserList(View):
    def get(self,request):
        if request.user.is_authenticated:
            admin_usr=User.objects.filter(is_superuser=True)
            return render(request,"register_admin_user_list.html",{"admin_usr":admin_usr})        
        else:
            return redirect('login1')

class StaffUserList(View):
    def get(self,request):
        if request.user.is_authenticated:
            staff_usr=User.objects.filter(is_staff=True , is_superuser=False)
            return render(request,"register_staff_user_list.html",{"staff_usr":staff_usr})
        else:
            return redirect("login1")

class CommonUserList(View):
    def get(self,request):
        if request.user.is_superuser:
            
            common_usr=User.objects.filter(is_staff=False , is_superuser=False)
            return render(request,"common_user_list.html",{"staff_usr":common_usr})
        else:
            return redirect("login1")
        
class BusList(View):
    def get(self,request):
        if request.user.is_authenticated:
            all_bus=Bus.objects.all()
            return render(request,"bus_list.html",{'all_bus':all_bus})
        else:
            return redirect("login1")

class JourneyRootList(View):
    def get(self,request):
        if request.user.is_authenticated:
            list=[]
            all_journey=JourneyRoot.objects.all()
            for i in all_journey:
                for j in i.bus.all():
                    list.append(j.bus_name)
            return render(request,"journey_root_list.html",{'all_journey':all_journey,'bus':list})
        else:
            return redirect("login1")

class TicketDetailsAdmin(View):
    def get(self,request):
        if request.user.is_authenticated:
            all_ticket=BookTicket.objects.all()
            return render(request,"bookinglist.html",{'all_ticket':all_ticket})
        else:
            return redirect("login1")
        
class AdminDetailsUpdate(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            admin=User.objects.get(id=id)
            form=AdminUpdate(instance=admin)
            return render(request,"admin_details_update.html",{"forms":form})
        else:
            return redirect("login1")
    
    def post(self,request,id):
        try:
            admin=User.objects.get(id=id)
            form=AdminUpdate(request.POST,instance=admin)
            if form.is_valid():
                form.save()
                messages.success(request,"Admin User Updated successfully....")  
                return redirect("admin_list")
        except:
             print("Invalid Input........!!")
    
class StaffDetailsUpdate(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            staff=User.objects.get(id=id)
            form=StaffUpdate(instance=staff)
            return render(request,"staff_details_update.html",{'forms':form})
        else:
            return redirect("login1")
   
    def post(self,request,id):
        try:
            staff=User.objects.get(id=id)
            form=StaffUpdate(request.POST,instance=staff)
            if form.is_valid():
                form.save()
                messages.success(request,"Staff User Updated successfully....")  
                return redirect("staff_list")
        except:
             print("Invalid Input........!!")

class BusListUpdate(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            bus1=Bus.objects.get(id=id)
            form=BusListUpdateForm(instance=bus1)
            return render(request,"bus_list_update.html",{"forms":form})      
        else:
            return redirect("login1")
        
    def post(self,request,id):
        try:
            bus1=Bus.objects.get(id=id)
            form=BusListUpdateForm(request.POST,instance=bus1)
            if form.is_valid():
                form.save()
                messages.success(request,"Bus Details Updated successfully....")  
                return redirect("bus_list")
        except:
             print("Invalid Input........!!")
    
class JourneyListUpdate(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            list=[]   
            journey=JourneyRoot.objects.get(id=id)
            bus=Bus.objects.filter(bus_status=True)
            for j in journey.bus.all():
                list.append(j.id)
            return render(request,"journey_root_list_update.html",{"journey":journey,"buses":bus,"buslist":list,"city":all_city})
        else:
            return redirect("login1")
    def post(self,request,id):
        try:
            journey_data=JourneyRoot.objects.get(id=id)
            if journey_data:  
                if request.POST['start_point'] != 'startpoint' and request.POST['end_point'] != 'endpoint':  
                    if request.POST['start_point'] != request.POST['end_point'] :   
                        journey_data.start_point=request.POST['start_point'] 
                        journey_data.end_point=request.POST['end_point']
                        journey_data.kilometer=request.POST['kilometer']
                        journey_data.one_kilometer_price=request.POST['one_kilometer_price']
                        journey_data.price=request.POST['price']
                        journey_data.via=request.POST['via']
                        journey_data.departure_date=request.POST['departure_date']
                        journey_data.departure_time=request.POST['departure_time']
                        journey_data.arrival_date=request.POST['arrival_date']
                        journey_data.arrival_time=request.POST['arrival_time']
                        journey_data.duration=request.POST['duration']
                        buses=request.POST.getlist('bus')              
                        for i in journey_data.bus.all():
                            journey_data.bus.remove(i)
                        journey_data.bus.add(*buses)
                        journey_data.save()   
                        messages.success(request,"Bus Details Updated successfully....")  
                        return redirect("journey_root_list")
                    else:
                        messages.info(request,"Please Enter Valid Destination....")  
                        return redirect("journey_root_list_update",id=id) 

                else:
                    messages.info(request,"Please Enter Valid Destination....")  
                    return redirect("journey_root_list_update",id=id)     

            else:
                messages.info(request,"Bus Details not Found....")  
                return redirect("journey_root_list_update",id=id)
        except:
             print("Invalid Input........!!")
   
class DeleteProfile(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            usr_id=User.objects.get(id=id)
            usr_id.delete()
            messages.success(request,"User Deleted Successfully")
            return redirect("home")
        else:
             return redirect("login1")
        
class BusDetailsDelete(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            u=Bus.objects.get(id=id)
            u.delete()
            messages.success(request,"Bus  list detete successfully....")  
            return redirect('bus_list')
        else:
             return redirect("login1")
        
class JourneyRootDeleteList(View):
    def get(self,request,id):
        if request.user.is_authenticated:

            delete_journey=JourneyRoot.objects.get(id=id)
            for i in delete_journey.bus.all():
                bus=Bus.objects.get(id=i.id)
                bus.bus_status = True
                bus.save() 
            delete_journey.delete()
            messages.success(request,"journey root list detete successfully....")  
            return redirect('journey_root_list')
        else:
             return redirect("login1")
    
class CommonUserRegister(View):
    def get(self,request):
        return render(request,'common_user_register.html')
    def post(self,request):
        if request.POST['username'] and request.POST['email'] and request.POST['firstname'] and request.POST['lastname'] and request.POST['password'] is not None:
            if request.POST['password'] ==  request.POST['confirmpassword']: 
                usr=User.objects.create_user(username=request.POST['username'],email=request.POST['email'],first_name=request.POST['firstname'],
                                             last_name=request.POST['lastname'],is_staff=False,is_superuser=False)
                usr.set_password(request.POST['password'])
                usr.save()
                messages.success(request,"Registrations successfully....")  
                return redirect("user-register")
            else:
                messages.info(request,"Password Does Not Match....")  
                return redirect("user-register")
        else:
            messages.info(request,ALL_FIELD)  
            return redirect("user-register")
       
class CommonUserUpdate1(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            admin=User.objects.get(id=id)
            form=CommonUserUpdate(instance=admin)
            return render(request,"common_user_update.html",{"forms":form})
        else:
            return redirect("login1")
    
    def post(self,request,id):
        try:
            admin=User.objects.get(id=id)
            form=CommonUserUpdate(request.POST,instance=admin)
            if form.is_valid():
                form.save()
                messages.success(request,"Common User Updated successfully....")  
                return redirect("common-user-list")
        except:
             print("Invalid Input........!!")

class BusBook(View):
    def get(self, request, id):
        all_bus = Bus.objects.filter(id=id)
        selected_seats = request.GET.getlist('selected_seat')
        seat_list1 = [int(seat) for seat in selected_seats[0].split(',')]
        seat_list = selected_seats[0].split(',')
        seat=len(seat_list)
        fare = []
        for root in all_bus:
            bus = root.buses.all().values()
            for j in bus.values('price'):
                fare.append(j)
        one_seat_price = int(fare[0]['price'])
        total = one_seat_price * (seat)
        context = {'all_bus': all_bus, 'selected_seats': seat_list1,'bus':bus,'seat_list':len(seat_list), 'total': total}
        return render(request, "book_ticket.html", context)

    def post(self,request,id):
        user=User.objects.get(username=request.POST['user'])
        if user:
            bus=Bus.objects.get(bus_name=request.POST['bus'])
            journey=request.POST['journey']
            seats=request.POST['seats']
            fare=request.POST['fare']
            phone=request.POST['phone']
            address=request.POST['address']
            book_date_time=request.POST['book_date_time']
            departure_time=request.POST['departure_time']
            arrival_time=request.POST['arrival_time']
            duration=request.POST['duration']
            slected_seat=request.POST['slected_seat']

            
            ticket=BookTicket.objects.create(user=user,bus=bus,journey=journey,seats=seats,fare=fare,phone=phone,address=address,book_date_time=book_date_time,
                            departure_time=departure_time,arrival_time=arrival_time,duration=duration,slected_seat=slected_seat)
            ticket.save()
            messages.success(request,"Ticket book succesfully... ")
            return redirect("home")
        else:
            messages.info(request,"user not found... ")
            return redirect("home")

class SearchBus(View):
    def get(self,request):
        if request.user.is_staff is False and  request.user.is_superuser is False:            
            return render(request,"searchbus.html",{'all_city':all_city})
        else:
            return redirect("login1")
    def post(self,request):
            start_point=request.POST['start_point']
            end_point=request.POST['end_point']
            departure_date=request.POST['departure_date']
            if start_point and end_point and departure_date is not None:
                avilable_bus=JourneyRoot.objects.filter(start_point = start_point,end_point = end_point,departure_date =departure_date).values()
                l1=[list(avilable_bus)]
                for i in l1[0]:
                    all_journey = JourneyRoot.objects.get(id=i["id"]).bus.values()
                    bus_type = list(all_journey)                
                    i["buses"] = bus_type
                if avilable_bus:
                    return render(request,"searchbus.html",{'all_bus':l1})
                else:
                    messages.info(request,"Bus is not available")
                    return redirect('search_bus')
            else:
                messages.info(request,ALL_FIELD)
                return redirect('search_bus')
            
class Seat(View):
        def get(self, request,id):
            bus = Bus.objects.get(id=id)
            seat=int(bus.bus_seat)
            selectseat=[]
            selected_seat=BookTicket.objects.filter(bus__bus_name=bus)
            for i in selected_seat.values('slected_seat'):
                seat_list=ast.literal_eval(i['slected_seat'])  
                selectseat.extend(seat_list)
            sequence = []
            for i in range(1, seat+1):
                sequence.append(i)
            context = {
                'l1': seat,
                'sequence': sequence,
                'id':id,
                'selected_seat':selectseat
            }
            return render(request, "seat.html", context)
        def post(self,request,id):
            selected_seats = request.POST.getlist('selected_seats')
            url = reverse('bookbus', kwargs={'id': id}) + f'?selected_seat={",".join(selected_seats)}'
            return redirect(url)
        
class TicketDetails(View):
    def get(self,request):
        ticket=BookTicket.objects.all()
        return render(request,"show_ticket_details.html",{"ticket":ticket})
    
def DeleteTicket(request,id):
    if request.user.is_authenticated:
            u=BookTicket.objects.get(id=id)
            u.delete()
            messages.success(request,"Bus ticket cancle successfully....")  
            return redirect('ticket_details')
    else:
            return redirect("login1")
