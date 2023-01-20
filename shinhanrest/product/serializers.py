from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Comment, Like

class ProductSerializer(serializers.ModelSerializer):
    # 모델에 없는 필드인데, serializer에만 정의된 필드
    # SerializerMethodField : 함수로 내가 직접 값을 만들게 라는 뜻

    comment_count = serializers.SerializerMethodField() # serializer에서 내가 원하는 custom field 생성 가능
    like_count = serializers.SerializerMethodField()

    # 이름 앞에 get + 값 이름, 인자는 꼭 2개 (self, obj): self= , obj = Product
    def get_comment_count(self, obj):
        return obj.comment_set.all().count()
    
    # 각 제품마다 좋아요 개수 출력
    def get_like_count(self, obj):
        return Like.objects.filter(product=obj).count()

        # 필터 조건으로 product=obj, product_id=obj, product__pk=obj 모두 가능
        #return Comment.objects.filter(product=obj).count() # count() : 총 query 개수
    
    class Meta:
        model = Product
        fields = '__all__' # 모든 필드를 모두 출력

class CommentSerializer(serializers.ModelSerializer): # 가져오기 위한 serializer 이고, 생성하기 위한 serializer 따로 생성

    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer): # 댓글을 생성하기 위한 serializer
    # model에서 member 필드를 hidden field 로 설정
    member = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), # CurrentUserDefault : 사용자 정보를 기본값으로 바로 들어가게 설정
        required=False
    )

    def validate_member(self, value):
        if not value.is_authenticated:
            raise serializers.ValidationError('member is required')
        return value

    # def validate(self, attrs):
    #     request = self.context['request'] # serializer는 view가 아니라서 request가 없다. 
    #     # self.context = view의 class에서 serializer를 직접 세팅한 경우 serializers의 context에 넣어주고 사용할 수 있다
    #     print(request.user)

    #     if request.user.is_authenticated:
    #         attrs['member'] = request.user
    #     else:
    #         raise ValidationError('member is required')

    #     return attrs

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'member': {'required': False}}


class LikeSerializer(serializers.ModelSerializer):
    # 사용자 정보는 header에 넣는 게 아니라(프론트로부터 body에서 받는 게 아니라) 자동으로 전송되는 것
    # 자동으로 member라는 값을 생성하기 위함
    member = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), # CurrentUserDefault : 사용자 정보를 기본값으로 바로 들어가게 설정
        required=False
    )
 
    # validate_필드명 
    def validate_member(self, value):
        # value = request.user
        if not value.is_authenticated:
            raise serializers.ValidationError('member is required')
        return value

    class Meta:
        model = Like
        fields = '__all__'