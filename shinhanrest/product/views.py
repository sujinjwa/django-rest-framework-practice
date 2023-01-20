from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response
from .models import Product, Comment, Like
from .serializers import (
    ProductSerializer, 
    CommentSerializer, 
    CommentCreateSerializer,
    LikeSerializer
)
from .paginations import ProductLargePagination

class ProductListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # serialize : 객체를 json으로 변환
    serializer_class = ProductSerializer
    # pagination_class = ProductLargePagination

    def get_queryset(self):
        # GenericAPIView 가 가지는 메서드
        # 원하는 값만 검색해서 queryset 가져오려면, 인자값 받아서 filter 해야 한다
        
        products = Product.objects.all()
        
        name = self.request.query_params.get('name')

        if name:
            products = products.filter(name__contains=name)
        
        return products

    # 리스트 전달, get: ListModelMixin이 가지는 메서드
    def get(self, request, *args, **kwargs):
        # Queryset
        # serializer_class
        # return Response
        
        # print(request.user)
        return self.list(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

class ProductDetailView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        # Product.objects.all().order_by('id').get(pk=kwargs['pk'])
        return self.retrieve(request, args, kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, args, kwargs)

class CommentListView(mixins.ListModelMixin, generics.GenericAPIView):
    # mixins.CreateModelMixin (X)
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')

        if product_id:
            return Comment.objects.filter(product_id=product_id).order_by('-id')
        return Comment.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, args, kwargs)

class CommentCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

class CommentDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')

        if product_id:
            # product=product_id, product__pk=product_id 도 가능
            return Comment.objects.filter(product_id=product_id).order_by('-id')
        return Comment.objects.none()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

class LikeCreateView(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.all()

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        
        if Like.objects.filter(member=request.user, product_id=product_id).exists():
            # print(Like.objects.all().filter(member=request.user))
            Like.objects.all().filter(member=request.user, product_id=product_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Like.objects.filter(member=request.user).delete()
        
        return self.create(request, args, kwargs)
