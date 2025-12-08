from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import RecorderSettings
from .forms import RecorderSettingsForm

def home(request):
    """Home page view"""
    return render(request, 'recorder/home.html')

@login_required
def recorder(request):
    """Screen recorder view"""
    # Get user's recorder settings
    settings, created = RecorderSettings.objects.get_or_create(user=request.user)

    context = {
        'settings': settings
    }

    return render(request, 'recorder/recorder.html', context)

@login_required
def settings(request):
    """Settings view for recorder"""
    # Get user's recorder settings
    settings, created = RecorderSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = RecorderSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    else:
        form = RecorderSettingsForm(instance=settings)

    context = {
        'form': form
    }

    return render(request, 'recorder/settings.html', context)

@login_required
def get_settings(request):
    """API view to get user's recorder settings"""
    settings, created = RecorderSettings.objects.get_or_create(user=request.user)

    data = {
        'video_quality': settings.video_quality,
        'frame_rate': settings.frame_rate,
        'record_audio': settings.record_audio,
        'audio_source': settings.audio_source,
        'show_cursor': settings.show_cursor,
        'countdown_seconds': settings.countdown_seconds,
        'auto_save': settings.auto_save
    }

    return JsonResponse(data)
