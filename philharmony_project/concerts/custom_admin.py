from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import *

# Кастомный сайт админки
class PhilharmonyAdminSite(admin.AdminSite):
    site_header = "PhilHarmony Manager - Панель управления"
    site_title = "PhilHarmony Admin"
    index_title = "🎵 Добро пожаловать в систему управления филармонией"
    
    def index(self, request, extra_context=None):
        # Добавляем статистику на главную страницу админки
        extra_context = extra_context or {}
        extra_context['stats'] = {
            'total_concerts': Concert.objects.count(),
            'planned_concerts': Concert.objects.filter(status='Планируется').count(),
            'total_artists': Artist.objects.count(),
            'total_instruments': Instrument.objects.count(),
            'halls_count': Hall.objects.count(),
            'works_count': MusicalWork.objects.count(),
            'programs_count': Program.objects.count(),
        }
        return super().index(request, extra_context)

# Создаем экземпляр кастомной админки
philharmony_admin = PhilharmonyAdminSite(name='philharmony_admin')

# Inline для артистов концерта
class ConcertArtistInline(admin.TabularInline):
    model = ConcertArtist
    extra = 1
    verbose_name = "Участие артиста"
    verbose_name_plural = "Артисты концерта"

# Inline для произведений в программе
class ProgramWorkInline(admin.TabularInline):
    model = ProgramWork
    extra = 1
    verbose_name = "Произведение в программе"
    verbose_name_plural = "Произведения в программе"
    ordering = ['sequence_order']

# Кастомные классы админки с русскими названиями
@admin.register(Manager, site=philharmony_admin)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position']
    search_fields = ['full_name', 'position']
    list_display_links = ['full_name']
    verbose_name = "Менеджер"
    verbose_name_plural = "Менеджеры"

@admin.register(Hall, site=philharmony_admin)
class HallAdmin(admin.ModelAdmin):
    list_display = ['hall_name', 'capacity']
    search_fields = ['hall_name']
    list_filter = ['capacity']
    verbose_name = "Зал"
    verbose_name_plural = "Залы"

@admin.register(Artist, site=philharmony_admin)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'amu', 'contact_info_short']
    list_filter = ['amu']
    search_fields = ['full_name']
    list_per_page = 20
    verbose_name = "Артист"
    verbose_name_plural = "Артисты"
    
    def contact_info_short(self, obj):
        return obj.contact_info[:50] + "..." if obj.contact_info and len(obj.contact_info) > 50 else obj.contact_info
    contact_info_short.short_description = "Контактная информация"

@admin.register(Instrument, site=philharmony_admin)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'inventory_number', 'condition_display']
    list_filter = ['type']
    search_fields = ['name', 'inventory_number']
    list_editable = ['type']
    verbose_name = "Инструмент"
    verbose_name_plural = "Инструменты"
    
    def condition_display(self, obj):
        colors = {
            'Отличное': 'green',
            'Требует настройки': 'orange',
            'В ремонте': 'red'
        }
        color = colors.get(obj.condition, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.condition)
    condition_display.short_description = "Состояние"

@admin.register(MusicalWork, site=philharmony_admin)
class MusicalWorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'composer', 'duration']
    search_fields = ['title', 'composer']
    list_filter = ['composer']
    verbose_name = "Музыкальное произведение"
    verbose_name_plural = "Музыкальные произведения"

@admin.register(Concert, site=philharmony_admin)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['title', 'concert_date', 'time', 'status_display', 'hall', 'manager']
    list_filter = ['status', 'date', 'hall', 'manager']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'
    list_per_page = 25
    inlines = [ConcertArtistInline]
    verbose_name = "Концерт"
    verbose_name_plural = "Концерты"
    
    def concert_date(self, obj):
        return obj.date.strftime("%d.%m.%Y")
    concert_date.short_description = "Дата"
    
    def status_display(self, obj):
        colors = {
            'Планируется': 'orange',
            'Завершен': 'green'
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.status)
    status_display.short_description = "Статус"

@admin.register(Program, site=philharmony_admin)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program_name', 'concert']
    search_fields = ['program_name']
    list_filter = ['concert']
    inlines = [ProgramWorkInline]
    verbose_name = "Программа"
    verbose_name_plural = "Программы"

@admin.register(ProgramWork, site=philharmony_admin)
class ProgramWorkAdmin(admin.ModelAdmin):
    list_display = ['program', 'work', 'sequence_order']
    list_filter = ['program']
    search_fields = ['program__program_name', 'work__title']
    verbose_name = "Произведение в программе"
    verbose_name_plural = "Произведения в программах"

@admin.register(ConcertArtist, site=philharmony_admin)
class ConcertArtistAdmin(admin.ModelAdmin):
    list_display = ['concert', 'artist', 'instrument']
    list_filter = ['concert', 'artist']
    search_fields = ['concert__title', 'artist__full_name', 'instrument__name']
    verbose_name = "Участие артиста"
    verbose_name_plural = "Участия артистов"

# Регистрируем LogEntry для просмотра логов
@admin.register(LogEntry, site=philharmony_admin)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    list_filter = ['action_time', 'user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    date_hierarchy = 'action_time'
    verbose_name = "Запись лога"
    verbose_name_plural = "Записи логов"