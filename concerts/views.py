from django.shortcuts import render, get_object_or_404
from .models import Concert, ConcertArtist, MusicalWork, Program, ProgramWork, Artist, Instrument

def concert_list(request):
    concerts = Concert.objects.all().order_by('date')
    
    # Считаем статистику
    total_concerts = concerts.count()
    planned_concerts = concerts.filter(status='Планируется').count()
    
    # Считаем общее количество назначений артистов (всех участий)
    total_artists = ConcertArtist.objects.count()
    
    return render(request, 'concerts/concert_list.html', {
        'concerts': concerts,
        'total_concerts': total_concerts,
        'planned_concerts': planned_concerts,
        'total_artists': total_artists,
    })

def concert_detail(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    artists = ConcertArtist.objects.filter(concert=concert)
    
    # Пытаемся найти программу
    try:
        program = Program.objects.get(concert=concert)
    except Program.DoesNotExist:
        program = None
    
    return render(request, 'concerts/concert_detail.html', {
        'concert': concert,
        'artists': artists,
        'program': program
    })

def artist_management(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    artists = ConcertArtist.objects.filter(concert=concert)
    return render(request, 'concerts/artist_management.html', {
        'concert': concert,
        'artists': artists
    })

def program_management(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    
    # Пытаемся найти программу для этого концерта
    try:
        program = Program.objects.get(concert=concert)
    except Program.DoesNotExist:
        program = None
    
    return render(request, 'concerts/program_management.html', {
        'concert': concert,
        'program': program
    })

def artist_list(request):
    artists = Artist.objects.all().order_by('full_name')
    
    # Статистика для артистов
    total_artists = artists.count()
    artists_with_concerts = Artist.objects.filter(concertartist__isnull=False).distinct().count()
    
    return render(request, 'concerts/artist_list.html', {
        'artists': artists,
        'total_artists': total_artists,
        'artists_with_concerts': artists_with_concerts,
    })

def instrument_list(request):
    instruments = Instrument.objects.all().order_by('name')
    
    # Статистика для инструментов
    total_instruments = instruments.count()
    
    # Считаем инструменты в отличном состоянии (доступные для использования)
    available_instruments = instruments.filter(condition='Отличное').count()
    
    # Считаем инструменты по типам - исправленная версия
    from django.db.models import Count
    instruments_by_type = Instrument.objects.values('type').annotate(
        count=Count('id')
    ).order_by('type')
    
    # Отладочная информация (можно убрать после проверки)
    print("=== DEBUG: Instruments by type ===")
    for item in instruments_by_type:
        print(f"Type: '{item['type']}', Count: {item['count']}")
    
    return render(request, 'concerts/instrument_list.html', {
        'instruments': instruments,
        'total_instruments': total_instruments,
        'available_instruments': available_instruments,
        'instruments_by_type': instruments_by_type,
    })