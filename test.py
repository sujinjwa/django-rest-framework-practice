def test(a=20, b=30): # 인자의 기본값 지정
    print(a, b)

#test(20, 30)
#test() # 기본값 있는 경우 인자 없이 함수 호출 가능
#test(b=50) # 인자 b에만 값 지저앟고 싶은 경우

# 여러 개의 인자(개수가 정해지지 않은 인자)들을 입력 받기 위한 인자 = 가변 인자


def test1(a, b, *args, **kwargs):
    print(a, b)
    print(args) # 빈 튜플
    print(kwargs) # 빈 딕셔너리

test1(10, 20)
test1(10, 20, 30, 40, 50)
test1(10, 20, 30, 40, 50, pk=123, asdf=1234, zxcv=123)