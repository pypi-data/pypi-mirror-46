from aiohttp import web

from . import oauth2_app


if __name__ == "__main__":
    app = oauth2_app(
        "a1b8c7904865ac38baba",
        "147d82d8ded7a74899fcc4da2b61f8d305bf81c5",
        "https://github.com/login/oauth/authorize",
        "https://github.com/login/oauth/access_token",
    )

    web.run_app(app)
