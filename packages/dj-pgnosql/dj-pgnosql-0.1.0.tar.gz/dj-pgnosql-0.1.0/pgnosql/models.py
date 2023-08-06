from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class KV(models.Model):
    '''
    KV.objects.get(key=..)
    '''

    def __str__(self):
        return '{}:{}'.format(self.key, self.value)

    key = models.CharField(max_length=100, db_index=True)
    value = JSONField(default=dict)
    index = models.CharField(max_length=255, db_index=True, help_text='You can provide an index to make this key searchable')

    time_to_live = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @classmethod
    def set(cls, key, value, time_to_live = 0, index = None):
        data = {
            "key": key,
            "value": value,
            "time_to_live": time_to_live
        }
        if index is not None:
            data['index'] = index
        kv, created = KV.objects.update_or_create(
            key=key, defaults=data)
        return kv

    @staticmethod
    def get(key, default_value=None):
        try:
            return KV.objects.get(key=key).value
        except KV.DoesNotExist:
            return default_value

    @staticmethod
    def delete_key(key):
        return KV.objects.get(key=key).delete()
