import datetime
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from .models import Game


def index(request):
    return render(request, "index.html", {"games": Game.objects.all(),})


class APIView(View):
    @property
    def json(self):
        if not hasattr(self, "_json_cache"):
            self._json_cache = json.loads(self.request.body) if self.request.body else {}
        return self._json_cache

    def dispatch(self, request, *args, **kwargs):
        try:
            result = super().dispatch(request, *args, **kwargs)
            if isinstance(result, HttpResponseBase):
                return result
            return JsonResponse(result, json_dumps_params={"indent": 2})
        except (Http404, ObjectDoesNotExist):
            return JsonResponse({"error": "Record not found."}, status=404)
        except Exception as ex:
            return JsonResponse({"error": str(ex)}, status=500)


class GamesAPI(APIView):
    @property
    def request_ip(self):
        try:
            return self.request.META["HTTP_X_FORWARDED_FOR"].split(",")[0]
        except Exception:
            return self.request.META["REMOTE_ADDR"]

    def prune(self):
        cutoff = timezone.now() - datetime.timedelta(seconds=settings.TRACKER_PRUNE_SECONDS)
        Game.objects.filter(last_seen__lt=cutoff).delete()

    def get(self, request, *args, **kwargs):
        self.prune()
        return {
            "games": [g.to_dict() for g in Game.objects.all()],
        }

    def post(self, request, *args, **kwargs):
        game, created = Game.objects.get_or_create(address=self.request_ip, port=int(self.json.get("port", 19567)))
        game.update(self.json)
        return game.to_dict()
