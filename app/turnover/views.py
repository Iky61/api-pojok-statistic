import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TurnoverSerializer


class TurnoverApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializers = TurnoverSerializer(data=request.data)

        if serializers.is_valid():
            file = request.data.get('file')

            # validate file type
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                return Response({
                    'message': 'Error',
                    'code': 400,
                    'error': 'invalid file type',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

#           # validate file
            if not file:
                return Response({
                    'message': 'Error',
                    'code': '400',
                    'error': 'invalid file',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            # save file for temporary analyze usage
            serializers.save()

            # TODO: Analyze & return graph data
            # read file from ./uploads and analyze
            data = {}

            # delete uploaded file & return response
            dirname = (os.path.dirname(
                os.path.abspath(__file__)) + '/uploads/' + file.name)
            os.remove(dirname)

            return Response({
                'message': 'Success',
                'code': 201,
                'error': '',
                'data': data
            }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
