import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TurnoverSerializer

from  app.views import *
import pandas as pd


class TurnoverApiView(APIView):
    def Omset_Analyst(self, filename):
        df = pd.read_excel(filename)
        df = df[['Tanggal', 'User', 'Quantity', 'Total']]
        df = df[df.Total > 100]
        df = Time_Enginering(df)
        df['User'] = df.User.apply(lambda x: x.split()[0].split('_')[0].split('(')[0])
        df = df.groupby(['Tahun', 'No_Bulan', 'Bulan', 'User'])[['Quantity', 'Total', 'Nomor']].sum().reset_index()
        df['Date'] = df.Bulan.apply(lambda x: str(x) + '-') + df.Tahun.apply(lambda x: str(x))
        
        DATA = {}
        for x in df.No_Bulan.unique().tolist():
            if x == 1:
                n = df[df.No_Bulan == x]
                value1 = []
                for y in n.User.unique().tolist():
                    value2 = {}
                    m = n[n.User == y]
                    value2["label"] = y
                    value2["data"] = m.Total.tolist()[0]
                    value1.append(value2)
                DATA[n.Date.unique()[0]] = value1
            else:
                n = df[df.No_Bulan <= x]
                value1 = []
                for y in n[n.No_Bulan == x].User.unique().tolist():
                    value2 = {}
                    m = n[n.User == y]
                    average = m[m.No_Bulan < x].Total.mean()
                    condition = str(average)
                    if condition == 'nan':
                        value2["label"] = y
                        value2["date"] = m[n.No_Bulan == x].Total.sum()
                        value1.append(value2)
                    else:
                        value2["label"] = y
                        value2["date"] = m[n.No_Bulan == x].Total.sum()
                        value2["average"] = average
                        value1.append(value2)
                DATA[n.Date.unique()[-1]] = value1
        return DATA


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
            data = self.Omset_Analyst(filename=dirname)

            os.remove(dirname)

            return Response({
                'message': 'Success',
                'code': status.HTTP_201_CREATED,
                'error': '',
                'data': data
            }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
