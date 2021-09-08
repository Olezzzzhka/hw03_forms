from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import User, Post, Group


User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='test group title',
            slug='test_slug',
            description='test description',
        )
        cls.post = Post.objects.create(
            text='test text',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='noname')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_post = Client()
        self.author_post.force_login(self.post.author)

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_techpage(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_about_authorpage(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_grouppage(self):
        response = self.guest_client.get('/group/test_slug/')
        self.assertEqual(response.status_code, 200)

    def test_profilepage(self):
        response = self.guest_client.get('/profile/noname/')
        self.assertEqual(response.status_code, 200)

    def test_postpage(self):
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_author_posteditpage(self):
        response = self.author_post.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_quest_client(self):
        url_and_redirect_way = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post.id}/edit/': f'/auth/login/?next=/posts/{self.post.id}/edit/',
        }

        for url, redirect_way in url_and_redirect_way.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect_way)

    def test_authorized_user_createpage(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_unexistingpage(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
 
    def test_unexistingpage_for_client(self):
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        templates_utl_names = {
            '/': 'index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/noname/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html'
        }

        for adress, template in templates_utl_names.items():
            with self.subTest(adress=adress):
                response = self.author_post.get(adress)
                self.assertTemplateUsed(response, template)
