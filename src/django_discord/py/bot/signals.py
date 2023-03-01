import django.dispatch

bot_ready = django.dispatch.Signal()
command_error = django.dispatch.Signal()
bot_error = django.dispatch.Signal()
