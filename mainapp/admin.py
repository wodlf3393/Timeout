from django.contrib import admin
from .models import User_account, User_history, Schedule, Group_account, Invite, Punish,Group_history
# Register your models here.

admin.site.register(User_account)
admin.site.register(User_history)
admin.site.register(Schedule)
admin.site.register(Group_account)
admin.site.register(Invite)
admin.site.register(Punish)
admin.site.register(Group_history)