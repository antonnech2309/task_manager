from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_system.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="test_position"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
            position=self.position
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            position=self.position
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_system_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse(
            "admin:task_system_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)
