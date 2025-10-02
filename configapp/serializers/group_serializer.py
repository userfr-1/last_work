from rest_framework import serializers

from configapp.models import GroupStudent, Table,Rooms,TableType

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = "__all__"
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = "__all__"

class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = "__all__"