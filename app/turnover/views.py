import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TurnoverSerializer

import pandas as pd


class TurnoverApiView(APIView):
    # fungsi untuk menentukan feature dan target
    def Feature_Target(self, dataset):
        df = dataset
        
        type_ = pd.DataFrame(df.dtypes).reset_index()
        
        objek = []
        value = []
        for x in range(len(type_)):
            n = type_.iloc[x]
            if n[0] == 'O' or n[0] == 'str':
                objek.append(n['index'])
            elif n[0] == 'int' or n[0] == 'float':
                value.append(n['index'])
            else:
                None
        
        objek_value = []
        for x in objek:
            for y in value:
                name = x + ' to ' + y
                feature_target = [x, y]
                a = {'kode':name, 'option':feature_target}
                objek_value.append(a)
                
        return objek_value

    # fungsi untuk mengirimkan data bar_plot
    def Bar_plot(self, filename):
        df = pd.read_excel(filename)
    
        final = []
        all_obj_target = Feature_Target(dataset=df)
        for x in all_obj_target:
            feature = x['option'][0]
            target = x['option'][1]

            df1 = df.groupby([feature])[[target]].sum().reset_index()

            X = df1[feature].tolist()
            Y = df1[target].tolist()

            data = []
            for a, b in zip(X, Y):
                value = {'label':a, 'data':b}
                data.append(value)
                
            result = {'Code':x['kode'], 'data':data}
            final.append(result)

<<<<<<< HEAD
        data = []
        for x, y in zip(X, Y):
            value = {'label': x, 'data': y}
            data.append(value)

        return data
=======
        return final
>>>>>>> 1599c1c (mengubah feature)

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
