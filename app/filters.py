from django_filters import DateFilter, CharFilter, BooleanFilter, NumberFilter, ChoiceFilter, FilterSet, ModelChoiceFilter, DateTimeFilter, DateRangeFilter
from django import forms
from .models import *

class GyerekFilter(FilterSet):

	valasztas = (
            (True, 'Aktív' ),
			(False, 'Nem Aktív'),
			)

	kod = CharFilter(field_name="kod", lookup_expr='icontains', label='Gyerek neve')
	ev = NumberFilter(field_name="szul_ido", lookup_expr='year', widget=forms.NumberInput(attrs={'style':'width:70px'}))
	honap = NumberFilter(field_name="szul_ido", lookup_expr='month', widget=forms.NumberInput(attrs={'style':'width:50px'}))
	nap = NumberFilter(field_name="szul_ido", lookup_expr='day', widget=forms.NumberInput(attrs={'style':'width:50px'}))
	
	anyja_neve = CharFilter(field_name="anyja_neve", lookup_expr='icontains', label='Anyja neve')
	aktiv = ChoiceFilter(field_name="aktiv", label='Aktív', choices=valasztas)
	
	
	
	class Meta:
		model = Gyerek
		fields = ['kod', 'ev','honap', 'nap', 'anyja_neve', 'aktiv']
	

class SzuloFilter(FilterSet):

	nev = CharFilter(field_name="nev", lookup_expr='icontains', label='Szülő neve')
	telefon = CharFilter(field_name="telefon", lookup_expr='icontains', label='Telefonszám')
	email = CharFilter(field_name="email", lookup_expr='icontains', label='E-mail')
	lev_cim = CharFilter(field_name="lev_cim", lookup_expr='icontains', label='Levelezési cím')
	szerzodo = BooleanFilter(field_name="szerzodo", label='Szerződő')
	class Meta:
		model = Gyerek
		fields = ['nev', 'telefon', 'email', 'lev_cim', 'szerzodo']


class GuruFilter(FilterSet):

	Helyszinek = (
		(1, 'Budapesti Központ'),
		(2, 'Pécsi Központ'),
	)
	nev = CharFilter(field_name="nev", lookup_expr='icontains', label='Oktató neve')
	kepzettseg = CharFilter(field_name="kepzettseg", lookup_expr='icontains', label='Képzettség')
	helyszin = ChoiceFilter (field_name="helyszin", choices=Helyszinek)

	
	class Meta:
		model = Guru
		fields = ['nev', 'kepzettseg', 'helyszin']

class Foglalkozas_tipusFilter(FilterSet):

	Kategoriak = (
            ('Egyéni', 'Egyéni'),
			('Páros', 'Páros'),
			('Csoportos', 'Csoportos'),
            ('Család terápia', 'Család terápia'),
            ('Szülői', 'Szülői'),
            ('Online', 'Online'),
            ('Egyéb', 'Egyéb'),
			)
	cat = ChoiceFilter(field_name="cat", choices=Kategoriak, label='Foglalkozás típus kategóriája')
	nev = CharFilter(field_name="nev", lookup_expr='icontains', label='Foglalkozás típus elnevezése')
	ar = CharFilter(field_name="ar", lookup_expr='icontains', label='Ár')
	class Meta:
		model = Foglalkozas_tipus
		fields = ['nev', 'ar', 'cat']


class HelyszinFilter(FilterSet):

	elnevezes = CharFilter(field_name="elnevezes", lookup_expr='icontains', label='Elnevezés')
	varos = CharFilter(field_name="varos", lookup_expr='icontains', label='Város')
	cim = CharFilter(field_name="cim", lookup_expr='icontains', label='Cím')
	
	class Meta:
		model = Helyszin
		fields = ['elnevezes', 'varos', 'cim']


class CsoportFilter(FilterSet):

	valasztas = (
            (True, 'Aktív' ),
			(False, 'Nem Aktív'),
			)

	nev = CharFilter(field_name="nev", lookup_expr='icontains', label='Csoport elnevezése')
	foglalkozas_tipus = ModelChoiceFilter(field_name="foglalkozas_tipus", queryset=Foglalkozas_tipus.objects.all())
	helyszin = ModelChoiceFilter(field_name="helyszin", queryset=Helyszin.objects.all())
	aktiv = ChoiceFilter(field_name="aktiv", label='Aktív', choices=valasztas, )

	class Meta:
		model = Csoport
		fields = ['nev', 'foglalkozas_tipus', 'helyszin', 'aktiv']

	


class OraFilter(FilterSet):

	class Meta:
		model = Ora
		fields = ['csoport', 'ev', 'honap', 'nap','megtartott']

	csoport = CharFilter(field_name="csoport__nev", lookup_expr='icontains', label='Terápia elnevezése')
	ev = NumberFilter(field_name="kezdes", lookup_expr='year', widget=forms.NumberInput(attrs={'style':'width:70px'}))
	honap = NumberFilter(field_name="kezdes", lookup_expr='month', widget=forms.NumberInput(attrs={'style':'width:50px'}))
	nap = NumberFilter(field_name="kezdes", lookup_expr='day', widget=forms.NumberInput(attrs={'style':'width:50px'}))
	megtartott = BooleanFilter(field_name="megtartott", label='Megtartott')

class GyerekCsoportFilter(FilterSet):

	class Meta:
		model = GyerektoCsoport
		fields = ['gyerek']

	gyerek = ModelChoiceFilter(field_name="gyerek")
	
	

class BefizetesFilter(FilterSet):

	class Meta:
		model = Befizetes
		fields = ['szulo', 'osszeg', 'datum']
	
	szulo = ModelChoiceFilter(field_name="szulo", queryset=Szulo.objects.filter(szerzodo=True))
	#szulo = CharFilter(field_name="szulo", lookup_expr='icontains', label='Szülő')
	osszeg = CharFilter(field_name="osszeg", lookup_expr='icontains', label='Összeg')
	datum = DateTimeFilter(field_name="kezdes", input_formats=["%Y.%m.%d  %H:%M"], label='Befizetés dátuma')


class EgyediFilter(FilterSet):

	Tipusok = (
            ('Alapozó szakasz', 'Alapozó szakasz'),
			('Online tréning', 'Online tréning'),
			('Felvétel', 'Felvétel'),
            )

	idopont = DateTimeFilter(field_name="idopont", input_formats=["%Y.%m.%d  %H:%M"], label='Időpont')
	tipus = ChoiceFilter(field_name="tipus", choices=Tipusok, label='Egyedi típus')
	megtartva = BooleanFilter(field_name="megtartva", label='Megtartott')	

	class Meta:
		model = Egyedi
		fields = ['idopont', 'tipus', 'megtartva']

class NapiuziFilter(FilterSet):

	szoveg = CharFilter(field_name="szoveg", lookup_expr='icontains', label='Szöveg')
	rogzitve = DateFilter(field_name="rogzitve", input_formats=["%Y.%m.%d"], label='Rögzítve')
	rogzito = CharFilter(field_name="rogzito", lookup_expr='icontains', label='Rögzítő')
	
	class Meta:
		model = Napiuzi
		fields = ['rogzitve', 'szoveg', 'rogzito']