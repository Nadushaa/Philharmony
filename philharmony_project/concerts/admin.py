from django.contrib import admin
from .models import Manager, Hall, Artist, Instrument, Concert, ConcertArtist, MusicalWork, Program, ProgramWork

# Inline для отображения артистов в концерте
class ConcertArtistInline(admin.TabularInline):
    model = ConcertArtist
    extra = 1

# Inline для отображения произведений в программе
class ProgramWorkInline(admin.TabularInline):
    model = ProgramWork
    extra = 1

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'hall', 'manager']
    inlines = [ConcertArtistInline]

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program_name', 'concert']
    inlines = [ProgramWorkInline]

@admin.register(ProgramWork)
class ProgramWorkAdmin(admin.ModelAdmin):
    list_display = ['program', 'work', 'sequence_order']
    list_filter = ['program']


# Регистрируем остальные модели простым способом
admin.site.register(Manager)
admin.site.register(Hall)
admin.site.register(Artist)
admin.site.register(Instrument)
admin.site.register(ConcertArtist)
admin.site.register(MusicalWork)