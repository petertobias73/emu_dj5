import datetime
from django.db.models import Q
from django.apps import AppConfig

class AppMainConfig(AppConfig):     # 👈 Egyedibb név
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'


'''
def SzuloListaExport (qs):

    workbook = load_workbook('havi_elszamolas_2.xlsx')
    
    
    worksheet = workbook.active
    worksheet.title = gyerek.nev
    

    qs = Jelenleti.objects.values_list('ora', flat=True).filter(gyerek=gyerek)
    orak = Ora.objects.filter(id__in=qs).filter(kezdes__year=ev, kezdes__month=elozo_honap)
    fejlec=gyerek.nev+" terápiái a "+str(ev)+". év "+str(elozo_honap)+". hónapban"
    worksheet.cell(row=1, column=1).value=fejlec
    sor=4
    
    for ora in orak:
        worksheet.cell(row=sor, column=1).value=ora.csoport.nev
        worksheet.cell(row=sor, column=2).value=ora.csoport.foglalkozas_tipus.nev
        worksheet.cell(row=sor, column=3).value=ora.kezdes.date()
        allapot=Jelenleti.objects.filter(gyerek=gyerek).filter(ora=ora)[0].status
        if allapot == 0:
            worksheet.cell(row=sor, column=4).value="jelöletlen"
            worksheet.cell(row=sor, column=5).value=0
        elif allapot == 1:
            worksheet.cell(row=sor, column=4).value="megjelent"
            worksheet.cell(row=sor, column=5).value=ora.csoport.foglalkozas_tipus.ar
            osszesen = osszesen + ora.csoport.foglalkozas_tipus.ar
        elif allapot == 2:
            worksheet.cell(row=sor, column=4).value="0%-os lemondás"
            worksheet.cell(row=sor, column=5).value=0
        elif allapot == 3:
            worksheet.cell(row=sor, column=4).value="100%-os lemondás"
            worksheet.cell(row=sor, column=5).value=ora.csoport.foglalkozas_tipus.ar
            osszesen = osszesen + ora.csoport.foglalkozas_tipus.ar
        sor = sor + 1

    worksheet.cell(row=sor+1, column=1).value="Összesen:"
    worksheet.cell(row=sor+1, column=5).value=osszesen
    xlsfilename=gyerek.nev+"_"+str(ev)+"_"+str(elozo_honap)+".xlsx"
    response = HttpResponse(content=save_virtual_workbook(workbook))
    #response = HttpResponse(content=save_virtual_workbook(workbook), mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='+xlsfilename
    return response
'''



