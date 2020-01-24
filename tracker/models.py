from django.db import models
from django.utils import timezone


class Game(models.Model):
    address = models.GenericIPAddressField()
    port = models.IntegerField()
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    players = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = [
            ("address", "port"),
        ]

    def update(self, data):
        self.last_seen = timezone.now()
        self.players = "\n".join(data.get("players", []))
        self.description = data.get("description", "")
        self.save()

    def to_dict(self, **extra):
        return {
            "address": self.address,
            "port": self.port,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "players": [p.strip() for p in self.players.split("\n") if p.strip()],
            "description": self.description.strip(),
            **extra,
        }
