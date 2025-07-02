from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import *

class UserAuthTests(TestCase):
    def test_sign_up(self):
        response = self.client.post(reverse('signUp'), {
            'username': 'testuser',
            'email': 'test@example.com', 
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)



class ActivityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Bien-être')
        self.activity = Activity.objects.create(title='Yoga', description='Relaxation', category=self.category)

    def test_view_activities(self):
        response = self.client.get(reverse('activities'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yoga')

    def test_toggle_favorite(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('toggle_favorite', args=[self.activity.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FavoriteActivity.objects.filter(user=self.user, activity=self.activity).exists())

    def test_remove_favorite(self):
        self.client.login(username='testuser', password='testpass')
        FavoriteActivity.objects.create(user=self.user, activity=self.activity)
        response = self.client.post(reverse('toggle_favorite', args=[self.activity.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FavoriteActivity.objects.filter(user=self.user, activity=self.activity).exists())

class AdminActivityTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_staff=True)

        moderator_group, _ = Group.objects.get_or_create(name='Moderator')
        self.admin.groups.add(moderator_group)

        logged = self.client.login(username='admin', password='adminpass')
        self.assertTrue(logged)

    def test_access_admin_activity_page(self):
        response = self.client.get(reverse('administrator_activities'))
        self.assertEqual(response.status_code, 200)

    def test_admin_create_activity(self):
        response = self.client.post(reverse('add_activity'), {
            'title': 'Meditation',
            'description': 'Relax your mind',
            'category': self.category.id if hasattr(self, 'category') else Category.objects.create(name='Relax').id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Activity.objects.filter(title='Meditation').exists())

    def test_non_admin_access_denied(self):
        user = User.objects.create_user(username='user', password='userpass')
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('administrator_activities'))
        self.assertNotEqual(response.status_code, 200)


class InformationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.client.login(username='admin', password='adminpass')

    def test_add_information(self):
        response = self.client.post(reverse('add_information'), {
            'title': 'Conseil Bien-être',
            'content': 'Buvez de l’eau régulièrement',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Information.objects.filter(title='Conseil Bien-être').exists())


