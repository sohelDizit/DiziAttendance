from django.contrib import admin
from .models import Category,Person,GuestEntry,Entry,DeviceRegister,CardNumber

class CardCardInline(admin.TabularInline):
    model = CardNumber
    readonly_fields = ('id', )
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines   = [CardCardInline]
    readonly_fields = ['img_preview']
    list_display = ['Name','MemberNumber','Relation','organisation','StartDate']
    fields=('img_preview','Image','Name','MemberNumber','organisation','StartDate','Relation','Max_guest_allowed','Categorys','Details',)

    
admin.site.register(Category)
admin.site.register(Person,PersonAdmin)
# admin.site.register(Person)
# admin.site.register(GuestEntry)
# admin.site.register(Entry)
admin.site.register(DeviceRegister)
admin.site.register(CardNumber)