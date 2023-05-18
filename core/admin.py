from django.contrib import admin
from .models import Bus ,JourneyRoot,BookTicket,CancleTicket,User
from django.contrib.admin import ModelAdmin
# Register your models here.



class UserAdmin(ModelAdmin):
        list_display = ('id', 'email', 'username', 'first_name', 'last_name' ,'profile_img','acivation_status')
        list_filter = ('is_superuser',)
        fieldsets = [
                (None, {'fields': ('email', 'password',)}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'username','profile_img','acivation_status',)}),
                ('Permissions', {'fields': ('is_superuser',)}),
        ]

        add_fieldsets = (
                (None, {
                        'classes': ('wide',),
                        'fields': ( 'is_student','profile_img','acivation_status'),
                }),
        )
        search_fields = ('username',)
        ordering = ('id',)
        filter_horizontal = ()


admin.site.register(User, UserAdmin)



    


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ["bus_seat", "bus_type", "bus_category", "bus_number", "bus_name"][::-1]


@admin.register(JourneyRoot)
class JourneyRootAdmin(admin.ModelAdmin):
    list_display = ['Buses','via','duration','arrival_time','arrival_date','departure_time','departure_date','price','one_kilometer_price','kilometer', "end_point", "start_point"][::-1]





@admin.register(CancleTicket)
class CancleTicketAdmin(admin.ModelAdmin):
    list_display = ["cancle_bus", "user"][::-1]





@admin.register(BookTicket)
class BookTicketAdmin(admin.ModelAdmin):
    list_display = ['duration','arrival_time','departure_time',"book_date_time", "address", "phone", "fare", "seats","slected_seat", "journey", "bus", "user"][::-1]
