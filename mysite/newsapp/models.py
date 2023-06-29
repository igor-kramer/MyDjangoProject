from django.db import models
from django.urls import reverse


class HousingType(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "HousingType"
        verbose_name_plural = "HousingTypes"


class NumberOfRooms(models.Model):
    quantity = models.SmallIntegerField()

    class Meta:
        verbose_name = "NumberOfRoom"
        verbose_name_plural = "NumberOfRooms"


class Housing(models.Model):
    housing_type = models.ForeignKey(HousingType, on_delete=models.PROTECT)
    number_of_room = models.ForeignKey(NumberOfRooms, on_delete=models.PROTECT)
    address = models.TextField(null=True, blank=True)
    square = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Housing"
        verbose_name_plural = "Housings"


class News(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse('housing_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "New"
        verbose_name_plural = "News"
