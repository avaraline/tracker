import datetime

import requests
from django.conf import settings
from django.db import models
from django.utils import timezone


class Game(models.Model):
    address = models.GenericIPAddressField()
    port = models.IntegerField()
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    players = models.TextField(blank=True)
    description = models.TextField(blank=True)
    password = models.BooleanField(default=False)
    discord_msgid = models.TextField(blank=True)

    class Meta:
        unique_together = [
            ("address", "port"),
        ]

    @classmethod
    def prune(cls):
        cutoff = timezone.now() - datetime.timedelta(
            seconds=settings.TRACKER_PRUNE_SECONDS
        )

        if settings.TRACKER_DISCORD_WEBHOOK:
            # cross out the game in discord
            for game in cls.objects.filter(last_seen__lt=cutoff):
                if not game.discord_msgid:
                    continue
                try:
                    requests.patch(
                        settings.TRACKER_DISCORD_WEBHOOK + f"/messages/{game.discord_msgid}",
                        json={ "content": "~~" + game.discord_msg() + "~~" })
                except:
                    pass

        cls.objects.filter(last_seen__lt=cutoff).delete()

    def update(self, data):
        self.last_seen = timezone.now()
        self.players = "\n".join(data.get("players", []))
        self.description = data.get("description", "")
        self.password = data.get("password", "")

        self.save()

    def discord_msg(self):
        players = self.player_list()
        if len(players) < 1:
            return ""
        host = players[0]
        address = self.address
        description = self.description
        myid = settings.TRACKER_DISCORD_ROLE_ID

        msg = f"<@&{myid}> **{host}** is hosting at {address}"

        if len(description) > 0:
            msg += f" - *{description}*"

        if len(players) == 2:
            msg += f" - {players[1]} is playing"

        if len(players) > 2:
            plst = ", ".join(players[1:])
            msg += f" - {plst} are playing"

        return msg

    def handle_notification(self, existing_msg):
        d_url = settings.TRACKER_DISCORD_WEBHOOK
        if not d_url:
            return
        new_msg = self.discord_msg()
        if not self.discord_msgid:
            # post new message
            resp = requests.post(
                # tell discord to be synchronous
                # so we can get the message id
                d_url + "?wait=true",
                json={
                    "username": "Tracker",
                    "content": new_msg,
                },
            )
            d_meta = resp.json()
            msgid = d_meta["id"]
            self.discord_msgid = msgid
            self.save()
        else:
            if existing_msg != new_msg:
                # update existing message
                resp = requests.patch(
                    d_url + f"/messages/{self.discord_msgid}",
                    json={ "content": new_msg }
                )

    def player_list(self):
        return [p.strip() for p in self.players.split("\n") if p.strip()]

    def to_dict(self, **extra):
        return {
            "address": self.address,
            "port": self.port,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "players": self.player_list(),
            "description": self.description.strip(),
            "password": self.password,
            **extra,
        }
