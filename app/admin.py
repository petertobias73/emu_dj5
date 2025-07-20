from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(Szulo, Gyerek, Csalad, Guru, Foglalkozas_tipus, Csoport, GyerektoCsoport, Ora, Helyszin, GurutoCsoport, Jelenleti, Befizetes, Egyedi, Napiuzi)
class ViewAdmin (ImportExportModelAdmin):
    pass