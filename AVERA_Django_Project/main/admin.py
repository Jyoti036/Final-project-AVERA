from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email","user_type","is_staff")
    search_fields = ("username","email","first_name","last_name")

for model in [Admin, CareOrganization, Child, AdoptionInformation, AwarenessContent, SuccessStory, Gift, Feedback, Wishlist, MilestoneUpdate, FAQ, Notification]:
    admin.site.register(model)
