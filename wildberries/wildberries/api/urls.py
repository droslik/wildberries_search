from django.urls import path
from .views import GoodsApiView


urlpatterns = [
    path('goods-list', GoodsApiView.as_view(), name='goods'),
]
