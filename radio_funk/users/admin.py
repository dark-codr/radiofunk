from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from radio_funk.users.forms import UserAdminChangeForm, UserAdminCreationForm

from .models import Settings, Privacy, Wallet

User = get_user_model()

admin.site.register(Settings)
admin.site.register(Privacy)
admin.site.register(Wallet)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "image")}),
        (_("Followers info"), {"fields": ("follower",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "podcaster",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
