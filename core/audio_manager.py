#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Audio Manager Module
------------------
Handles audio recording from microphone and system.
"""

import os
import threading
import tempfile
import time
import wave
import numpy as np
import sounddevice as sd
import soundfile as sf
from PyQt5.QtCore import QObject, pyqtSignal

class AudioManager(QObject):
    """Audio manager class to handle microphone and system audio recording."""

    # Signals
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Initialize variables
        self.is_recording = False
        self.is_paused = False
        self.stop_requested = False

        self.recording_thread = None
        self.output_file = None

        # Audio source flags
        self.use_microphone = True
        self.use_system_audio = False

        # Audio parameters
        self.sample_rate = 44100
        self.channels = 2
        self.dtype = 'float32'

        # Audio buffers
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()

    def configure_audio_source(self, audio_source):
        """Configure which audio sources to use.

        Args:
            audio_source (str): The audio source to record from ('mic', 'system', 'both', or 'none')
        """
        if audio_source == "mic":
            self.use_microphone = True
            self.use_system_audio = False
        elif audio_source == "system":
            self.use_microphone = False
            self.use_system_audio = True
        elif audio_source == "both":
            self.use_microphone = True
            self.use_system_audio = True
        else:  # "none"
            self.use_microphone = False
            self.use_system_audio = False

    def start_recording(self, output_file):
        """Start audio recording.

        Args:
            output_file (str): Path to save the audio file
        """
        if self.is_recording or (not self.use_microphone and not self.use_system_audio):
            return

        # Set output file
        self.output_file = output_file

        # Reset flags
        self.is_recording = True
        self.is_paused = False
        self.stop_requested = False

        # Clear audio buffer
        with self.buffer_lock:
            self.audio_buffer = []

        # Start recording thread
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()

    def stop_recording(self):
        """Stop audio recording."""
        if not self.is_recording:
            return

        try:
            # Set stop flag
            self.stop_requested = True

            # Wait for recording thread to finish with timeout
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=5.0)  # Wait up to 5 seconds

                # If thread is still alive after timeout, it's stuck
                if self.recording_thread.is_alive():
                    print("Warning: Audio recording thread did not terminate properly")

            # Save audio buffer to file if needed
            try:
                self._save_audio_to_file()
            except Exception as e:
                print(f"Error saving audio file: {e}")

        except Exception as e:
            import traceback
            print(f"Error in stop_recording audio: {e}")
            print(traceback.format_exc())
        finally:
            # Always reset flags
            self.is_recording = False
            self.is_paused = False

    def pause_recording(self):
        """Pause audio recording."""
        if not self.is_recording or self.is_paused:
            return

        self.is_paused = True

    def resume_recording(self):
        """Resume audio recording."""
        if not self.is_recording or not self.is_paused:
            return

        self.is_paused = False

    def toggle_microphone(self, enabled):
        """Toggle microphone recording.

        Args:
            enabled (bool): Whether to enable microphone recording
        """
        self.use_microphone = enabled

    def toggle_system_audio(self, enabled):
        """Toggle system audio recording.

        Args:
            enabled (bool): Whether to enable system audio recording
        """
        self.use_system_audio = enabled

    def _record_audio(self):
        """Record audio to a file."""
        try:
            # Define callback function for audio input
            def audio_callback(indata, frames, time, status):
                if status:
                    print(f"Status: {status}")

                if not self.is_paused and self.is_recording:
                    with self.buffer_lock:
                        self.audio_buffer.append(indata.copy())

            # Start audio stream
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                callback=audio_callback
            ):
                # Keep thread alive until stop is requested
                while not self.stop_requested:
                    time.sleep(0.1)

            # Save audio buffer to file
            self._save_audio_to_file()

        except Exception as e:
            self.error_signal.emit(f"Error recording audio: {str(e)}")
            self.stop_requested = True

    def _save_audio_to_file(self):
        """Save recorded audio buffer to a file."""
        try:
            with self.buffer_lock:
                if not self.audio_buffer:
                    # No audio recorded
                    print("No audio data to save")
                    return

                # Concatenate all audio chunks
                try:
                    audio_data = np.concatenate(self.audio_buffer, axis=0)
                except ValueError as e:
                    print(f"Error concatenating audio data: {e}")
                    # If concatenation fails, try to save at least the first chunk
                    if len(self.audio_buffer) > 0:
                        audio_data = self.audio_buffer[0]
                    else:
                        return

            # Make sure output directory exists
            output_dir = os.path.dirname(self.output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # Save to file
            sf.write(
                self.output_file,
                audio_data,
                self.sample_rate,
                format='WAV'
            )

            print(f"Audio saved to {self.output_file}")

        except Exception as e:
            import traceback
            error_msg = f"Error saving audio: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())

            if hasattr(self, 'error_signal'):
                self.error_signal.emit(error_msg)

    def get_available_devices(self):
        """Get a list of available audio devices."""
        try:
            devices = sd.query_devices()
            return devices
        except Exception as e:
            self.error_signal.emit(f"Error getting audio devices: {str(e)}")
            return []
