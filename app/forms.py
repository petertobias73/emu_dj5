import datetime
from django import forms
from app.models import *
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
#from sequencing.customwidgets import ReadOnlySelect

class SzuloForm(ModelForm):
    users = User.objects.all()

    class Meta:
        model = Szulo
        fields = '__all__'
        fields_required = ['nev', 'telefon', 'email', 'lev_cim']
        
        widgets = {
            'nev': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:300px', "placeholder" : "Vezetéknév Keresztnév"}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "06xx1234567"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:300px', "placeholder" : "valaki@mail.hu"}),
            'lev_cim': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:400px', "placeholder" : "IR Város, Utca házszám"}),
        }

    
    def clean(self):
        cleaned_data = super().clean()
        telefon = cleaned_data.get("telefon")
        lev_cim = cleaned_data.get("lev_cim")
        nev = cleaned_data.get("nev")
        msg_telefon_1 = 'A telefonszámnak 06xx1234567 formátumúnak kell lennie!'
        msg_telefon_2 = 'A telefon körzetszám rossz!'
        msg_cim = 'A cím nem megfelelő!'
        msg_nev = 'A név nem megfelelő!'
        
        rossz_korzetszamok = ['00','01','02','03','04','05','08','09','10','38','39','40','41','43','51','58','60','61','64','65','67','71','80','81','86','90','91','97','98']
        
        if not (len(telefon) == 10 or len(telefon) == 11 and telefon.isdigit()) or telefon[:2]!="06":
            self._errors["telefon"] = self.error_class([msg_telefon_1])
        elif telefon[2:4] in rossz_korzetszamok:
            self._errors["telefon"] = self.error_class([msg_telefon_2])
        if not lev_cim[:4].isdigit() or lev_cim[4:5]!=" " or len(lev_cim.split(" "))<4 or len(lev_cim.split(","))<2:
            self._errors["lev_cim"] = self.error_class([msg_cim])
        if len(nev.split(" "))<2:
            self._errors["nev"] = self.error_class([msg_nev])


class GyerekForm(ModelForm):
    class Meta:
        model = Gyerek
        exclude = ('kod',)
        fields_required = ['nev', 'szul_ido', 'anyja_neve']

        widgets = {
            'nev': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:200px', "placeholder" : "Vezetéknév Keresztnév"}),
            'szul_ido': forms.DateInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "éééé-hh-nn", 'autocomplete': 'off'}),
            'anyja_neve': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:200px', "placeholder" : "Vezetéknév Keresztnév"}),
            
        }
    def clean(self):
        cleaned_data = super().clean()
        nev = cleaned_data.get("nev")
        anyja_neve = cleaned_data.get("anyja_neve")
        msg_nev = 'A név nem megfelelő!'

        if len(nev.split(" "))<2:
            self._errors["nev"] = self.error_class([msg_nev])
        if len(anyja_neve.split(" "))<2:
            self._errors["anyja_neve"] = self.error_class([msg_nev])


class GyerekUpdateForm(ModelForm):
    class Meta:
        model = Gyerek
        fields = '__all__'
        fields_required = ['nev', 'szul_ido', 'anyja_neve', 'kod']

        widgets = {

            'kod': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "Gerek Kód"}),
            'nev': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:200px', "placeholder" : "Vezetéknév Keresztnév"}),
            'szul_ido': forms.DateInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "éééé-hh-nn", 'autocomplete': 'off'}),
            'anyja_neve': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:200px', "placeholder" : "Vezetéknév Keresztnév"}),
            
        }
    def clean(self):
        cleaned_data = super().clean()
        nev = cleaned_data.get("nev")
        anyja_neve = cleaned_data.get("anyja_neve")
        msg_nev = 'A név nem megfelelő!'

        if len(nev.split(" "))<2:
            self._errors["nev"] = self.error_class([msg_nev])
        if len(anyja_neve.split(" "))<2:
            self._errors["anyja_neve"] = self.error_class([msg_nev])



class CsaladForm(ModelForm):
    class Meta:
        model = Csalad
        fields = '__all__'
        
        widgets = {
            'szulo': forms.Select(attrs={'class': 'form-control', 'style': 'width:200px'}),}

CsaladFormSet = inlineformset_factory(
    Gyerek, Csalad, form=CsaladForm,
    fields=['szulo',], extra=2, can_delete=True, max_num=2, min_num=1, validate_min=True,
    )

class HelyszinForm(ModelForm):
    class Meta:        
        model = Helyszin        
        fields = '__all__'
        fields_required = ['elnevezes', 'varos', 'cim']

        widgets = {
            'elnevezes': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:400px',  "placeholder" : "Könnyen kezelhető elnevezés"}),
            'varos': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:200px',  "placeholder" : "Városnév"}),
            'cim': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px', "placeholder" : "IR Város, Utca házszám"}),            
            }
    
    def clean(self):
        cleaned_data = super().clean()
        cim = cleaned_data.get("cim")
        msg_cim = 'A cím nem megfelelő!'
               
        if not cim[:4].isdigit() or cim[4:5]!=" " or len(cim.split(" "))<4 or len(cim.split(","))<2:
            self._errors["cim"] = self.error_class([msg_cim])


class GuruForm(ModelForm):
    class Meta:
        model = Guru
        exclude = ('fenykep',)
        fields_required = ['user','nev', 'kepzettseg', 'helyszin', 'email', 'bemutatkozas']

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'style': 'width:300px'}),
            'nev': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:300px',  "placeholder" : "Terapeuta neve"}),
            'kepzettseg': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px',  "placeholder" : "Képzettség leírása"}),
            'helyszin': forms.Select(attrs={'class': 'form-control', 'style': 'width:200px'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:300px',  "placeholder" : "E-mail"}),
            }


class Foglalkozas_tipusForm(ModelForm):

    class Meta:
        model = Foglalkozas_tipus
        fields = '__all__'
        fields_required = ['nev', 'ar', 'cat']
    
        widgets = {
            
            'nev': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:400px',  "placeholder" : "Könnyen kezelhető típus név"}),
            'ar': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:200px',  "placeholder" : "Ár Forintban"}),
            'cat': forms.Select(attrs={'class': 'form-control', 'style': 'width:200px'}),
            
            }
    
        




# Csoport űrlapok
class CsoportForm(ModelForm):
    
    class Meta:
        model = Csoport
        fields = '__all__'
        fields_required = ['nev', 'foglalkozas_tipus', 'helyszin']
    
        widgets = {
            
            'nev': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px',  "placeholder" : "Könnyen kezelhető név"}),
            'foglalkozas_tipus': forms.Select(attrs={'class': 'form-control', 'style': 'width:400px'}),
            'helyszin': forms.Select(attrs={'class': 'form-control', 'style': 'width:300px'}),
            }

class GyerektoCsoportForm(ModelForm):

    class Meta:
        model = GyerektoCsoport
        fields = '__all__'
        fields_required = ['gyerek']

              

GyerektoCsoportFormSet = inlineformset_factory(
    Csoport, GyerektoCsoport, form=GyerektoCsoportForm,
    fields=['gyerek', ], extra=1, can_delete=True ,min_num=1, validate_min=True,
    )
 
class GurutoCsoportForm(ModelForm):
    class Meta:
        model = GurutoCsoport
        fields = '__all__'
        fields_required = ['guru']
     

GurutoCsoportFormSet = inlineformset_factory(
    Csoport, GurutoCsoport, form=GurutoCsoportForm,
    fields=['guru', ], extra=0, can_delete=True, min_num=1, max_num=2, validate_min=True, validate_max=True
    )



# Óra űrlapok

class OraCreateForm(ModelForm):

    class Meta:
        
        model = Ora        
        exclude = ('megtartott',)

        widgets = {
            'kezdes': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "éééé-hh-nn óó:pp", 'autocomplete': 'off'}),
            'befejezes': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "éééé-hh-nn óó:pp", 'autocomplete': 'off'}),
            'csoport': forms.Select(attrs={'class': 'form-control', 'style': 'width:400px'}),
            'feljegyzes': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:400px', "placeholder" : "Feljegyzes"}), 
        }



    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("kezdes")
        end_date = cleaned_data.get("befejezes")
        delta = end_date - start_date
        msg = u"Nincs egy óra a bejegyzett időpontok között!"
        msg2 = u"Több mint 8 órás foglalkozás, ez nem lehet jó!"
        sok = u"Több mint egy napos óra? Egyhuzamban? Nem lesz az jó!"

        if delta.days > 0:
            self._errors["befejezes"] = self.error_class([sok])
        elif delta.seconds < 1800:
            self._errors["befejezes"] = self.error_class([msg])
        elif delta.seconds > 28800:
            self._errors["befejezes"] = self.error_class([msg2])
    

class OraModForm(ModelForm):
    class Meta:        
        model = Ora        
        exclude = ('megtartott',)
        
#(3, 'Havonta'),
class OraismetlesForm(forms.Form):
    
    ISMETLODES = (
        
        (2, 'Hetente'),
        (3, 'Havonta'),
        
        )
    
    hetfo = forms.BooleanField(label='Hétfő', initial=False, required=False)
    kedd = forms.BooleanField(label='Kedd', initial=False, required=False)
    szerda = forms.BooleanField(label='Szerda', initial=False, required=False)
    csutortok = forms.BooleanField(label='Csütörtök', initial=False, required=False)
    pentek = forms.BooleanField(label='Péntek', initial=False, required=False)
    szombat = forms.BooleanField(label='Szombat', initial=False, required=False)
    periodus = forms.ChoiceField(choices=ISMETLODES, required=True)
    idohosz = forms.IntegerField(label='Alklalom',min_value=1, help_text='Hány alkalom legyen?', required=True)


class JelenletiForm(ModelForm):
      class Meta:
        model = Jelenleti
        exclude = ('ora',)
        widgets = {
            
            
            'gyerek': forms.Select(attrs={'class': 'form-control', 'style': 'width:150px'}),
            #'gyerek': forms.Select(attrs={'class': 'form-control', 'disabled':"", 'style': 'width:150px'}),
            'status': forms.Select(attrs={'class': 'form-control', 'style': 'width:150px'}),
        }

class JelenletiForm2(ModelForm):

    def __init__(self, pk, *args, **kwargs):
        self.pk = pk
        super().__init__(*args, **kwargs)

        #ora = Ora.objects.get(id=5514)
        ora = Ora.objects.get(id=self.pk)
        csoport=ora.csoport
        qs = GyerektoCsoport.objects.values_list('gyerek', flat=True).filter(csoport=csoport)
        gyerekek = Gyerek.objects.filter(id__in=qs)
        self.fields['gyerek'].queryset = gyerekek
    
    class Meta:
        model = Jelenleti
        exclude = ('ora',)
        widgets = {
           
           
            'gyerek': forms.Select(attrs={'class': 'form-control-sm', 'style': 'width:150px','type':'hidden'}),
            #'gyerek': forms.Select(attrs={'class': 'form-control', 'disabled':"", 'style': 'width:150px'}),
            'status': forms.RadioSelect(attrs={'type': 'button'}),
        }

    
        

class OraForm(ModelForm):
    class Meta:
        model = Ora
        fields = ['csoport', 'megtartott']


class BefizetesForm(ModelForm):
    szulo = forms.ModelChoiceField(label='* Szülő',
        queryset=Szulo.objects.filter(aktiv=True).filter(szerzodo=True))

    class Meta:        
        model = Befizetes
        exclude = ('rogzito',)        
        #fields = '__all__'
        fields_required = ['szulo','osszeg']
        

    
    
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Felhasználónév",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "E-mail cím",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Jelszó először",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Jelszó másodszor",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class JelszocsereForm(PasswordChangeForm):

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Régi jelszó",                
                "class": "form-control"
            }
        ))

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Új jelszó",                
                "class": "form-control"
            }
        ))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Új jelszó megint",                
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class PasswChangeForm(SetPasswordForm):

    class Meta:
        model = User
        fields = '__all__'

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Új jelszó",                
                "class": "form-control"
            }
        ))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Új jelszó megint",                
                "class": "form-control"
            }
        ))





class UserModForm(ModelForm):
        class Meta:
            model = User
            exclude = ('user_permissions', 'is_superuser', 'is_staff', 'password')
            
            
        def clean(self):
            cleaned_data = super().clean()
            groups = cleaned_data.get("groups")
            msg = 'Egy felhasználó csak egy csoportban lehet tag. Ön többet jelölt!'
            
            if groups.count() > 1:
                self._errors["groups"] = self.error_class([msg])



class EgyediForm(ModelForm):
    
    class Meta:
        model = Egyedi
        fields = '__all__'

        widgets = {
            
            'leiras': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:400px'}),
                        
        }
        widgets = {
            'idopont': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "éééé-hh-nn óó:pp", 'autocomplete': 'off'}),
            'tipus': forms.Select(attrs={'class': 'form-control', 'style': 'width:400px'}),
            'letszam':forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "létszám"}),
            'ar':forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:150px', "placeholder" : "ár Forintban"}),
            'leiras': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:400px'}),
            
        }



class NapiuziForm(ModelForm):
    
    class Meta:
        model = Napiuzi
        fields = ('szoveg',)

        widgets = {
            'szoveg': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:400px'}),
                        
        }


#widgetek: https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.TextInput



class Havi_osszesites(forms.Form):

    EVEK = (
        ('2021','2021'),
        ('2022','2022'),
        ('2023','2023'),
        ('2024','2024')
        )

    HONAPOK =(
        ('01','Január'),
        ('02','Február'),
        ('03','Március'),
        ('04','Április'),
        ('05','Május'),
        ('06','Június'),
        ('07','Július'),
        ('08','Augusztus'),
        ('09','Szeptember'),
        ('10','Október'),
        ('11','November'),
        ('12','December'),
        )

    ev = forms.ChoiceField(label='Év ', choices=EVEK, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:80px'}))
    honap = forms.ChoiceField(label='Hónap ', choices=HONAPOK, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:130px'}))

    #https://stackoverflow.com/questions/36724255/render-choicefield-options-in-django-template