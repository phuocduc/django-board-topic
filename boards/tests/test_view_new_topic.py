from django.test import TestCase
from ..models import Topic, Board
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..forms import NewTopicForm
from ..views import new_topics

class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="testing", description='just for test')
        User.objects.create_user(username='admin', email='admin@gamin.com', password='Avatar@123')
        self.client.login(username='admin', password='Avatar@123')

    def test_topic_view_success_status_codeee(self):
        url = reverse('new_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_topic_view_not_found_status_code(self):
        url = reverse('new_topics', kwargs={'pk': 6})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def new_topic_url_resolve_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topics)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topics', kwargs={'pk': 1})
        board_topic_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topic_url))

    def test_csrf(self):
        new_topic_url = reverse('new_topics', kwargs={'pk':1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    def test_contains_form(self):
        new_topic_url = reverse('new_topics', kwargs={'pk': 1})
        reponse = self.client.get(new_topic_url)
        form = reponse.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
        #     def test_new_topic_valid_post_data(self):
