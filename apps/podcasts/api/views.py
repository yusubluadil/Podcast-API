from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework import status

from .pagination import DefaultLimitOffsetPagination
from .serializers import (
    ShowSerializer,
    EpisodeSerializer
)
from ..services.spotify_client import (
    SpotifyClient,
    SpotifyAPIError
)


class PodcastSearchView(ListAPIView):
    serializer_class = ShowSerializer
    pagination_class = DefaultLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        market = request.query_params.get("market")
        limit = self.paginator.get_limit(request) if self.paginator else 20
        offset = self.paginator.get_offset(request) if self.paginator else 0

        client = SpotifyClient()
        try:
            result = client.search_shows(query=query, limit=limit, offset=offset, market=market)
        except SpotifyAPIError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        items = result["items"]
        total = result["total"]

        page = self.paginator.paginate_queryset(items, request, view=self)
        serializer = self.get_serializer(page, many=True)
        response = self.paginator.get_paginated_response(serializer.data)
        response.headers["X-Total-Count"] = str(total)
        return response


class PodcastDetailView(RetrieveAPIView):
    serializer_class = ShowSerializer
    lookup_url_kwarg = "showId"

    def retrieve(self, request, *args, **kwargs):
        show_id = kwargs.get(self.lookup_url_kwarg)
        market = request.query_params.get("market")

        client = SpotifyClient()
        try:
            data = client.get_show(show_id, market=market)
        except SpotifyAPIError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        serializer = self.get_serializer(data)
        return Response(serializer.data)


class PodcastEpisodesView(ListAPIView):
    serializer_class = EpisodeSerializer
    pagination_class = DefaultLimitOffsetPagination
    lookup_url_kwarg = "showId"

    def list(self, request, *args, **kwargs):
        show_id = kwargs.get(self.lookup_url_kwarg)
        market = request.query_params.get("market")
        limit = self.paginator.get_limit(request) if self.paginator else 20
        offset = self.paginator.get_offset(request) if self.paginator else 0

        client = SpotifyClient()
        try:
            result = client.get_show_episodes(show_id, limit=limit, offset=offset, market=market)
        except SpotifyAPIError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        items = result["items"]
        total = result["total"]

        page = self.paginator.paginate_queryset(items, request, view=self)
        serializer = self.get_serializer(page, many=True)

        response = self.paginator.get_paginated_response(serializer.data)
        response.headers["X-Total-Count"] = str(total)
        return response
