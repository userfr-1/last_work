from configapp.models import *
from configapp.serializers import *
from rest_framework.viewsets import ModelViewSet
class AddGroupAPI(ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupSerializer

class AddTableAPI(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class RoomsAPI(ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer

class TableAPI(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableTypeAPI(ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer