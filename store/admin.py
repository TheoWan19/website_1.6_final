from django.contrib import admin
from .models import *
from accounts.models import Employee, ClientUser
from django.utils.translation import gettext_lazy as _

# Register your models here.

class AdminInvoice(admin.ModelAdmin):
    list_display = ('invoice_id','client', 'save_by', 'invoice_date_time', 'total', 'last_updated_date', 'paid', 'invoice_type')    

admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article)

admin.site.site_title = _("VAAPPARYAJ INVOICE SYSTEM")
admin.site.site_header = _("VAAPPARYAJ INVOICE SYSTEM")
admin.site.index_title = _("VAAPPARYAJ INVOICE SYSTEM")