from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import SlugField
from django.urls.base import reverse
from django.utils.text import slugify


DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)


THEMES_CHOICES = (
    ('dark', 'dark'),
    ('dark-yellow', 'dark yellow'),
    ('dark-purple', 'dark purple'),
    ('dark-red', 'dark red'),
    ('dark-gray', 'dark gray'),
    ('light', 'light'),
    ('light-yellow', 'light yellow'),
    ('light-purple', 'light purple'),
    ('light-red', 'light red'),
    ('light-black', 'light black'),
)

AVATAR_CHOICES = (
    ('default0', 'default0'),
    ('default1', 'default1'),
    ('default2', 'default2'),
    ('default3', 'default3'),
    ('default4', 'default4'),
    ('default5', 'default5'),
)

CATEGORY_CHOICES = (
    ('general', 'general'),
    ('coding', 'coding'),
    ('sports', 'sports'),
    ('math', 'math'),
    ('history', 'history'),
    ('tech', 'tech'),
    ('science', 'science'),
    ('Astronomy', 'Astronomy'),
    ('Pop', 'Pop'),
    ('Celebrites', 'Celebrites'),
    ('Celebrites', 'Celebrites'),
    ('Celebrites', 'Celebrites'),
)

class User(AbstractUser):
    ''' user model '''
    avatar = models.CharField(max_length=12, choices=AVATAR_CHOICES, default="default3") # avatar
    following = models.ManyToManyField(to="User", related_name="user_following")
    followers = models.ManyToManyField(to="User", related_name="user_followers")
    # interests = models.CharFiel(max_length=16, choiches=INTERESTS_CHOICES)
    theme = models.CharField(max_length=12, choices=THEMES_CHOICES, default="light")

    def get_unread_notifications(self):
        ''' Get the set of all the answers to the questions '''
        return self.notification_set.filter(read=False)

    def get_notifications(self):
        return self.notification_set.all()

    def __str__(self):
        return self.username

    def get_all_themes(self):
        return THEMES_CHOICES

    def get_avatars(self):
        return AVATAR_CHOICES


class Quiz(models.Model):
    ''' Quiz model '''
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120) #56
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default="general")
    slug = SlugField(max_length=200, unique=True, default=None, blank=True)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_absolute_url(self):
        ''' Get the url link'''
        return reverse('quiz', kwargs={'slug': self.slug})

    def get_questions(self):
        ''' Get the set of all the questions '''
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quizes'

    def save(self, *args, **kwargs):
        ''' On save slugfy the quiz url '''
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        ''' Get the set of all the answers to the questions '''
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.user.username}[{self.score}] in {self.quiz.name}"


class Notification(models.Model):
    ''' User notification '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    desc = models.CharField(max_length=264)

    def __str__(self) -> str:
        return f"{self.user} - {self.name}"
