from django.db import models


class Packet(models.Model):
    resource_id = models.PositiveIntegerField(null=False)
    payload = models.CharField(max_length=20000, null=False)
    packet_index = models.PositiveIntegerField(null=False)
    last_chunk = models.BooleanField(null=True)
