from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NOname')
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
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        template_pages_names = {
            reverse('posts:index'): 'index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:group_list', kwargs={'slug':'test_slug'}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username':self.user.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id':self.post.id}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit', kwargs={'post_id':self.post.id}
            ): 'posts/create_post.html'
        }

        for reverse_name, template in template_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
