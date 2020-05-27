from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board
from ..views import TopicListView

class BoardTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name= 'Django', description = 'web framework newbie')
    
    def test_board_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_board_topic_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 5})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_urls_resolve_board_topic_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_view_contain_link_navigation(self):
        board_topic_url = reverse('board_topics', kwargs={'pk':1})
        home_url = reverse('home')
        new_topic = reverse('new_topics', kwargs={'pk':1})
        response = self.client.get(board_topic_url)
        self.assertContains(response, 'href="{0}"'.format(home_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic))