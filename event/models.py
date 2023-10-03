from django.db import models
from accounts.models import User


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Day(models.Model):
    DAY_CHOICES = (
        ('수요일', '수요일'),
        ('목요일', '목요일'),
        ('금요일', '금요일'),
    )
    DATE_CHOICES = (
        (10, 10),
        (11, 11),
        (12, 12),
    )

    day = models.CharField(choices=DAY_CHOICES, max_length=5)
    date = models.IntegerField(choices=DATE_CHOICES)

    def __str__(self):
        return f'{self.day}'

class Category(models.Model):
    # CATEGORY_CHOICES = (
    #     ('음식', '음식'),
    #     ('굿즈', '굿즈'),
    #     ('체험', '체험'),
    #     ('기타', '기타'),
    # )

    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    category = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.category}'

class Event(TimeStamp):
    COLLEGE_CHOICES = (
        ('교육관', '교육관'),
        ('대강당', '대강당'),
        ('신세계관', '신세계관'),
        ('생활관', '생활관'),
        ('정문', '정문'),
        ('포스코관', '포스코관'),
        ('학문관', '학문관'),
        ('휴웃길', '휴웃길'),
        ('잔디광장', '잔디광장'),
        ('학문관광장', '학문관광장'),
        ('스포츠트랙', '스포츠트랙')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ManyToManyField(Day, related_name='events')
    college = models.CharField(choices=COLLEGE_CHOICES, max_length=20)
    category = models.ManyToManyField(Category, related_name='events')
    name = models.TextField()
    number = models.CharField(max_length=10, blank=True)
    thumnail = models.TextField(null=True, blank=True)
    opened = models.BooleanField(default=False)
    hashtag = models.TextField(null=True, blank=True)
    description = models.TextField(blank=True)
    like = models.ManyToManyField(User, related_name='events', blank=True)
    busy = models.BooleanField(default=False)
    began = models.BooleanField(default=False)
    wheelchair = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    contact = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Image(TimeStamp):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.TextField()


class Menu(TimeStamp):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='menus')
    menu = models.TextField()
    price = models.PositiveIntegerField()
    is_soldout = models.BooleanField(default=False)
    like = models.ManyToManyField(User, related_name='menus', blank=True)

    def __str__(self):
        return "{} - {}".format(self.menu,self.event.name)

class Comment(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

class Notice(TimeStamp):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notices')
    content = models.TextField()

class Time(TimeStamp):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='times')
    starttime = models.TextField(null=True,blank= True)
    finishtime = models.TextField(null=True,blank= True)