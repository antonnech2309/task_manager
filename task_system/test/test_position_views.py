from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_system.models import Position

POSITION_URL = reverse("task_system:position-list")


class PublicPositionTest(TestCase):
    def test_login_required(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="test_name"
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            position=self.position
        )
        self.client.force_login(self.user)

    def test_retrieve_position(self):
        res = self.client.get(POSITION_URL)
        self.assertEqual(res.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(
            list(res.context["position_list"]),
            list(positions)
        )

    def test_create_position(self):
        response = self.client.post(
            reverse("task_system:position-create"),
            {"name": "new_position"}
        )
        self.assertRedirects(response, reverse("task_system:position-list"))
        self.assertTrue(
            Position.objects.filter(name="new_position").exists()
        )

    def test_update_position(self):
        res = self.client.post(
            reverse("task_system:position-update", args=[1]),
            {"name": "updated_name"}
        )
        self.assertRedirects(res, reverse("task_system:position-list"))
        self.assertTrue(
            Position.objects.filter(name="updated_name").exists()
        )

    def test_delete_position(self):
        response = self.client.post(
            reverse(
                "task_system:position-delete",
                args=[1]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Position.objects.filter(id=1).exists()
        )
