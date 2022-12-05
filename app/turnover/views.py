from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TurnoverSerializer


class TurnoverApiView(APIView):
    def post(self, request, *args, **kwargs):

        serializers = TurnoverSerializer(data=request.data)

        if serializers.is_valid():
            # TODO: change model to file
            file = request.data.get('file')
            print(file)

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
