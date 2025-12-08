#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Screen Recorder Module
---------------------
Handles the screen recording functionality.
"""

import os
import time
import threading
import tempfile
import subprocess
import numpy as np
import cv2
from datetime import datetime
from screeninfo import get_monitors
from PyQt5.QtCore import QObject, pyqtSignal

class ScreenRecorder(QObject):
    """Screen recorder class to capture screen and audio."""

    # Signals
    recording_started_signal = pyqtSignal()
    recording_stopped_signal = pyqtSignal(str)  # Output file path
    recording_paused_signal = pyqtSignal()
    recording_resumed_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, audio_manager):
        super().__init__()

        # Store audio manager
        self.audio_manager = audio_manager

        # Initialize variables
        self.is_recording = False
        self.is_paused = False
        self.stop_requested = False
        self.recording_thread = None
        self.output_file = None
        self.temp_video_file = None
        self.temp_audio_file = None

        # Get screen dimensions
        self.screen_width = 1920  # Default
        self.screen_height = 1080  # Default

        # Region selection
        self.region = None
        self.use_region = False

        try:
            # Get primary monitor
            primary_monitor = get_monitors()[0]
            self.screen_width = primary_monitor.width
            self.screen_height = primary_monitor.height
        except Exception as e:
            print(f"Warning: Could not get monitor info: {e}")

    def start_recording(self):
        """Start the screen recording process."""
        if self.is_recording:
            return

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.expanduser("~"), "Videos", "ScreenRecordings")
        os.makedirs(output_dir, exist_ok=True)

        # Generate output file name based on current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = os.path.join(output_dir, f"ScreenRecording_{timestamp}.mp4")

        # Create temporary files
        temp_dir = tempfile.gettempdir()
        self.temp_video_file = os.path.join(temp_dir, f"temp_video_{timestamp}.avi")
        self.temp_audio_file = os.path.join(temp_dir, f"temp_audio_{timestamp}.wav")

        # Reset flags
        self.is_recording = True
        self.is_paused = False
        self.stop_requested = False

        # Start recording thread
        self.recording_thread = threading.Thread(target=self._record_screen)
        self.recording_thread.daemon = True
        self.recording_thread.start()

        # Start audio recording if needed
        self.audio_manager.start_recording(self.temp_audio_file)

        # Emit signal
        self.recording_started_signal.emit()

    def stop_recording(self):
        """Stop the screen recording process."""
        if not self.is_recording:
            return self.output_file

        try:
            # Set stop flag
            self.stop_requested = True

            # Wait for recording thread to finish with timeout
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=5.0)  # Wait up to 5 seconds

                # If thread is still alive after timeout, it's stuck
                if self.recording_thread.is_alive():
                    print("Warning: Recording thread did not terminate properly")

            # Stop audio recording
            try:
                self.audio_manager.stop_recording()
            except Exception as e:
                print(f"Error stopping audio recording: {e}")

            # Combine video and audio if files exist
            if os.path.exists(self.temp_video_file):
                self._combine_video_audio()
            else:
                print("Warning: No video file was created")

            # Reset flags
            self.is_recording = False
            self.is_paused = False

            # Emit signal
            if hasattr(self, 'recording_stopped_signal'):
                self.recording_stopped_signal.emit(self.output_file)

            return self.output_file

        except Exception as e:
            import traceback
            print(f"Error in stop_recording: {e}")
            print(traceback.format_exc())

            # Reset flags even if there was an error
            self.is_recording = False
            self.is_paused = False
            self.stop_requested = True

            return self.output_file

    def pause_recording(self):
        """Pause the screen recording process."""
        if not self.is_recording or self.is_paused:
            return

        self.is_paused = True
        self.audio_manager.pause_recording()

        # Emit signal
        self.recording_paused_signal.emit()

    def resume_recording(self):
        """Resume the screen recording process."""
        if not self.is_recording or not self.is_paused:
            return

        self.is_paused = False
        self.audio_manager.resume_recording()

        # Emit signal
        self.recording_resumed_signal.emit()

    def _record_screen(self):
        """Record the screen to a video file."""
        try:
            # Determine capture dimensions
            if self.use_region and self.region:
                x, y, width, height = self.region
                capture_width = width
                capture_height = height
            else:
                capture_width = self.screen_width
                capture_height = self.screen_height

            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 30.0

            # Make sure the directory exists
            os.makedirs(os.path.dirname(self.temp_video_file), exist_ok=True)

            # Create video writer
            out = cv2.VideoWriter(
                self.temp_video_file,
                fourcc,
                fps,
                (capture_width, capture_height)
            )

            # Check if video writer was initialized properly
            if not out.isOpened():
                raise Exception(f"Failed to initialize video writer with dimensions {capture_width}x{capture_height}")

            print(f"Recording started with dimensions: {capture_width}x{capture_height}")
            print(f"Temporary video file: {self.temp_video_file}")

            # Variables for FPS calculation
            frame_count = 0
            start_time = time.time()
            last_fps_print = start_time

            # Start recording loop
            while not self.stop_requested:
                if not self.is_paused:
                    try:
                        # Capture screen
                        img = self._capture_screen()

                        # Check if image is valid
                        if img is None or img.size == 0:
                            print("Warning: Captured empty frame")
                            time.sleep(1/fps)
                            continue

                        # Make sure image has the right dimensions
                        if img.shape[1] != capture_width or img.shape[0] != capture_height:
                            img = cv2.resize(img, (capture_width, capture_height))

                        # Write frame to video
                        out.write(img)

                        # Update frame count
                        frame_count += 1

                        # Print FPS every 5 seconds
                        current_time = time.time()
                        if current_time - last_fps_print >= 5:
                            elapsed = current_time - start_time
                            current_fps = frame_count / elapsed if elapsed > 0 else 0
                            print(f"Recording at {current_fps:.2f} FPS")
                            last_fps_print = current_time

                    except Exception as e:
                        print(f"Error capturing frame: {e}")
                        # Continue recording despite errors

                # Sleep to maintain frame rate
                time.sleep(1/fps)

            # Calculate final statistics
            end_time = time.time()
            total_time = end_time - start_time
            avg_fps = frame_count / total_time if total_time > 0 else 0
            print(f"Recording finished: {frame_count} frames in {total_time:.2f} seconds ({avg_fps:.2f} FPS)")

            # Release video writer
            out.release()
            print(f"Video file saved: {self.temp_video_file}")

        except Exception as e:
            import traceback
            error_msg = f"Error recording screen: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.error_signal.emit(error_msg)
            self.stop_requested = True

    def set_region(self, region):
        """Set a specific region to record.

        Args:
            region (QRect): The region to record
        """
        self.region = (
            region.x(),
            region.y(),
            region.width(),
            region.height()
        )
        self.use_region = True

    def set_fullscreen(self):
        """Set to record the full screen."""
        self.use_region = False
        self.region = None

    def _capture_screen(self):
        """Capture the current screen as an image."""
        # Use OpenCV to capture the screen
        # This is a simplified version - in a real implementation,
        # you would use platform-specific methods for better performance

        try:
            # For Windows, you might use:
            import numpy as np
            from PIL import ImageGrab

            # Capture screen or region
            if self.use_region and self.region:
                x, y, width, height = self.region
                img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            else:
                img = ImageGrab.grab(bbox=(0, 0, self.screen_width, self.screen_height))

            # Convert to numpy array
            img_np = np.array(img)

            # Convert from BGR to RGB
            img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

            return img_np

        except Exception as e:
            print(f"Error capturing screen: {e}")
            # Return a blank image of the correct size as a fallback
            if self.use_region and self.region:
                width = self.region[2]
                height = self.region[3]
            else:
                width = self.screen_width
                height = self.screen_height

            return np.zeros((height, width, 3), dtype=np.uint8)

    def _combine_video_audio(self):
        """Combine video and audio files into the final output."""
        try:
            # Make sure output directory exists
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

            # Check if video file exists
            if not os.path.exists(self.temp_video_file):
                raise Exception(f"Video file not found: {self.temp_video_file}")

            # Check if audio file exists
            has_audio = os.path.exists(self.temp_audio_file) and os.path.getsize(self.temp_audio_file) > 0

            # Check if FFmpeg is available
            try:
                result = subprocess.run(
                    ["ffmpeg", "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                )
                print(f"Using FFmpeg: {result.stdout.splitlines()[0] if result.stdout else 'version unknown'}")
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f"FFmpeg error: {e}")
                raise Exception("FFmpeg is not installed or not in PATH")

            # Combine video and audio using FFmpeg
            if has_audio:
                print(f"Combining video ({self.temp_video_file}) and audio ({self.temp_audio_file})")
                cmd = [
                    "ffmpeg",
                    "-i", self.temp_video_file,
                    "-i", self.temp_audio_file,
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-strict", "experimental",
                    "-shortest",
                    "-y",  # Overwrite output file if it exists
                    self.output_file
                ]
            else:
                print(f"No audio file found, using video only: {self.temp_video_file}")
                cmd = [
                    "ffmpeg",
                    "-i", self.temp_video_file,
                    "-c:v", "libx264",
                    "-y",  # Overwrite output file if it exists
                    self.output_file
                ]

            # Run FFmpeg command
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )

            print(f"FFmpeg output: {process.stderr}")
            print(f"Recording saved to: {self.output_file}")

            # Clean up temporary files
            try:
                if os.path.exists(self.temp_video_file):
                    os.remove(self.temp_video_file)
                    print(f"Deleted temporary video file: {self.temp_video_file}")

                if os.path.exists(self.temp_audio_file):
                    os.remove(self.temp_audio_file)
                    print(f"Deleted temporary audio file: {self.temp_audio_file}")
            except Exception as e:
                print(f"Warning: Failed to delete temporary files: {e}")

        except Exception as e:
            import traceback
            error_msg = f"Error combining video and audio: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.error_signal.emit(error_msg)

            # If combining fails, just use the video file
            try:
                if os.path.exists(self.temp_video_file):
                    print(f"Fallback: Copying video file to output")
                    # Use copy instead of rename to avoid issues with different drives
                    import shutil
                    shutil.copy2(self.temp_video_file, self.output_file)
                    print(f"Video file copied to: {self.output_file}")
            except Exception as copy_error:
                print(f"Failed to copy video file: {copy_error}")
