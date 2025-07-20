from django.urls import path, re_path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [

    # The home page
    
    path('', views.index, name='home'),

    #Vezetői view-k
    path('gyerek/', views.GyerekCreate, name="gyerek"),
    path('gyerek/<str:pk>/', views.GyerekUpdate, name="gyerek_mod"),
    path('gyerek_lista/', views.GyerekList, name="gyerek_lista"),
    path('gyerek_lista_export/', views.GyerekListExport, name="gyerek_lista_export"),
    

    path('szulo/', views.SzuloCreate, name="szulo"),
    path('szulo/<str:pk>/', views.SzuloUpdate, name="szulo_mod"),
    path('szulo_lista/', views.SzuloList, name="szulo_lista"),
    
    path('szulo_lista_export/', views.SzuloListExport, name="szulo_lista_export"),
   
    path('guru/', views.GuruCreate, name="guru"),
    path('guru/<str:pk>/', views.GuruUpdate, name="guru_mod"),
    path('guru_lista/', views.GuruList, name="guru_lista"),

    path('foglalkozas_tipus/', views.Foglalkozas_tipusCreate, name="foglalkozas_tipus"),
    path('foglalkozas_tipus/<str:pk>/', views.Foglalkozas_tipusUpdate, name="foglalkozas_tipus_mod"),
    path('foglalkozas_tipus_lista/', views.Foglalkozas_tipusList, name="foglalkozas_tipus_lista"),
    
    path('helyszin/', views.HelyszinView, name="helyszin"),
    path('helyszin/<str:pk>/', views.HelyszinUpdate, name="helyszin_mod"),
    path('helyszin_lista/', views.HelyszinList, name="helyszin_lista"),

    path('terapia/', views.CsoportCreate, name="terapia"),
    path('terapia/<str:pk>/',  views.CsoportUpdate, name='terapia_mod'),
    path('terapia_lista/', views.CsoportList, name="terapia_lista"),
    path('terapia_lista_export/', views.CsoportListExport, name="terapia_lista_export"),

    path('ora/', views.OraCreate, name="ora"),
    path('ismetles/<str:pk>/', views.OraIsmetles, name="ismetles"),
    path('ora_lista/', views.OraListEgy, name="ora_lista"),
    path('ora_lista_meg/', views.OraListEgyMeg, name="ora_lista_meg"),
    path('nemmegtartott_havi_ora_lista/', views.OraListEgyNem, name="nemmegtartott_havi_ora_lista"),

    path('ora_lista_harom/', views.OraListHarom, name="ora_lista_harom"),
    path('ora_lista_full/', views.OraListFull, name="ora_lista_full"),
    path('ora/<str:pk>/', views.OraUpdate, name="ora_mod"),
    path('ora_torles/<str:pk>/', views.OraTorles, name="ora_torles"),
 

    path('egyedi/', views.EgyediCreate, name="egyedi"),
    path('egyedi_lista/', views.EgyediList, name="egyedi_lista"),
    path('egyedi/<str:pk>/', views.EgyediUpdate, name="egyedi_mod"),
    path('egyedi_torles/<str:pk>/', views.EgyediTorles, name="egyedi_torles"),

    path('napiuzi/', views.NapiuziCreate, name="napiuzi"),
    path('napiuzi_lista/', views.NapiuziList, name="napiuzi_lista"),
    path('napiuzi/<str:pk>/', views.NapiuziUpdate, name="napiuzi_mod"),
    path('napiuzi_torles/<str:pk>/', views.NapiuziTorles, name="napiuzi_torles"),
    
    path('jelenleti/<str:pk>/', views.JelenletiView, name="jelenleti"),
    path('jelenleti_regen/<str:pk>/', views.Jelenleti_regenerate_View, name="jelenleti_regen"),
    
    path('befizetes/', views.BefizetesView, name="befizetes"),
    path('befizetes_lista/', views.BefizetesList, name="befizetes_lista"),
    path('befizetes/<str:pk>/', views.BefizetesUpdate, name="befizetes_mod"),

    path('egyenlegek/', views.EgyenlegekView, name="egyenlegek"),
    path('attekinto/', views.AttekintoView, name="attekinto"),
    path('osszesitett_elszamolas/', views.Osszesített_elszamolas, name="osszesitett_elszamolas"),
    path('export_havi_osszesites/<str:pk>/', views.export_havi_osszesites, name="export_havi_osszesites"),
    path('export_havi_osszesites_honap/<str:pk>/', views.export_havi_osszesites_honap, name="export_havi_osszesites_honap"),
    path('osszesito/', views.osszesito, name="osszesito"),
    

    path('uj_felhasznalo/', views.register_user, name="uj_felhasznalo"),
    path('felhasznalok/', views.felhasznalok, name="felhasznalok"),
    path('user_mod/<str:pk>/', views.user_mod, name="user_mod"),
    path('jelszocsere/', views.jelszocsere, name="jelszocsere"),
    path('passwchange/<str:pk>/', views.passwchange, name="passwchange"),

    

    path('naptar/', views.naptar, name="naptar"),

    path('guru_lap/', views.guru_lap, name='guru_lap'),
    

    #re_path(r'^.*\.*', views.pages, name='pages'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)