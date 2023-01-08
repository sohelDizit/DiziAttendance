from django.contrib import admin
from .models import Category,Person,GuestEntry,Entry,DeviceRegister,CardNumber

class CardCardInline(admin.TabularInline):
    model = CardNumber
    readonly_fields = ('id', )
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines   = [CardCardInline]


admin.site.register(Category)
admin.site.register(Person,PersonAdmin)
# admin.site.register(Person)
admin.site.register(GuestEntry)
admin.site.register(Entry)
admin.site.register(DeviceRegister)
admin.site.register(CardNumber)