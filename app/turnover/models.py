from django.db import models


class Turnover(models.Model):
    file = models.CharField(max_length=100)

    def __str__(self) -> str:
        return super().__str__()
