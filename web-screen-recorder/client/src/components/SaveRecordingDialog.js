import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  CircularProgress,
  Typography,
  Box,
  Alert
} from '@mui/material';
import apiService from '../utils/api';

const SaveRecordingDialog = ({ open, onClose, recordingData }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const handleSave = async () => {
    if (!title.trim()) {
      setError('Please enter a title for your recording');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Check if user is logged in
      const token = localStorage.getItem('token');
      if (!token) {
        // If not logged in, save locally
        saveLocally();
        return;
      }
      
      // If logged in, save to server
      await apiService.recordings.create({
        title,
        description,
        blob: recordingData.blob
      });
      
      setLoading(false);
      onClose(true);
    } catch (error) {
      console.error('Error saving recording:', error);
      setError('Failed to save recording. Please try again.');
      setLoading(false);
    }
  };
  
  const saveLocally = () => {
    try {
      // Create a download link
      const a = document.createElement('a');
      a.href = recordingData.url;
      a.download = `${title || 'screen-recording'}.webm`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      setLoading(false);
      onClose(true);
    } catch (error) {
      console.error('Error saving recording locally:', error);
      setError('Failed to save recording locally. Please try again.');
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    onClose(false);
  };
  
  return (
    <Dialog open={open} onClose={() => onClose(false)} maxWidth="sm" fullWidth>
      <DialogTitle>Save Recording</DialogTitle>
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        <TextField
          autoFocus
          margin="dense"
          label="Title"
          type="text"
          fullWidth
          variant="outlined"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={loading}
          required
        />
        
        <TextField
          margin="dense"
          label="Description (optional)"
          type="text"
          fullWidth
          variant="outlined"
          multiline
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
        />
        
        {recordingData && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Duration: {recordingData.duration ? screenRecorder.formatTime(recordingData.duration) : 'N/A'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Size: {recordingData.size ? `${Math.round(recordingData.size / 1024 / 1024 * 100) / 100} MB` : 'N/A'}
            </Typography>
          </Box>
        )}
        
        {!localStorage.getItem('token') && (
          <Alert severity="info" sx={{ mt: 2 }}>
            You are not logged in. The recording will be downloaded to your device.
          </Alert>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel} disabled={loading}>
          Cancel
        </Button>
        <Button 
          onClick={handleSave} 
          variant="contained" 
          color="primary"
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SaveRecordingDialog;
