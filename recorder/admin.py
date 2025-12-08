from django.contrib import admin
from .models import RecorderSettings

@admin.register(RecorderSettings)
class RecorderSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_quality', 'frame_rate', 'audio_source', 'show_cursor')
    list_filter = ('video_quality', 'audio_source', 'record_audio', 'show_cursor')
    search_fields = ('user__username', 'user__email')
