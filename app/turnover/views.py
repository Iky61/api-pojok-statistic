import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TurnoverSerializer

import pandas as pd


class TurnoverApiView(APIView):
    def Bar_plot(self, filename):
        df = pd.read_excel(filename)
        cols = df.columns.tolist()
        feature = []
        target = []

        for x in cols:
            if df[x].dtype == 'O':
                feature.append(x)
            else:
                target.append(x)

        df = df.groupby(feature[0])[[target[0]]].sum().reset_index()

        X = df[feature[0]].tolist()
        Y = df[target[0]].tolist()

        data = []
        for x,y in zip(X, Y):
            value = {'label':x, 'data':y}
            data.append(value)

        return data


    def post(self, request, *args, **kwargs):
        serializers = TurnoverSerializer(data=request.data)

        if serializers.is_valid():
            file = request.data.get('file')

            # validate file type
            if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                return Response({
                    'message': 'Error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'error': 'invalid file type',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

#           # validate file
            if not file:
                return Response({
                    'message': 'Error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'error': 'invalid file',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            # save file for temporary analyze usage
            serializers.save()

            filename = '_'.join(file.name.split())
            dirname = (os.path.dirname(
                os.path.abspath(__file__)) + '/uploads/' + filename)
            
            # read file from ./uploads and analyze
            data = self.Bar_plot(filename=dirname)

            os.remove(dirname)

            return Response({
                'message': 'Success',
                'code': status.HTTP_201_CREATED,
                'error': '',
                'data': data
            }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
