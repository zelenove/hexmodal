from django.db import models


class StatusChoices(models.TextChoices):
    PASSING = "PASSING", "Passing"
    FAILING = "FAILING", "Failing"


class Device(models.Model):
    latest_status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        blank=True,
        null=True,
    )
    devEUI = models.CharField(max_length=16, unique=True)


class Payload(models.Model):
    fCnt = models.IntegerField()
    data = models.TextField()
    device = models.ForeignKey(
        Device,
        to_field="devEUI",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        blank=True,
        null=True,
    )


