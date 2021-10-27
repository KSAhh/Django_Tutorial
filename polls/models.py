import datetime # python의 표준 모듈

from django.db import models
from django.utils import timezone # Django의 시간대 관련 유틸리티 django.utils.timezone 참조

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now()
    datetime.timedelta(days=1)


class Choice(models.Model):
    # ForeignKey : 외래키. 상단의 Qustion 클래스를 참조하겠다는 의미
    # CASCADE : Question 클래스가 삭제되면 Choice 클래스의 question도 삭제됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text