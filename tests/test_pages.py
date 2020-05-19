import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from wagtail.core.models import Site
from wagtail.contrib.redirects.models import Redirect
from wagtail.tests.utils import WagtailTestUtils

from tests.testapp import factories


def unpublish_page(page):
    revision = page.save_revision()
    revision.unpublish()
    return page


class TestPageMove(TestCase, WagtailTestUtils):
    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.user = User.objects.create_superuser(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )

    def test_move_creates_redirects(self):
        test_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
            parent=self.site.root_page,
            title='Automatic redirects test index page',
            slug='index-page',
            subtitle='Test subtitle',
            body='<p>Test body</p>',
        )

        test_sub_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
            parent=test_index_page,
            title='Automatic redirects test index page',
            slug='index-page',
            subtitle='Test subtitle',
            body='<p>Test body</p>',
        )

        test_page1 = factories.AutomaticRedirectsTestPageFactory(
            parent=test_sub_index_page,
            title='Test Page 1',
            slug='test-page-1'
        )

        self.client.login(
            username=self.user.username, password='johnpassword'
        ) == True

        resp = self.client.post(
            reverse('wagtailadmin_pages:move_confirm', args=(
                test_page1.id,
                test_index_page.id)
            ),
        )

        assert Redirect.objects.count() == 1

        response = self.client.get('/index-page/test-page-1/')
        assert response.status_code == 200

        response = self.client.get('/index-page/index-page/test-page-1/')
        assert response.status_code == 301

    def test_moving_parent_created_redirect_for_child_as_well(self):
        test_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
            parent=self.site.root_page,
            title='Automatic redirects test index page',
            slug='index-page',
            subtitle='Test subtitle',
            body='<p>Test body</p>',
        )

        test_sub_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
            parent=test_index_page,
            title='Automatic redirects test index page',
            slug='index-page',
            subtitle='Test subtitle',
            body='<p>Test body</p>',
        )

        test_page1 = factories.AutomaticRedirectsTestPageFactory(
            parent=test_sub_index_page,
            title='Test Page 1',
            slug='test-page-1'
        )

        test_child_page1 = factories.AutomaticRedirectsTestPageFactory(
            parent=test_page1,
            title='Test Child Page 1',
            slug='test-child-page-1'
        )

        self.client.login(
            username=self.user.username, password='johnpassword'
        ) == True

        resp = self.client.post(
            reverse('wagtailadmin_pages:move_confirm', args=(
                test_page1.id,
                test_index_page.id)
            ),
        )

        assert Redirect.objects.count() == 2

        response = self.client.get(
            '/index-page/test-page-1/test-child-page-1/'
        )
        assert response.status_code == 200

        response = self.client.get(
            '/index-page/index-page/test-page-1/test-child-page-1/'
        )
        assert response.status_code == 301

    def test_only_published_pages_gets_redirected(self):
        test_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
            parent=self.site.root_page,
            title='Automatic redirects test index page',
            slug='index-page',
            subtitle='Test subtitle',
            body='<p>Test body</p>',
        )

        assert test_index_page.live == True

        test_sub_index_page = factories.AutomaticRedirectsTestIndexPageFactory(
            parent=test_index_page,
            title='Automatic redirects test index page',
            slug='index-page',
            subtitle='Test subtitle',
            body='<p>Test body</p>',
        )

        test_page1 = factories.AutomaticRedirectsTestPageFactory(
            parent=test_sub_index_page,
            title='Test Page 1',
            slug='test-page-1'
        )

        test_page1.unpublish()

        self.client.login(
            username=self.user.username, password='johnpassword'
        ) == True

        resp = self.client.post(
            reverse('wagtailadmin_pages:move_confirm', args=(
                test_page1.id,
                test_index_page.id)
            ),
        )

        assert Redirect.objects.count() == 0
