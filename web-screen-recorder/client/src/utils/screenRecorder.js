/**
 * Screen Recorder Utility
 * Handles screen recording functionality using the MediaRecorder API
 */

class ScreenRecorder {
  constructor() {
    this.mediaRecorder = null;
    this.recordedChunks = [];
    this.stream = null;
    this.isRecording = false;
    this.isPaused = false;
    this.startTime = 0;
    this.elapsedTime = 0;
    this.timerInterval = null;
    this.onTimeUpdate = null;
    this.onRecordingComplete = null;
  }

  /**
   * Set up the screen recorder with options
   * @param {Object} options - Configuration options
   * @param {Function} options.onTimeUpdate - Callback for timer updates
   * @param {Function} options.onRecordingComplete - Callback when recording is complete
   */
  setup(options = {}) {
    this.onTimeUpdate = options.onTimeUpdate;
    this.onRecordingComplete = options.onRecordingComplete;
  }

  /**
   * Start recording the screen
   * @param {Object} options - Recording options
   * @param {boolean} options.audio - Whether to record audio
   * @param {string} options.audioSource - Audio source ('mic', 'system', or 'both')
   * @returns {Promise<void>}
   */
  async startRecording(options = { audio: true, audioSource: 'mic' }) {
    try {
      // Reset recorded chunks
      this.recordedChunks = [];
      
      // Get display media (screen)
      const displayMediaOptions = {
        video: {
          cursor: "always",
          displaySurface: "monitor",
        },
        audio: false, // We'll handle audio separately
      };
      
      const screenStream = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
      
      // Set up audio if requested
      let audioStream = null;
      if (options.audio) {
        const audioConstraints = {
          audio: true,
        };
        
        if (options.audioSource === 'mic' || options.audioSource === 'both') {
          audioStream = await navigator.mediaDevices.getUserMedia(audioConstraints);
        }
        
        // Note: System audio capture is limited by browser support
        // Chrome allows system audio capture through getDisplayMedia
      }
      
      // Combine streams if needed
      let combinedStream;
      if (audioStream) {
        const audioTracks = audioStream.getAudioTracks();
        combinedStream = new MediaStream([
          ...screenStream.getVideoTracks(),
          ...audioTracks
        ]);
      } else {
        combinedStream = screenStream;
      }
      
      this.stream = combinedStream;
      
      // Create media recorder
      this.mediaRecorder = new MediaRecorder(combinedStream, {
        mimeType: 'video/webm;codecs=vp9,opus',
      });
      
      // Set up event handlers
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.recordedChunks.push(event.data);
        }
      };
      
      this.mediaRecorder.onstop = () => {
        this._stopTimer();
        this._processRecording();
        
        // Stop all tracks
        this.stream.getTracks().forEach(track => track.stop());
      };
      
      // Start recording
      this.mediaRecorder.start(1000); // Collect data every second
      this.isRecording = true;
      this.isPaused = false;
      
      // Start timer
      this._startTimer();
      
      return this.stream;
    } catch (error) {
      console.error('Error starting recording:', error);
      throw error;
    }
  }

  /**
   * Stop the recording
   */
  stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
      this.isPaused = false;
    }
  }

  /**
   * Pause the recording
   */
  pauseRecording() {
    if (this.mediaRecorder && this.isRecording && !this.isPaused) {
      this.mediaRecorder.pause();
      this.isPaused = true;
      this._pauseTimer();
    }
  }

  /**
   * Resume the recording
   */
  resumeRecording() {
    if (this.mediaRecorder && this.isRecording && this.isPaused) {
      this.mediaRecorder.resume();
      this.isPaused = false;
      this._resumeTimer();
    }
  }

  /**
   * Process the recorded chunks into a downloadable file
   * @private
   */
  _processRecording() {
    if (this.recordedChunks.length === 0) {
      console.warn('No recorded data available');
      return;
    }
    
    const blob = new Blob(this.recordedChunks, {
      type: 'video/webm'
    });
    
    const url = URL.createObjectURL(blob);
    
    if (this.onRecordingComplete) {
      this.onRecordingComplete({
        blob,
        url,
        size: blob.size,
        type: blob.type,
        duration: this.elapsedTime
      });
    }
    
    return { blob, url };
  }

  /**
   * Start the recording timer
   * @private
   */
  _startTimer() {
    this.startTime = Date.now();
    this.elapsedTime = 0;
    
    this.timerInterval = setInterval(() => {
      if (!this.isPaused) {
        this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
        
        if (this.onTimeUpdate) {
          this.onTimeUpdate(this.elapsedTime);
        }
      }
    }, 1000);
  }

  /**
   * Pause the timer
   * @private
   */
  _pauseTimer() {
    // We don't clear the interval, just stop updating the elapsed time
  }

  /**
   * Resume the timer
   * @private
   */
  _resumeTimer() {
    // Update the start time to account for the pause duration
    this.startTime = Date.now() - (this.elapsedTime * 1000);
  }

  /**
   * Stop the timer
   * @private
   */
  _stopTimer() {
    clearInterval(this.timerInterval);
  }

  /**
   * Format seconds into HH:MM:SS
   * @param {number} seconds - Seconds to format
   * @returns {string} Formatted time string
   */
  static formatTime(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    
    return [
      h > 0 ? h.toString().padStart(2, '0') : '00',
      m.toString().padStart(2, '0'),
      s.toString().padStart(2, '0')
    ].join(':');
  }
}

export default new ScreenRecorder();
