from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json

from events.models import Event, EventCategory
from menu.models import MenuCategory, MenuItem, DrinkCategory, DrinkItem, SpecialMenu
from media_manager.models import MediaImage, CarouselSlide, HeroBanner
from core.models import SiteConfig, SocialLink, ContactMessage
from pages.models import Page


def is_staff(user):
    return user.is_staff


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_custom:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            next_url = request.GET.get('next', 'admin_custom:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Identifiants invalides ou accès non autorisé.')
    
    return render(request, 'admin_custom/login.html')


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_custom:login')


@login_required
@user_passes_test(is_staff)
def dashboard(request):
    today = timezone.now().date()
    this_month = today.replace(day=1)
    
    context = {
        'stats': {
            'events_total': Event.objects.count(),
            'events_upcoming': Event.objects.filter(date__gte=today, status='published').count(),
            'events_this_month': Event.objects.filter(date__gte=this_month, date__month=today.month).count(),
            'menu_items': MenuItem.objects.filter(is_available=True).count(),
            'drinks': DrinkItem.objects.filter(is_available=True).count(),
            'media_count': MediaImage.objects.count(),
            'messages_unread': ContactMessage.objects.filter(is_read=False).count(),
        },
        'upcoming_events': Event.objects.filter(
            date__gte=today, 
            status='published'
        ).order_by('date', 'start_time')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    
    return render(request, 'admin_custom/dashboard.html', context)


# ============ EVENTS ============

@login_required
@user_passes_test(is_staff)
def events_list(request):
    events = Event.objects.all().order_by('-date', '-start_time')
    
    # Filtres
    status = request.GET.get('status')
    category = request.GET.get('category')
    
    if status:
        events = events.filter(status=status)
    if category:
        events = events.filter(category_id=category)
    
    paginator = Paginator(events, 20)
    page = request.GET.get('page', 1)
    events = paginator.get_page(page)
    
    categories = EventCategory.objects.all()
    
    return render(request, 'admin_custom/events/list.html', {
        'events': events,
        'categories': categories,
        'current_status': status,
        'current_category': category,
    })


@login_required
@user_passes_test(is_staff)
def events_calendar(request):
    categories = EventCategory.objects.all()
    return render(request, 'admin_custom/events/calendar.html', {
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff)
def event_create(request):
    categories = EventCategory.objects.all()
    
    if request.method == 'POST':
        event = Event()
        event.title = request.POST.get('title')
        event.subtitle = request.POST.get('subtitle', '')
        event.description = request.POST.get('description', '')
        event.short_description = request.POST.get('short_description', '')
        event.date = request.POST.get('date')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time') or None
        event.doors_open = request.POST.get('doors_open') or None
        
        category_id = request.POST.get('category')
        if category_id:
            event.category_id = category_id
        
        event.artist_name = request.POST.get('artist_name', '')
        event.artist_bio = request.POST.get('artist_bio', '')
        event.artist_website = request.POST.get('artist_website', '')
        
        event.is_free = request.POST.get('is_free') == 'on'
        price = request.POST.get('price')
        event.price = float(price) if price else 0
        event.ticket_url = request.POST.get('ticket_url', '')
        
        event.status = request.POST.get('status', 'draft')
        event.is_featured = request.POST.get('is_featured') == 'on'
        event.is_weekly_highlight = request.POST.get('is_weekly_highlight') == 'on'
        
        if 'image' in request.FILES:
            event.image = request.FILES['image']
        
        event.save()
        messages.success(request, f'Événement "{event.title}" créé avec succès.')
        return redirect('admin_custom:events')
    
    return render(request, 'admin_custom/events/form.html', {
        'categories': categories,
        'event': None,
        'title': 'Créer un événement',
    })


@login_required
@user_passes_test(is_staff)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    categories = EventCategory.objects.all()
    
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.subtitle = request.POST.get('subtitle', '')
        event.description = request.POST.get('description', '')
        event.short_description = request.POST.get('short_description', '')
        event.date = request.POST.get('date')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time') or None
        event.doors_open = request.POST.get('doors_open') or None
        
        category_id = request.POST.get('category')
        event.category_id = category_id if category_id else None
        
        event.artist_name = request.POST.get('artist_name', '')
        event.artist_bio = request.POST.get('artist_bio', '')
        event.artist_website = request.POST.get('artist_website', '')
        
        event.is_free = request.POST.get('is_free') == 'on'
        price = request.POST.get('price')
        event.price = float(price) if price else 0
        event.ticket_url = request.POST.get('ticket_url', '')
        
        event.status = request.POST.get('status', 'draft')
        event.is_featured = request.POST.get('is_featured') == 'on'
        event.is_weekly_highlight = request.POST.get('is_weekly_highlight') == 'on'
        
        if 'image' in request.FILES:
            event.image = request.FILES['image']
        
        event.save()
        messages.success(request, f'Événement "{event.title}" modifié avec succès.')
        return redirect('admin_custom:events')
    
    return render(request, 'admin_custom/events/form.html', {
        'categories': categories,
        'event': event,
        'title': f'Modifier: {event.title}',
    })


@login_required
@user_passes_test(is_staff)
@require_POST
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    title = event.title
    event.delete()
    messages.success(request, f'Événement "{title}" supprimé.')
    return redirect('admin_custom:events')


@login_required
@user_passes_test(is_staff)
def event_categories(request):
    categories = EventCategory.objects.annotate(events_count=Count('events'))
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name')
            slug = request.POST.get('slug')
            color = request.POST.get('color', '#1a1a2e')
            EventCategory.objects.create(name=name, slug=slug, color=color)
            messages.success(request, f'Catégorie "{name}" créée.')
        
        elif action == 'delete':
            cat_id = request.POST.get('category_id')
            cat = get_object_or_404(EventCategory, pk=cat_id)
            cat.delete()
            messages.success(request, 'Catégorie supprimée.')
        
        return redirect('admin_custom:event_categories')
    
    return render(request, 'admin_custom/events/categories.html', {
        'categories': categories,
    })


# ============ MENU ============

@login_required
@user_passes_test(is_staff)
def menu_list(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    return render(request, 'admin_custom/menu/list.html', {
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff)
def menu_item_create(request):
    categories = MenuCategory.objects.all()
    
    if request.method == 'POST':
        item = MenuItem()
        item.name = request.POST.get('name')
        item.description = request.POST.get('description', '')
        item.price = float(request.POST.get('price', 0))
        item.category_id = request.POST.get('category')
        item.is_vegetarian = request.POST.get('is_vegetarian') == 'on'
        item.is_vegan = request.POST.get('is_vegan') == 'on'
        item.is_gluten_free = request.POST.get('is_gluten_free') == 'on'
        item.is_spicy = request.POST.get('is_spicy') == 'on'
        item.is_available = request.POST.get('is_available') == 'on'
        item.is_featured = request.POST.get('is_featured') == 'on'
        item.allergens = request.POST.get('allergens', '')
        
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        
        item.save()
        messages.success(request, f'"{item.name}" ajouté au menu.')
        return redirect('admin_custom:menu')
    
    return render(request, 'admin_custom/menu/item_form.html', {
        'categories': categories,
        'item': None,
        'title': 'Ajouter un plat',
    })


@login_required
@user_passes_test(is_staff)
def menu_item_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    categories = MenuCategory.objects.all()
    
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description', '')
        item.price = float(request.POST.get('price', 0))
        item.category_id = request.POST.get('category')
        item.is_vegetarian = request.POST.get('is_vegetarian') == 'on'
        item.is_vegan = request.POST.get('is_vegan') == 'on'
        item.is_gluten_free = request.POST.get('is_gluten_free') == 'on'
        item.is_spicy = request.POST.get('is_spicy') == 'on'
        item.is_available = request.POST.get('is_available') == 'on'
        item.is_featured = request.POST.get('is_featured') == 'on'
        item.allergens = request.POST.get('allergens', '')
        
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        
        item.save()
        messages.success(request, f'"{item.name}" modifié.')
        return redirect('admin_custom:menu')
    
    return render(request, 'admin_custom/menu/item_form.html', {
        'categories': categories,
        'item': item,
        'title': f'Modifier: {item.name}',
    })


@login_required
@user_passes_test(is_staff)
@require_POST
def menu_item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    name = item.name
    item.delete()
    messages.success(request, f'"{name}" supprimé du menu.')
    return redirect('admin_custom:menu')


@login_required
@user_passes_test(is_staff)
def menu_categories(request):
    categories = MenuCategory.objects.annotate(items_count=Count('items'))
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name')
            slug = request.POST.get('slug')
            order = int(request.POST.get('order', 0))
            MenuCategory.objects.create(name=name, slug=slug, order=order)
            messages.success(request, f'Catégorie "{name}" créée.')
        
        elif action == 'delete':
            cat_id = request.POST.get('category_id')
            cat = get_object_or_404(MenuCategory, pk=cat_id)
            cat.delete()
            messages.success(request, 'Catégorie supprimée.')
        
        return redirect('admin_custom:menu_categories')
    
    return render(request, 'admin_custom/menu/categories.html', {
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff)
def drinks_list(request):
    categories = DrinkCategory.objects.prefetch_related('drinks').all()
    return render(request, 'admin_custom/menu/drinks.html', {
        'categories': categories,
    })


# ============ MEDIA ============

@login_required
@user_passes_test(is_staff)
def media_gallery(request):
    images = MediaImage.objects.all()
    
    category = request.GET.get('category')
    if category:
        images = images.filter(category__slug=category)
    
    paginator = Paginator(images, 24)
    page = request.GET.get('page', 1)
    images = paginator.get_page(page)
    
    from media_manager.models import MediaCategory
    categories = MediaCategory.objects.all()
    
    return render(request, 'admin_custom/media/gallery.html', {
        'images': images,
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff)
def media_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        category_id = request.POST.get('category')
        
        for f in files:
            MediaImage.objects.create(
                file=f,
                category_id=category_id if category_id else None,
                uploaded_by=request.user
            )
        
        messages.success(request, f'{len(files)} image(s) uploadée(s).')
        return redirect('admin_custom:media')
    
    from media_manager.models import MediaCategory
    categories = MediaCategory.objects.all()
    
    return render(request, 'admin_custom/media/upload.html', {
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff)
@require_POST
def media_delete(request, pk):
    image = get_object_or_404(MediaImage, pk=pk)
    image.file.delete()
    image.delete()
    messages.success(request, 'Image supprimée.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('admin_custom:media')


@login_required
@user_passes_test(is_staff)
def carousel_manage(request):
    slides = CarouselSlide.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            slide = CarouselSlide()
            slide.title = request.POST.get('title', '')
            slide.subtitle = request.POST.get('subtitle', '')
            slide.order = int(request.POST.get('order', 0))
            slide.is_active = request.POST.get('is_active') == 'on'
            if 'image' in request.FILES:
                slide.image = request.FILES['image']
            slide.save()
            messages.success(request, 'Slide ajoutée.')
        
        elif action == 'delete':
            slide_id = request.POST.get('slide_id')
            slide = get_object_or_404(CarouselSlide, pk=slide_id)
            slide.delete()
            messages.success(request, 'Slide supprimée.')
        
        return redirect('admin_custom:carousel')
    
    return render(request, 'admin_custom/media/carousel.html', {
        'slides': slides,
    })


# ============ SETTINGS ============

@login_required
@user_passes_test(is_staff)
def site_settings(request):
    config = SiteConfig.objects.first()
    if not config:
        config = SiteConfig.objects.create()
    
    if request.method == 'POST':
        config.site_name = request.POST.get('site_name', '')
        config.tagline = request.POST.get('tagline', '')
        config.description = request.POST.get('description', '')
        config.phone = request.POST.get('phone', '')
        config.email = request.POST.get('email', '')
        config.address_line1 = request.POST.get('address_line1', '')
        config.address_line2 = request.POST.get('address_line2', '')
        config.city = request.POST.get('city', '')
        config.postal_code = request.POST.get('postal_code', '')
        config.region = request.POST.get('region', '')
        config.google_maps_embed_url = request.POST.get('google_maps_embed_url', '')
        config.google_maps_directions_url = request.POST.get('google_maps_directions_url', '')
        config.opening_hours = request.POST.get('opening_hours', '')
        config.meta_title = request.POST.get('meta_title', '')
        config.meta_description = request.POST.get('meta_description', '')
        
        if 'logo' in request.FILES:
            config.logo = request.FILES['logo']
        
        config.save()
        messages.success(request, 'Configuration sauvegardée.')
        return redirect('admin_custom:settings')
    
    return render(request, 'admin_custom/settings/site.html', {
        'config': config,
    })


@login_required
@user_passes_test(is_staff)
def social_links(request):
    links = SocialLink.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            platform = request.POST.get('platform')
            url = request.POST.get('url')
            order = int(request.POST.get('order', 0))
            SocialLink.objects.create(platform=platform, url=url, order=order)
            messages.success(request, 'Lien ajouté.')
        
        elif action == 'delete':
            link_id = request.POST.get('link_id')
            link = get_object_or_404(SocialLink, pk=link_id)
            link.delete()
            messages.success(request, 'Lien supprimé.')
        
        return redirect('admin_custom:social_links')
    
    return render(request, 'admin_custom/settings/social.html', {
        'links': links,
        'platforms': SocialLink.PLATFORMS,
    })


# ============ MESSAGES ============

@login_required
@user_passes_test(is_staff)
def contact_messages(request):
    msgs = ContactMessage.objects.all()
    
    status = request.GET.get('status')
    if status == 'unread':
        msgs = msgs.filter(is_read=False)
    elif status == 'read':
        msgs = msgs.filter(is_read=True)
    
    paginator = Paginator(msgs, 20)
    page = request.GET.get('page', 1)
    msgs = paginator.get_page(page)
    
    return render(request, 'admin_custom/messages/list.html', {
        'messages_list': msgs,
    })


@login_required
@user_passes_test(is_staff)
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        msg.delete()
        messages.success(request, 'Message supprimé.')
        return redirect('admin_custom:messages')
    
    return render(request, 'admin_custom/messages/detail.html', {
        'msg': msg,
    })


# ============ API ENDPOINTS ============

@login_required
@user_passes_test(is_staff)
def api_events(request):
    """API pour les événements (AJAX)"""
    events = Event.objects.all()
    
    data = []
    for e in events:
        data.append({
            'id': e.id,
            'title': e.title,
            'date': e.date.isoformat(),
            'start_time': e.start_time.strftime('%H:%M'),
            'status': e.status,
            'category': e.category.name if e.category else None,
        })
    
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_staff)
def api_events_calendar(request):
    """API pour le calendrier FullCalendar"""
    start = request.GET.get('start', '')[:10]
    end = request.GET.get('end', '')[:10]
    
    events = Event.objects.all()
    if start:
        events = events.filter(date__gte=start)
    if end:
        events = events.filter(date__lte=end)
    
    data = []
    for e in events:
        color = e.category.color if e.category else '#1a1a2e'
        
        # Ajuster la couleur selon le statut
        if e.status == 'draft':
            color = '#6c757d'
        elif e.status == 'cancelled':
            color = '#dc3545'
        
        data.append({
            'id': e.id,
            'title': e.title,
            'start': f"{e.date.isoformat()}T{e.start_time.strftime('%H:%M')}",
            'end': f"{e.date.isoformat()}T{e.end_time.strftime('%H:%M')}" if e.end_time else None,
            'color': color,
            'extendedProps': {
                'status': e.status,
                'category': e.category.name if e.category else None,
            }
        })
    
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(is_staff)
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
def api_event_detail(request, pk):
    """API pour un événement spécifique"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': event.id,
            'title': event.title,
            'date': event.date.isoformat(),
            'start_time': event.start_time.strftime('%H:%M'),
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else None,
            'description': event.description,
            'status': event.status,
            'category_id': event.category_id,
        })
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        event.date = data.get('date', event.date)
        if 'start_time' in data:
            event.start_time = data['start_time']
        event.save()
        return JsonResponse({'status': 'ok'})
    
    elif request.method == 'DELETE':
        event.delete()
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
