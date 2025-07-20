from rest_framework import serializers
from app.models import Gyerek

class GyerekSerializers(serializers.ModelSerializer):
	class Meta:
	    model = Gyerek
	    fields = ('id', 'kod', 'szul_ido', 'aktiv', "age")


