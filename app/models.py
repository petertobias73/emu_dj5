from django.db import models
import datetime
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



# Családi adatok
class Szulo(models.Model):
    #user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nev = models.CharField('* Szülő neve', max_length=50, null=True, blank=False)
    telefon = models.CharField('* Telefonszáma', max_length=16, null=True, blank=False)
    email = models.EmailField('* E-mail cím', null=True, blank=False)
    lev_cim = models.CharField('* Számlázási cím', max_length=80, null=True, blank=False)
    szerzodo = models.BooleanField('Szerződő fél', default=False)
    aktiv = models.BooleanField('Aktív', default=True)
    rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True)
    modositva = models.DateTimeField('Módosítva', auto_now=True)
    
    #rogzito = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nev
    def gyerekek(self):        
        return Csalad.objects.filter(szulo=self.id)
    
    class Meta:
        ordering = ['nev']
        unique_together = ['nev', 'telefon']

class Gyerek(models.Model):
    nev = models.CharField('* Gyerek neve', max_length=50, blank=False, null=True)
    szul_ido = models.DateField('* Gyerek születési ideje', auto_now_add=False, auto_now=False, null=True)
    kod = models.CharField('Gyerek kód', max_length=50, blank=False, null=True)
    anyja_neve = models.CharField('* Anyja születési neve', max_length=50, blank=False, null=True)
    aktiv = models.BooleanField('Oktatásban van', default=True)
    #rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True)
    #rogzito = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def age(self):
        return timezone.now().year - self.szul_ido.year
        
    def __str__(self):
        return self.kod

    def szulok(self):        
        return Csalad.objects.filter(gyerek=self.id)

    def csoportok(self):
        return GyerektoCsoport.objects.filter(gyerek=self.id)

        

    class Meta:
        ordering = ['kod']
        unique_together = ['nev', 'szul_ido', 'anyja_neve']

class Csalad(models.Model):
    szulo = models.ForeignKey(Szulo, on_delete=models.CASCADE, verbose_name='Szülő', blank=False)
    gyerek = models.ForeignKey(Gyerek, on_delete=models.CASCADE, verbose_name='Gyerek', blank=False)  
    def __str__(self):
        elnevezes = self.szulo.nev + ' - ' + self.gyerek.nev
        return elnevezes
    class Meta:
        unique_together = ['gyerek', 'szulo']

class Helyszin(models.Model):
    elnevezes = models.CharField('* Foglalkozások helyszín elnevezése', max_length=30, blank=False, null=True, unique=True)
    varos = models.CharField('* Város', max_length=30, blank=False, null=True, unique=True)
    cim = models.CharField('* Címe', max_length=50, blank=False, null=True, unique=True)

    def __str__(self):
        return self.elnevezes

    class Meta:
        ordering = ['elnevezes']
    


# Guru - Foglalkozások - Tanítvány adatok
class Guru(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='* Felhasználó')
    nev = models.CharField('* Név', max_length=50, blank=False, null=True, unique=True)
    kepzettseg = models.CharField('* Képzettség', max_length=100, blank=False, null=True )
    bemutatkozas = RichTextField('* Bemutatkozás',null=True, blank=True)
    fenykep = models.ImageField('Fénykép', default="guru.jpg", null=True, blank=True)
    helyszin = models.ForeignKey(Helyszin, on_delete=models.CASCADE, null=True, verbose_name='* Helyszín')
    email = models.EmailField('* E-mail cím', null=True, blank=False)
    aktiv = models.BooleanField('Aktív', default=True)

    def __str__(self):
        return self.nev

class Foglalkozas_tipus(models.Model):
    KATEGORIAK = (
            ('Egyéni', 'Egyéni'),
			('Páros', 'Páros'),
			('Csoportos', 'Csoportos'),
            ('Család terápia', 'Család terápia'),
            ('Szülői', 'Szülői'),
            ('Egyéb', 'Egyéb'),
			)

    nev = models.CharField('* Foglalkozás típus elnevezése ', max_length=50, blank=False, null=True, unique=True)
    ar = models.IntegerField('* Foglalkozás típus ára Ft-ban', blank=False, null=True)
    cat = models.CharField('* Foglalkozás típus kategória ', max_length=30, blank=False, null=True, choices=KATEGORIAK)
    
    #rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True)
    #rogzito = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nev
    class Meta:
        ordering = ['cat']


class Csoport(models.Model):#A terápia modelje. Csak a felületek vannak átnevezve
    nev = models.CharField('* Terápia elnevezése ', max_length=50, blank=False, null=True, unique=True)
    foglalkozas_tipus = models.ForeignKey(Foglalkozas_tipus, on_delete=models.CASCADE, verbose_name='* Típus')
    helyszin = models.ForeignKey(Helyszin, on_delete=models.CASCADE, null=True, verbose_name='* Helyszín')
    aktiv = models.BooleanField('Aktív', default=True)

    #rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True)
    #rogzito = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nev

    def guruk(self):        
        return GurutoCsoport.objects.filter(csoport=self.id)
    def gyerekek(self):        
        return GyerektoCsoport.objects.filter(csoport=self.id)
    
    class Meta:
        ordering = ['nev']
        


class GurutoCsoport(models.Model):
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, verbose_name='Terapeuta')
    csoport = models.ForeignKey(Csoport, on_delete=models.CASCADE, verbose_name='Terápia')
    def __str__(self):
        elnevezes = self.csoport.nev + ' - ' + self.guru.nev
        return elnevezes   
    class Meta:
        unique_together = ['csoport', 'guru']
        ordering = ['csoport']


class GyerektoCsoport(models.Model):
    gyerek = models.ForeignKey(Gyerek, on_delete=models.CASCADE, verbose_name='Gyerek')
    csoport = models.ForeignKey(Csoport, on_delete=models.CASCADE, verbose_name='Terápia')
    def __str__(self):
        elnevezes = self.csoport.nev + ' - ' + self.gyerek.nev
        return elnevezes   
    class Meta:
        unique_together = ['csoport', 'gyerek']
        ordering = ['csoport']


class Ora(models.Model):
    kezdes = models.DateTimeField('* Kezdés')
    befejezes = models.DateTimeField('* Befejezés')
    csoport = models.ForeignKey(Csoport, on_delete=models.CASCADE, verbose_name='* Terápia')
    feljegyzes = models.TextField(null=True, blank=True)
    megtartott = models.BooleanField('Megtartott', default=False)
    lezart = models.BooleanField('Lezárva', default=False)
    #rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True)
    #rogzito = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        elnevezes = self.csoport.nev + ' - ' + str(self.kezdes)
        return elnevezes
    
    def guruk(self):
        csoport=self.csoport        
        return GurutoCsoport.objects.filter(csoport=csoport)
    
    def gyerekek(self):
        csoport=self.csoport        
        return GyerektoCsoport.objects.filter(csoport=csoport)

    class Meta:
        unique_together = ['csoport', 'kezdes']
        ordering = ['csoport', 'kezdes']

class Jelenleti(models.Model):

    ALLAPOT = (
            (0, 'Nincs beállítva'),
			(1, 'Jelen volt'),
			(2, '100%-os lemondás'),
            (3, '0%-os lemondás'),
			)


    ora = models.ForeignKey(Ora, on_delete=models.CASCADE, verbose_name='Óra')
    gyerek = models.ForeignKey(Gyerek, on_delete=models.CASCADE, verbose_name='Gyerek')
    status = models.IntegerField(default=0, null=True, choices=ALLAPOT, verbose_name='Jelenléte')
    #rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True)
    #rogzito = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        elnevezes = str(self.ora) +' - '+ self.gyerek.kod
        return elnevezes
    class Meta:
        unique_together = ['ora', 'gyerek']

class Befizetes(models.Model):
    szulo = models.ForeignKey(Szulo, on_delete=models.CASCADE, verbose_name='* Szülő')
    osszeg = models.IntegerField('* Összeg')
    datum = models.DateField(auto_now=True, null=True, auto_now_add=False)
    megjegyzes = RichTextField(null=True, blank=True, verbose_name='Megjegyzés')
    rogzitve = models.DateTimeField('Rögzítve', auto_now_add=True, blank=True)
    rogzito = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    def __str__(self):
        elnevezes = self.szulo.nev +' - '+ str(self.datum) +' - ' + str(self.osszeg)
        return elnevezes


class Egyedi(models.Model):

    TIPUS = (
            ('Alapozó szakasz', 'Alapozó szakasz'),
			('Online tréning', 'Online tréning'),
			('Felvétel', 'Felvétel'),
            )


    idopont = models.DateTimeField('Időpont')
    tipus = models.CharField('Típus', null=True, blank=True, choices=TIPUS, max_length=40)
    letszam = models.IntegerField('Léteszám', null=True)
    megtartva = models.BooleanField('Megtartva', default=False)
    leiras = models.CharField('Leiras', null=True, blank=True, max_length=60)
    ar = models.IntegerField('Ára', null=True)


    def __str__(self):
        elnevezes = self.tipus + ' - ' + str(self.idopont)
        return elnevezes

    class Meta:
        unique_together = ['idopont', 'tipus']
        ordering = ['idopont']

class Napiuzi(models.Model):
    szoveg = models.TextField('Üzenet', null=True )
    rogzitve = models.DateField('Rögzítve', auto_now_add=True)
    rogzito = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.szoveg[:30]

    class Meta:
        ordering = ['rogzitve']



            
