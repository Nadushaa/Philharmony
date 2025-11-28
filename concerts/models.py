from django.db import models

class Manager(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    position = models.CharField('Должность', max_length=100)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

class Hall(models.Model):
    hall_name = models.CharField('Название зала', max_length=100)
    capacity = models.IntegerField('Вместимость', null=True, blank=True)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

class Artist(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    amu = models.CharField('Амплуа', max_length=100, blank=True, null=True)
    contact_info = models.TextField('Контактная информация', blank=True, null=True)

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'

class Instrument(models.Model):
    TYPE_CHOICES = [
        ('Струнные', 'Струнные'),
        ('Духовые', 'Духовые'),
        ('Язычковые', 'Язычковые'),
        ('Ударные', 'Ударные'),
        ('Перкуссия', 'Перкуссия'),
        ('Клавишные', 'Клавишные'),
        ('Электромузыкальные', 'Электромузыкальные'),
    ]
    
    CONDITION_CHOICES = [
        ('Отличное', 'Отличное'),
        ('Требует настройки', 'Требует настройки'),
        ('В ремонте', 'В ремонте'),
    ]
    
    name = models.CharField('Наименование', max_length=100)
    type = models.CharField('Тип', max_length=50, choices=TYPE_CHOICES)
    inventory_number = models.CharField('Инвентарный номер', max_length=50, unique=True)
    condition = models.CharField('Состояние', max_length=50, choices=CONDITION_CHOICES, default='Отличное')

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"
class Concert(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Планируется')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class ConcertArtist(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.artist} в {self.concert}"
    
class MusicalWork(models.Model):
    title = models.CharField('Название произведения', max_length=255)
    composer = models.CharField('Композитор', max_length=255)
    duration = models.TimeField('Продолжительность', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.composer}"

class Program(models.Model):
    concert = models.OneToOneField(Concert, on_delete=models.CASCADE, verbose_name='Концерт')
    program_name = models.CharField('Название программы', max_length=255, blank=True)

    def __str__(self):
        return self.program_name or f"Программа {self.concert.title}"

class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название произведения")
    composer = models.CharField(max_length=100, verbose_name="Композитор", blank=True)
    
    def __str__(self):
        if self.composer:
            return f"{self.title} - {self.composer}"
        return self.title

class ProgramWork(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name='Программа')
    work = models.ForeignKey(MusicalWork, on_delete=models.CASCADE, verbose_name='Произведение')
    sequence_order = models.IntegerField('Порядковый номер', default=1)

    class Meta:
        ordering = ['sequence_order']  # ← ТОЛЬКО ЭТО ДОЛЖНО БЫТЬ!

    def __str__(self):
        return f"{self.sequence_order}. {self.work.title}"