from django.core.management.base import BaseCommand
from faker import Faker
from random import choice

from app.models import Question, Answer, Tag, Like, Author, QuestionInst


class Command(BaseCommand):
    help = 'Мусор в бд'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Количество мусора')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        users_count = ratio
        for _ in range(users_count):
            username = fake.unique.first_name()
            surname = fake.unique.last_name()
            password = fake.password()
            Author.objects.create(name=username, surname=surname, password=password)

        questions_count = ratio * 10
        for _ in range(questions_count):
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=3)
            user = choice(Author.objects.all())
            Question.objects.create(title=title, context=content, author=user)

        answers_count = ratio * 100
        for _ in range(answers_count):
            content = fake.paragraph(nb_sentences=2)
            user = choice(Author.objects.all())
            question = choice(Question.objects.all())
            answer = Answer.objects.create(title=fake.sentence(nb_words=3), context=content, author=user)
            question.questioninst_set.create().answers.add(answer)

        tags_count = ratio
        for _ in range(tags_count):
            name = fake.unique.word()
            tag = Tag.objects.create(name=name)
            for question in Question.objects.all():
                question.tags.add(tag)  # assuming we want all questions to have all tags

        ratings_count = ratio * 200
        for _ in range(ratings_count):
            user = choice(Author.objects.all())
            question = choice(Question.objects.all())
            Like.objects.create(author=user, vote=choice(Like.VOTES)[0],
                                content_object=question)  # assuming we want to relate likes to questions for this case

        self.stdout.write(self.style.SUCCESS('ДБ в мусоре'))
