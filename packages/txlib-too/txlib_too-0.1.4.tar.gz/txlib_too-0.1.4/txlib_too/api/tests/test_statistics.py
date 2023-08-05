# -*- coding: utf-8 -*-
import pytest

from txlib_too.api.statistics import Statistics
from txlib_too.api.tests.utils import clean_registry, get_mock_response
from txlib_too.tests.compat import patch


@pytest.fixture(autouse=True)
def auto_clean_registry():
    """Run the test and the remove the `http_handler` entry from
    the registry."""
    clean_registry()


class TestStatisticsModel():
    """Test the functionality of the Statistics model."""

    @patch('txlib_too.http.http_requests.requests.request')
    def test_get_populates_object(self, mock_request):
        mock_response = """{
                "en": {
                    "reviewed_percentage": "0%",
                    "completed": "100%",
                    "untranslated_words": 0,
                    "last_commiter": "diegobz",
                    "reviewed": 0,
                    "translated_entities": 2165,
                    "translated_words": 16629,
                    "last_update": "2014-02-20 14:25:06",
                    "untranslated_entities": 0
                },
            }"""
        mock_request.return_value = get_mock_response(
            200, mock_response,
        )
        obj = Statistics.get(project_slug='sample_project', slug='new_resource')

        assert obj == mock_response