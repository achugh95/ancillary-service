from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from ancillary.kafka.consumer import AncillaryService
from ancillary.serializers import PacketSerializer


class SendData(APIView):

    serializer_class = PacketSerializer

    def post(self, request, *args, **kwargs):

        request_data = request.data

        # Validate Data
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)

        AncillaryService().process(packet_data=request_data)
        response = {
            "status": 0,
            "message": "Success",
        }
        return Response(response, status=HTTP_200_OK)
