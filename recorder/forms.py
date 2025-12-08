from django import forms
from .models import RecorderSettings

class RecorderSettingsForm(forms.ModelForm):
    """Form for updating recorder settings"""
    
    class Meta:
        model = RecorderSettings
        fields = [
            'video_quality', 
            'frame_rate', 
            'record_audio', 
            'audio_source', 
            'show_cursor', 
            'countdown_seconds', 
            'auto_save'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            if isinstance(self.fields[field_name].widget, forms.CheckboxInput):
                self.fields[field_name].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control'
                
        # Add help text
        self.fields['video_quality'].help_text = 'Higher quality results in larger file sizes'
        self.fields['frame_rate'].help_text = 'Higher frame rates result in smoother video but larger file sizes'
        self.fields['audio_source'].help_text = 'Choose which audio source to record'
        self.fields['countdown_seconds'].help_text = 'Number of seconds to count down before recording starts'
