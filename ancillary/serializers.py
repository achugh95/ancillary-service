from rest_framework.serializers import ModelSerializer

from ancillary.models import Packet


class PacketSerializer(ModelSerializer):
    class Meta:
        model = Packet
        fields = "__all__"
