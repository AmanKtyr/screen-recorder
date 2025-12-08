from django.db import models
from django.contrib.auth.models import User

class RecorderSettings(models.Model):
    """Model for user's recorder settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recorder_settings')

    # Video settings
    video_quality = models.CharField(
        max_length=10,
        choices=[
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ],
        default='high'
    )
    frame_rate = models.IntegerField(default=30)

    # Audio settings
    record_audio = models.BooleanField(default=True)
    audio_source = models.CharField(
        max_length=10,
        choices=[
            ('mic', 'Microphone'),
            ('system', 'System Audio'),
            ('both', 'Both'),
            ('none', 'None'),
        ],
        default='mic'
    )

    # Other settings
    show_cursor = models.BooleanField(default=True)
    countdown_seconds = models.IntegerField(default=3)
    auto_save = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Recorder Settings"
