import React from 'react';
import { 
  Box, 
  Button, 
  FormControl, 
  FormControlLabel, 
  Radio, 
  RadioGroup, 
  Typography,
  Paper
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Pause as PauseIcon,
  Save as SaveIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import screenRecorder from '../utils/screenRecorder';

const RecorderControls = ({ 
  isRecording, 
  isPaused, 
  recordingTime, 
  recordingData,
  audioSource,
  setAudioSource,
  onStart, 
  onStop, 
  onPause, 
  onResume,
  onSave,
  onDiscard
}) => {
  const formattedTime = screenRecorder.formatTime(recordingTime);
  
  const handleAudioSourceChange = (event) => {
    setAudioSource(event.target.value);
  };
  
  return (
    <Box sx={{ mt: 4 }}>
      {/* Audio Source Selection */}
      {!isRecording && (
        <Paper elevation={2} sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Audio Settings
          </Typography>
          <FormControl component="fieldset">
            <RadioGroup
              row
              name="audio-source"
              value={audioSource}
              onChange={handleAudioSourceChange}
            >
              <FormControlLabel 
                value="mic" 
                control={<Radio />} 
                label="Microphone" 
              />
              <FormControlLabel 
                value="system" 
                control={<Radio />} 
                label="System Audio" 
                disabled={true} // System audio may not be supported in all browsers
              />
              <FormControlLabel 
                value="both" 
                control={<Radio />} 
                label="Both" 
                disabled={true} // Combined audio may not be supported in all browsers
              />
              <FormControlLabel 
                value="none" 
                control={<Radio />} 
                label="No Audio" 
              />
            </RadioGroup>
          </FormControl>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            Note: System audio recording is limited by browser support
          </Typography>
        </Paper>
      )}
      
      {/* Recording Timer */}
      {isRecording && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
          <Typography variant="h4" component="div" fontFamily="monospace">
            {formattedTime}
          </Typography>
        </Box>
      )}
      
      {/* Recording Controls */}
      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
        {!isRecording && !recordingData && (
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<PlayIcon />}
            onClick={onStart}
            size="large"
          >
            Start Recording
          </Button>
        )}
        
        {isRecording && (
          <>
            {isPaused ? (
              <Button 
                variant="contained" 
                color="primary" 
                startIcon={<PlayIcon />}
                onClick={onResume}
              >
                Resume
              </Button>
            ) : (
              <Button 
                variant="contained" 
                color="secondary" 
                startIcon={<PauseIcon />}
                onClick={onPause}
              >
                Pause
              </Button>
            )}
            
            <Button 
              variant="contained" 
              color="error" 
              startIcon={<StopIcon />}
              onClick={onStop}
            >
              Stop Recording
            </Button>
          </>
        )}
        
        {recordingData && !isRecording && (
          <>
            <Button 
              variant="contained" 
              color="primary" 
              startIcon={<SaveIcon />}
              onClick={onSave}
            >
              Save Recording
            </Button>
            
            <Button 
              variant="outlined" 
              color="error" 
              startIcon={<DeleteIcon />}
              onClick={onDiscard}
            >
              Discard
            </Button>
            
            <Button 
              variant="outlined" 
              color="primary" 
              startIcon={<PlayIcon />}
              onClick={onStart}
            >
              New Recording
            </Button>
          </>
        )}
      </Box>
    </Box>
  );
};

export default RecorderControls;
