import time
import base64
import requests

from django.conf import settings
from django.core.cache import cache


SPOTIFY_TOKEN_CACHE_KEY = "spotify_access_token"
SPOTIFY_TOKEN_EXPIRES_AT = "spotify_access_token_expires_at"


class SpotifyAPIError(Exception):
    pass


class SpotifyClient:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.base_url = "https://api.spotify.com/v1"

    def _get_basic_auth_header(self):
        token = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        b64 = base64.b64encode(token).decode("utf-8")
        return {"Authorization": f"Basic {b64}"}

    def get_access_token(self):
        token = cache.get(SPOTIFY_TOKEN_CACHE_KEY)
        expires_at = cache.get(SPOTIFY_TOKEN_CACHE_KEY + "_expires_at")

        now = int(time.time())
        if token and expires_at and now < expires_at - 30:
            return token

        url = "https://accounts.spotify.com/api/token"
        headers = self._get_basic_auth_header()
        data = {"grant_type": "client_credentials"}

        resp = requests.post(url, headers=headers, data=data, timeout=20)
        if resp.status_code != 200:
            raise SpotifyAPIError("Failed to obtain Spotify access token.")

        payload = resp.json()
        token = payload.get("access_token")
        expires_in = int(payload.get("expires_in", 3600))

        cache.set(SPOTIFY_TOKEN_CACHE_KEY, token, expires_in)
        cache.set(SPOTIFY_TOKEN_CACHE_KEY + "_expires_at", int(time.time()) + expires_in, expires_in)

        return token

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def search_shows(self, query, limit=20, offset=0, market=None):
        if not query:
            return {"items": [], "total": 0}

        url = f"{self.base_url}/search"
        params = {"q": query, "type": "show", "limit": limit, "offset": offset}
        if market:
            params["market"] = market

        resp = requests.get(url, headers=self._auth_headers(), params=params, timeout=20)
        if resp.status_code != 200:
            raise SpotifyAPIError("Spotify search request failed.")

        data = resp.json().get("shows", {})
        return {"items": data.get("items", []), "total": data.get("total", 0)}

    def get_show(self, show_id, market=None):
        url = f"{self.base_url}/shows/{show_id}"
        params = {}
        if market:
            params["market"] = market

        resp = requests.get(url, headers=self._auth_headers(), params=params, timeout=20)
        if resp.status_code != 200:
            raise SpotifyAPIError("Spotify show request failed.")

        return resp.json()

    def get_show_episodes(self, show_id, limit=20, offset=0, market=None):
        url = f"{self.base_url}/shows/{show_id}/episodes"
        params = {"limit": limit, "offset": offset}
        if market:
            params["market"] = market

        resp = requests.get(url, headers=self._auth_headers(), params=params, timeout=20)
        if resp.status_code != 200:
            raise SpotifyAPIError("Spotify episodes request failed.")

        data = resp.json()
        return {"items": data.get("items", []), "total": data.get("total", 0)}
