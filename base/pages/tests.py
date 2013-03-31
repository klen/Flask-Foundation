from ..core.tests import FlaskTest
from .models import Page


class PageTest(FlaskTest):

    def test_page(self):
        response = self.client.get('/p/unknown_page/')
        self.assert404(response)

        page1 = self.mixer.blend(
            'base.pages.models.Page', content=self.mixer.random)
        self.assertEqual(Page.route(page1.slug), page1.uri)
        response = self.client.get(page1.uri)
        self.assert200(response)
        self.assertTrue(page1.content in response.data)

        page2 = self.mixer.blend(
            'base.pages.models.Page', content=self.mixer.random, parent=page1)
        with self.assertNumQueries(2):
            self.assertEqual(page2.uri, '/p/{slug1}/{slug2}/'.format(
                slug1=page1.slug, slug2=page2.slug))
            self.assertEqual(page1.uri, '/p/{slug}/'.format(slug=page1.slug))

        self.assertEqual(Page.route(page2.slug), page2.uri)
        response = self.client.get(page2.uri)
        self.assertTrue(page2.content in response.data)

        page3 = self.mixer.blend(
            'base.pages.models.Page', link='http://google.com', parent=page1)
        response = self.client.get(page3.uri)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('http://google.com' in response.data)
