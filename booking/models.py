from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Schedule(models.Model):
    """予約スケジュール."""
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    name = models.CharField('予約者名', max_length=255)
    number = models.IntegerField('人数')
    #nature_number = models.IntegerField('人数',validators=[MinValueValidator(1)], null=True)
    #tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))
    #tel_number = models.CharField(validators=[tel_number_regex], max_length=15, verbose_name='電話番号')
    tel = models.CharField('電話番号', max_length=15, null=True)
    #staff = models.ForeignKey('Staff', verbose_name='スタッフ', on_delete=models.CASCADE)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        #return f'{self.name} {self.number} {start} ~ {end}'
        return f'{self.name} {self.number} {start} ~ {end} {self.tel}'