import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Container,
  Alert,
  CircularProgress
} from '@mui/material';
import RecorderControls from '../components/RecorderControls';
import SaveRecordingDialog from '../components/SaveRecordingDialog';
import screenRecorder from '../utils/screenRecorder';

const Recorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [recordingData, setRecordingData] = useState(null);
  const [audioSource, setAudioSource] = useState('mic');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [saveDialogOpen, setSaveDialogOpen] = useState(false);
  
  const videoRef = useRef(null);
  
  useEffect(() => {
    // Set up screen recorder
    screenRecorder.setup({
      onTimeUpdate: (time) => setRecordingTime(time),
      onRecordingComplete: (data) => {
        setRecordingData(data);
        
        // Display the recorded video
        if (videoRef.current) {
          videoRef.current.src = data.url;
          videoRef.current.controls = true;
        }
      }
    });
    
    // Clean up
    return () => {
      if (recordingData && recordingData.url) {
        URL.revokeObjectURL(recordingData.url);
      }
    };
  }, []);
  
  const handleStartRecording = async () => {
    try {
      setLoading(true);
      setError('');
      setRecordingData(null);
      
      // Clear previous video
      if (videoRef.current) {
        videoRef.current.src = '';
        videoRef.current.controls = false;
      }
      
      // Start recording
      const stream = await screenRecorder.startRecording({
        audio: audioSource !== 'none',
        audioSource
      });
      
      // Display the stream in the video element
      if (videoRef.current && stream) {
        videoRef.current.srcObject = stream;
      }
      
      setIsRecording(true);
      setIsPaused(false);
      setLoading(false);
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Failed to start recording. Please make sure you have granted the necessary permissions.');
      setIsRecording(false);
      setLoading(false);
    }
  };
  
  const handleStopRecording = () => {
    screenRecorder.stopRecording();
    setIsRecording(false);
    setIsPaused(false);
    
    // Clear the srcObject
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };
  
  const handlePauseRecording = () => {
    screenRecorder.pauseRecording();
    setIsPaused(true);
  };
  
  const handleResumeRecording = () => {
    screenRecorder.resumeRecording();
    setIsPaused(false);
  };
  
  const handleSaveRecording = () => {
    setSaveDialogOpen(true);
  };
  
  const handleSaveDialogClose = (saved) => {
    setSaveDialogOpen(false);
    
    if (saved) {
      // Reset recording data if saved
      setRecordingData(null);
      
      // Clear the video
      if (videoRef.current) {
        videoRef.current.src = '';
        videoRef.current.controls = false;
      }
    }
  };
  
  const handleDiscardRecording = () => {
    // Reset recording data
    setRecordingData(null);
    
    // Clear the video
    if (videoRef.current) {
      videoRef.current.src = '';
      videoRef.current.controls = false;
    }
  };
  
  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Screen Recorder
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      <Paper elevation={3} className="video-container">
        {loading ? (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            height: '400px'
          }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <video 
              ref={videoRef}
              className="video-preview"
              autoPlay
              muted
              playsInline
            />
            
            {isRecording && (
              <div className="recording-indicator">
                <div className="recording-indicator-dot"></div>
                <span>Recording</span>
              </div>
            )}
          </>
        )}
      </Paper>
      
      <RecorderControls 
        isRecording={isRecording}
        isPaused={isPaused}
        recordingTime={recordingTime}
        recordingData={recordingData}
        audioSource={audioSource}
        setAudioSource={setAudioSource}
        onStart={handleStartRecording}
        onStop={handleStopRecording}
        onPause={handlePauseRecording}
        onResume={handleResumeRecording}
        onSave={handleSaveRecording}
        onDiscard={handleDiscardRecording}
      />
      
      {saveDialogOpen && (
        <SaveRecordingDialog 
          open={saveDialogOpen}
          onClose={handleSaveDialogClose}
          recordingData={recordingData}
        />
      )}
    </Container>
  );
};

export default Recorder;
