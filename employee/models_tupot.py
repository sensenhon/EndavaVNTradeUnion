from django.db import models
from django.contrib.auth import get_user_model

class TUPOTExportHistory(models.Model):
    filename = models.CharField(max_length=255)
    export_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.filename} ({self.export_time:%d/%m/%Y %H:%M:%S})"
