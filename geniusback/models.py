import random

from django.db import models

# Create your models here.
class Members(models.Model):
    nickname = models.CharField(max_length=50)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=100)
    profImg = models.URLField(max_length=512)
    seedCnt = models.IntegerField(default=10)
    createDate = models.DateTimeField(auto_now_add=True)
    createCnt = models.IntegerField(default=0)

    class Meta:
        db_table = 'member'


class Books(models.Model):
    bookName = models.CharField(max_length=50)
    bCreateDate = models.DateTimeField(auto_now_add=True)
    coverImg = models.URLField(max_length=512)
    copyR = models.CharField(max_length=30)
    evalStart = models.IntegerField(default=0)
    writer = models.CharField(max_length=30)
    genre = models.CharField(max_length=50)
    lastPage = models.IntegerField()

    class Meta:
        db_table = 'book'


class MyLibrary(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mylibrary'


class Draft(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    savedAt = models.DateTimeField(auto_now_add=True)
    diff = models.IntegerField(default=0)
    writer = models.CharField(max_length=30, null=True)
    genre = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'draft'

class Intro(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    introMode = models.BooleanField() # 0 : 알콩이(선택형), 1 : 달콩이(작성형)
    subject = models.CharField(max_length=100)
    IntroContent = models.TextField(null=True)

    class Meta:
        db_table = 'intro'


class DraftPage(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    pageNum = models.IntegerField()
    pageContent = models.TextField()

    class Meta:
        db_table = 'draftpage'


class FeedBack(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    feedCap = models.CharField(max_length=512)
    feedContent = models.TextField()

    class Meta:
        db_table = 'feedback'


class Followers(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    following = models.IntegerField(default=0) # 내가 버튼 누른거(내가 구독한 사람 수)
    follower = models.IntegerField(default=0) # 구독자 수
    #팔로우 버튼 눌렀을 떄, 누른사람은 팔로잉 수 증가하고 눌림 당한 사람은 팔로워 수를 증가시키는 로직 필요! -> views에 코딩!
    # 누른 사람 닉네임, 눌림당한 사람 닉네임으로 조회 하면 될 듯

    class Meta:
        db_table = 'follower'


class Flower(models.Model):
    flowerName = models.CharField(max_length=50) # id - 1: 소중한 꽃 피우기, 2 : 나를 표현하기, 3 : 당신은 출석왕, 4 : 당신은 독서왕, 5 : 알콩이와 친해지기, 6 : 달콩이와 친해지기, 7 : 당신은 인싸, 8 : 당신은 훌륭한 작가

    class Meta:
        db_table = 'flower'


class MyForest(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    #장르별로 동화 만든 개수 조회 및 장르 수 제일 많은 장르 찾기 -> Book 테이블에서 genre 속성으로 조회
    #알콩이로 동화 만든 개수 및 달콩이로 동화 만든 개수 조회, 알콩_달콩 중 어떤게 많은지 찾기 -> Intro 테이블에서 introMode 속성으로 알콩이 달콩이 개수 조회
    #유저가 많은 동화 개수 조회(1년별로 조회 가능해야함) -> Book 테이블에서 bCreateDate 속성으로 조회

    class Meta:
        db_table = 'myforest'


class MyFlower(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    getDate = models.DateField() #잠금이 해제 되는 Date를 저장하면 될 듯
    isActive = models.BooleanField() #False : 잠금, True : 잠금해제

    class Meta:
        db_table = 'myflower'
