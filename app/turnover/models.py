from django.db import models


class Turnover(models.Model):
    file = models.FileField(upload_to='turnover/uploads/')

    def __str__(self) -> str:
        return super().__str__()
