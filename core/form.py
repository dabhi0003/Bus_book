from django import forms
from .models import User,Bus,JourneyRoot

class ProfileDetails(forms.ModelForm):
    class Meta:
        model=User
        fields=['profile_img','first_name','last_name','email','username',]  

        
class AdminUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        } 

class CommonUserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }     

class StaffUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BusListUpdateForm(forms.ModelForm):
    class Meta:
        model=Bus
        fields=['bus_name','bus_number','bus_category','bus_type','bus_seat']
        widgets = {
            'bus_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bus_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bus_category': forms.TextInput(attrs={'class': 'form-control'}),
            'bus_type': forms.TextInput(attrs={'class': 'form-control'}),
            'bus_seat': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class JourneyListUpdate(forms.ModelForm):
#     class Meta:
#         model=JourneyRoot
#         fields=['start_point','end_point','kilometer','one_kilometer_price','price','bus']
#         widgets = {
#             'start_point': forms.TextInput(attrs={'class': 'form-control'}),
#             'end_point': forms.TextInput(attrs={'class': 'form-control'}),
#             'kilometer': forms.TextInput(attrs={'class': 'form-control'}),
#             'one_kilometer_price': forms.TextInput(attrs={'class': 'form-control'}),
#             'price': forms.TextInput(attrs={'class': 'form-control'}),
#             'bus': forms.TextInput(attrs={'class': 'form-control','multiple':'multiple'}),
#         }


    