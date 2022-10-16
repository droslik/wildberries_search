from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GoodsSerializer
from .utils import data_handling


class GoodsApiView(APIView):
    serializer_class = GoodsSerializer

    def get(self, request):
        return Response('Welcome to the searching service! '
                        'Please, enter the article number into the field'
                        'or attach xlsx-file')

    def post(self, request):
        data = data_handling(request)
        if isinstance(data, list):
            serializer = GoodsSerializer(data, many=True)
            return Response({'goods': list(serializer.data)})
        serializer = GoodsSerializer(data)
        return Response(serializer.data)
