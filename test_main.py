
from unittest.mock import patch, MagicMock

import pytest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from main import get_app, post_to_slack


hub_payload = """{
  "callback_url": "https://registry.hub.docker.com/u/svendowideit/testhook/hook/2141b5bi5i5b02bec211i4eeih0242eg11000a/",
  "push_data": {
    "images": [
        "27d47432a69bca5f2700e4dff7de0388ed65f9d3fb1ec645e2bc24c223dc1cc3",
        "51a9c7c1f8bb2fa19bcd09789a34e63f35abb80044bc10196e304f6634cc582c",
        "..."
    ],
    "pushed_at": 1417566161,
    "pusher": "trustedbuilder",
    "tag": "latest"
  },
  "repository": {
    "comment_count": "0",
    "date_created": 1417494799,
    "description": "",
    "dockerfile": "Dockerfile detail",
    "full_description": "Docker Hub based automated build from a GitHub repo",
    "is_official": false,
    "is_private": true,
    "is_trusted": true,
    "name": "testhook",
    "namespace": "svendowideit",
    "owner": "svendowideit",
    "repo_name": "svendowideit/testhook",
    "repo_url": "https://registry.hub.docker.com/u/svendowideit/testhook/",
    "star_count": 0,
    "status": "Active"
  }
}
"""

class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return get_app()

    @unittest_run_loop
    async def test_index(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        text = await resp.text()
        assert "I" in text

    @unittest_run_loop
    async def test_dockerhub(self):

        with patch("main.post_to_slack") as mock:
            resp = await self.client.request("POST", "/dockerhub?slack_webhook=https://hooks.slack.com/services/spam/ham/egggggggggggggs", data=hub_payload)
        mock.assert_called_once_with("latest", "trustedbuilder", "svendowideit/testhook", "https://registry.hub.docker.com/u/svendowideit/testhook/", "https://hooks.slack.com/services/spam/ham/egggggggggggggs")
        assert resp.status == 200
        text = await resp.text()
        assert "OK" in text

    def test_slack_message_should_parse_to_json(self):
        with patch("main.requests") as mock:
            post_to_slack("tag", "pusher", "reponame", "repourl", "hookurl")
            assert "hookurl" == mock.post.call_args[0][0]
            data = mock.post.call_args[1]["data"]["payload"]
            import json
            try:
                json.loads(data)
            except json.decoder.JSONDecodeError:
                pytest.fail("Payload cannot be parsed")

