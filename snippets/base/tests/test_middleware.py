from mock import Mock, patch

from django.test import RequestFactory
from django.urls import Resolver404

from snippets.base.middleware import FetchSnippetsMiddleware
from snippets.base.tests import TestCase


class FetchSnippetsMiddlewareTests(TestCase):
    def setUp(self):
        self.get_response_mock = Mock()
        self.middleware = FetchSnippetsMiddleware(self.get_response_mock)

    @patch('snippets.base.middleware.resolve')
    @patch('snippets.base.middleware.fetch_snippets')
    def test_resolve_fetch_snippets_match(self, fetch_snippets, resolve):
        """
        If resolve returns a match to the fetch_snippets view, return the
        result of the view.
        """
        request = Mock()
        result = resolve.return_value
        result.func = fetch_snippets
        result.args = (1, 'asdf')
        result.kwargs = {'blah': 5}

        self.assertEqual(self.middleware(request), fetch_snippets.return_value)
        fetch_snippets.assert_called_with(request, 1, 'asdf', blah=5)

    @patch('snippets.base.middleware.resolve')
    @patch('snippets.base.middleware.fetch_json_snippets')
    def test_resolve_fetch_json_snippets_match(self, fetch_json_snippets, resolve):
        """
        If resolve returns a match to the fetch_json_snippets view,
        return the result of the view.
        """
        request = Mock()
        result = resolve.return_value
        result.func = fetch_json_snippets
        result.args = (1, 'asdf')
        result.kwargs = {'blah': 5}

        self.assertEqual(self.middleware(request), fetch_json_snippets.return_value)
        fetch_json_snippets.assert_called_with(request, 1, 'asdf', blah=5)

    @patch('snippets.base.middleware.resolve')
    @patch('snippets.base.middleware.fetch_snippets')
    def test_resolve_no_match(self, fetch_snippets, resolve):
        """
        If resolve doesn't return a match to the fetch_snippets view, return
        None.
        """
        request = Mock()
        result = resolve.return_value
        result.func = lambda request: 'asdf'

        self.assertEqual(self.middleware(request), self.get_response_mock())

    def test_unknown_url(self):
        request = RequestFactory().get('/admin')
        self.assertRaises(Resolver404, self.middleware, request)
