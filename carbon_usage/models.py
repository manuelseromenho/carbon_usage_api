from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    usage_types = models.ManyToManyField(
        "carbon_usage.UsageType", related_name="user_info", through="Usage"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name


class Usage(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        "User", related_name="usages", on_delete=models.SET_NULL, null=True
    )
    usage_type_id = models.ForeignKey(
        "carbon_usage.UsageType",
        related_name="usages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    usage_at = models.DateTimeField(auto_now_add=True, blank=True)
    amount = models.FloatField()

    class Meta:
        verbose_name = "Usage"
        verbose_name_plural = "Usages"

    def __str__(self):
        date_time = self.usage_at.strftime("%d-%m-%Y %H:%M:%S")
        user_name = self.user_id.name
        usage_type = self.usage_type_id.name
        return f"Date Time: {date_time} User:{user_name} Usage Type:{usage_type}"


class UsageType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # unit = models.CharField(choices=UNIT_CHOICES, default='', max_length=25)
    unit = models.CharField(max_length=25)
    factor = models.FloatField()

    class Meta:
        verbose_name = "Usage Type"
        verbose_name_plural = "Usage Types"

    def __str__(self):
        return self.name
