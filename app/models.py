from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def total_tags(self):
        return self.questions.count()


class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by('-answers')

    def new(self):
        return self.order_by("-datetime")


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)


class Like(models.Model):
    LIKE = 1
    remove = 0
    VOTES = (
        (LIKE, 'Нравится'),
        (remove, 'Убрал голос')
    )
    vote = models.SmallIntegerField(choices=VOTES)
    author = models.ForeignKey('Author', related_name='likes', on_delete=models.PROTECT)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    objects = LikeManager()

    def __str__(self):
        return f"{self.author.name + self.author.surname} {self.vote}"


class Question(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, related_name='questions')
    datetime = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like', related_query_name='questions')
    context = models.TextField(max_length=512)
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions')
    objects = QuestionManager()


class Answer(models.Model):
    title = models.CharField(max_length=256)
    context = models.CharField(max_length=256)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, related_name='answers')
    datetime = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation('Like', related_query_name='answers')

    def __str__(self):
        return f"{self.author.surname + self.author.name} answer"


class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.surname}"


class QuestionInst(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answers = models.ManyToManyField('Answer', blank=True)


def user_directory_path(instance, filename):
    return 'user_{0}/ {1}'.format(instance.author.id, filename)


class UserAccount(models.Model):
    author = models.OneToOneField('Author', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
