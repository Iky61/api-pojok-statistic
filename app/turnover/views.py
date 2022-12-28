import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TurnoverSerializer

from  app.views import *
import pandas as pd


class TurnoverApiView(APIView):
    # fungsi untuk mengirimkan data bar_plot
    def Bar_plot(self, filename):
        df = pd.read_excel(filename)
    
        final = {}
        all_obj_target = Feature_Target(dataset=df)
        for x in all_obj_target:
            feature = x['option'][0]
            target = x['option'][1]

            df1 = df.groupby([feature])[[target]].sum().sort_values(target, ascending=False).reset_index()

            X = df1[feature].tolist()
            Y = df1[target].tolist()

            data = []
            for a, b in zip(X, Y):
                value = {'label':a, 'data':b}
                data.append(value)
            
            final[x['kode']] = data

        return final


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
