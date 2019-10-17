from django.test import Client, TestCase

from django.contrib.auth.models import User
from .models import Article, Paragraph, ParagraphBatch

client = Client()


class ApiTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user")
        self.user.set_password("password")
        self.user.save()
        client.login(username="user", password="password")
        self.article = self.create_article(
            name="My First Article", theme="Géographie", text="this is text 1"
        )
        for i in range(2, 5):
            Paragraph.objects.create(
                text=f"this is text {i}",
                article=self.article,
                batch=self.article.batches[0],
            )
        self.paragraphs = self.article.paragraphs

    def test_me_values(self):
        response = client.get("/app/me")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["is_certified"], False)

    def create_article(self, name, theme, text, audience="all"):
        article = Article.objects.create(name=name, theme=theme, audience=audience)
        batch = ParagraphBatch.objects.create()
        Paragraph.objects.create(text=text, article=article, batch=batch)
        return article

    def test_get_paragraph(self):
        response = client.get("/app/api/paragraph")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "id": 1,
                "theme": "Géographie",
                "text": "this is text 1",
                "title": "My First Article",
            },
        )

    def test_post_paragraph(self):
        client.post(
            "/app/api/paragraph",
            content_type="application/json",
            data={
                "paragraph": self.paragraphs.first().pk,
                "data": [
                    {"question": {"text": "q1"}, "answer": {"text": "a1", "index": 11}},
                    {"question": {"text": "q2"}, "answer": {"text": "a2", "index": 12}},
                    {"question": {"text": "q3"}, "answer": {"text": "a3", "index": 13}},
                    {"question": {"text": "q4"}, "answer": {"text": "a4", "index": 14}},
                    {"question": {"text": "q5"}, "answer": {"text": "a5", "index": 15}},
                ],
            },
        )

        paragraph = Article.objects.first().paragraphs.first()
        sample_question = paragraph.questions.all()[2]
        sample_answer = sample_question.answers.first()
        self.assertEqual(paragraph.questions.count(), 5)
        self.assertEqual(sample_question.text, "q3")
        self.assertEqual(sample_answer.text, "a3")
        self.assertEqual(paragraph.status, "completed")
        self.assertEqual(paragraph.user.username, "user")
        self.assertEqual(sample_answer.user.username, "user")

    def test_get_paragraph_theme(self):
        for i in range(0, 100):
            self.create_article(
                name=f"article {i}", theme="notmychoice", text=f"text {i}"
            )
        self.create_article(
            name=f"article I like", theme="mychoice", text=f"text I like"
        )
        self.create_article(
            name=f"other article I like", theme="mychoice", text=f"text I like"
        )

        response = client.get("/app/api/paragraph?theme=mychoice")
        self.assertEqual(response.json().get("theme"), "mychoice")

    def test_get_paragraph_pending_only(self):
        response = client.get("/app/api/paragraph")
        self.assertEqual(response.json()["text"], "this is text 1")
        Paragraph.objects.filter(pk__lte=int(response.json()["id"]) + 2).update(
            status="complete"
        )
        response = client.get("/app/api/paragraph")
        self.assertEqual(response.json()["text"], "this is text 4")

    def test_get_paragraph_limits_restricted_articles_to_certified_users(self):
        Article.objects.filter(pk=self.article.pk).update(audience="restricted")
        response = client.get("/app/api/paragraph")
        self.assertEqual(response.json(), {})
        User.objects.filter(pk=self.user.pk).update(email="example@e.gouv.fr")
        client.logout()
        client.login(username="user", password="password")
        response = client.get("/app/api/paragraph")
        self.assertEqual(response.json()["text"], "this is text 1")