from django.db import models
import pandas as pd


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def create_from_dataframe(cls, df):
        my_list = []
        for x in df.T.to_dict().values():
            my_list.append(cls(**x))

        cls.objects.bulk_create(my_list)