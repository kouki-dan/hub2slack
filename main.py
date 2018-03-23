
import os

import requests
from aiohttp import web


def post_to_slack(tag, pusher, repo_name, repo_url, webhook_url):
    payload = f"""
{{
    "attachments": [
        {{
			"title": "{repo_name}の新しいビルドです",
			"title_link": "{repo_url}",
			"color": "#3498db",
			"fields": [
				{{
                        "title": "タグ",
                        "value": "{tag}",
                        "short": true
				}},
				{{
                        "title": "配信者",
                        "value": "{pusher}",
                        "short": true
				}}
			]
        }}
    ]
}}
    """

    requests.post(webhook_url, data={"payload": payload})

async def index(reqeust):
    return web.Response(text="I'm alive")

async def dockerhub(request):
    data = await request.json()
    tag = data["push_data"]["tag"]
    pusher = data["push_data"]["pusher"]
    repo_name = data["repository"]["repo_name"]
    repo_url = data["repository"]["repo_url"]
    webhook_url = request.rel_url.query["slack_webhook"]

    post_to_slack(tag, pusher, repo_name, repo_url, webhook_url)

    return web.Response(text="OK")

def get_app():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_post("/dockerhub", dockerhub)
    return app

def main():
    app = get_app()
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)

if __name__ == "__main__":
    main()

