from rest_framework.permissions import AllowAny
from .serializers import GridSerializer, SquareSerializer
from rest_framework import generics
from .models import Grid, Square
from rest_framework.views import APIView
from rest_framework.response import Response


class GridView(generics.ListCreateAPIView):

    permission_classes = (AllowAny,)

    queryset = Grid.objects.all()
    serializer_class = GridSerializer


class SquareView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, grid_id, format=None):
        """
        Returns the squares for given grid_id
        :param request:
        :param grid_id:
        :param format:
        :return:
        """


        squares = Square.objects.filter(grid=grid_id).all()

        return Response(SquareSerializer(squares, many=True).data)

class ExploreView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, grid_id, x, y, format=None):
        """
        explores a square
        """

        square = Square.objects.get(grid=grid_id, x=x, y=y)
        square.explore()

        view = SquareView.as_view()

        return view(request._request, grid_id=grid_id)
