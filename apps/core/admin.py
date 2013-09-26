from django.contrib import admin
from .models import CommonUser


class CommomUserAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Class CommomUser
    """

    list_display = ('user', 'name', 'email', 'phone', 'active')
    list_display_links = ('user', 'name')
    list_editable = ('active',)


admin.site.register(CommonUser, CommomUserAdmin)