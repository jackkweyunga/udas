from django.db import models


# Create your models here.
class SystemLogs(models.Model):
    
    """System Logs"""
    
    log_content = models.TextField(default="")
    isModelLog = models.BooleanField(default=True)
    model_logged = models.CharField(max_length=1024, default="")
    date_logged = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f"DATETIME: {self.date_logged}   ISMODELLOG:{self.isModelLog}   MODEL: {self.model_logged}   MESSAGE: {self.log_content}"

    def log_level(self):
        return 1 if str(self.log_content).lower().count("failed") > 0 else 0

