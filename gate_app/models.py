from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Test(models.Model):
    name = models.CharField(max_length=200)
    subject_id = models.IntegerField()
    topic_id = models.IntegerField()

    def __str__(self):
        return self.name

class TestAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.test} - {self.score}/{self.total}"
