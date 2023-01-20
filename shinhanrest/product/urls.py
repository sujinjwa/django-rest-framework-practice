from django.urls import path
from . import views

urlpatterns = [
    path('/<int:pk>', views.ProductDetailView.as_view()), # <int:pk> : 숫자형을 변수명이 pk인 변수에 담아서 가변인자로 보낸다는 의미
    path('', views.ProductListView.as_view()),
    path('/<int:product_id>/comment', views.CommentListView.as_view()), # 실제 서비스에서 이러한 url 사용 x
    path('/comment', views.CommentCreateView.as_view()),
    path('/like', views.LikeCreateView.as_view()),


    path('/<int:product_id>/comment/<int:pk>', views.CommentDetailView.as_view()),
]