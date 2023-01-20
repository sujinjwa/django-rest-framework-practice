from django.db import models
from member.models import Member # 객체를 직접 임포트하는 방법도 있음. 하지만... 객체를 문자열로 표현하는 방법 존재!
# 객체를 직접 임포트하는 경우 순환참조로 인한 에러가 발생할 위험이 있다

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='상품명')
    price = models.IntegerField(verbose_name='가격')
    product_type = models.CharField(max_length=8, verbose_name='상품 유형',
        choices=(
            ('단품', '단품'),
            ('세트', '세트'),
        )
    )
    tstamp = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

    class Meta:
        db_table = 'shinhan_project'
        verbose_name = '상품'
        verbose_name_plural = '상품'


class Comment(models.Model):
    # Member가 아닌 'member.Member'로 명시하여, 
    # django에서는 "앱이름.모델명" 으로 특정 모델을 가리킬 수 있다
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE, verbose_name='사용자')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')
    comment = models.TextField(verbose_name='내용')
    tstamp = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

    class Meta:
        db_table = 'shinhan_product_comment'
        verbose_name = '상품 댓글'
        verbose_name_plural = '상품 댓글'

class Like(models.Model):
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE, verbose_name='사용자')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')

    class Meta:
        db_table = 'shinhan_product_like'
        verbose_name = '상품 좋아요'
        verbose_name_plural = '상품 좋아요'