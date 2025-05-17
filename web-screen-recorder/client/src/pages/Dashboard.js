import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia, 
  CardActions,
  Button,
  IconButton,
  Divider,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Delete as DeleteIcon,
  Share as ShareIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import apiService from '../utils/api';
import screenRecorder from '../utils/screenRecorder';

const Dashboard = () => {
  const [recordings, setRecordings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [recordingToDelete, setRecordingToDelete] = useState(null);
  
  const navigate = useNavigate();
  
  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    
    // Fetch recordings
    fetchRecordings();
  }, [navigate]);
  
  const fetchRecordings = async () => {
    try {
      setLoading(true);
      const response = await apiService.recordings.getAll();
      setRecordings(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching recordings:', error);
      setError('Failed to fetch recordings. Please try again later.');
      setLoading(false);
    }
  };
  
  const handlePlayRecording = (recording) => {
    // Open recording in a new tab
    window.open(recording.url, '_blank');
  };
  
  const handleDeleteRecording = (recording) => {
    setRecordingToDelete(recording);
    setDeleteDialogOpen(true);
  };
  
  const confirmDeleteRecording = async () => {
    if (!recordingToDelete) return;
    
    try {
      await apiService.recordings.delete(recordingToDelete._id);
      setRecordings(recordings.filter(r => r._id !== recordingToDelete._id));
      setDeleteDialogOpen(false);
      setRecordingToDelete(null);
    } catch (error) {
      console.error('Error deleting recording:', error);
      setError('Failed to delete recording. Please try again later.');
    }
  };
  
  const handleDownloadRecording = (recording) => {
    // Create a download link
    const a = document.createElement('a');
    a.href = recording.url;
    a.download = `${recording.title || 'recording'}.webm`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };
  
  const handleShareRecording = (recording) => {
    // Copy share link to clipboard
    navigator.clipboard.writeText(recording.url)
      .then(() => {
        alert('Share link copied to clipboard!');
      })
      .catch(err => {
        console.error('Failed to copy link:', err);
      });
  };
  
  if (loading) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>
          Loading your recordings...
        </Typography>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom>
        My Recordings
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ mb: 4 }}>
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => navigate('/recorder')}
        >
          Create New Recording
        </Button>
      </Box>
      
      <Divider sx={{ mb: 4 }} />
      
      {recordings.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6" color="text.secondary">
            You don't have any recordings yet
          </Typography>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => navigate('/recorder')}
            sx={{ mt: 2 }}
          >
            Create Your First Recording
          </Button>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {recordings.map((recording) => (
            <Grid item xs={12} sm={6} md={4} key={recording._id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="140"
                  image={recording.thumbnailUrl || '/placeholder-thumbnail.jpg'}
                  alt={recording.title}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {recording.title}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {recording.description || 'No description'}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      Duration: {screenRecorder.formatTime(recording.duration || 0)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(recording.createdAt).toLocaleDateString()}
                    </Typography>
                  </Box>
                </CardContent>
                
                <CardActions>
                  <IconButton 
                    color="primary" 
                    onClick={() => handlePlayRecording(recording)}
                    aria-label="play"
                  >
                    <PlayIcon />
                  </IconButton>
                  <IconButton 
                    color="primary" 
                    onClick={() => handleDownloadRecording(recording)}
                    aria-label="download"
                  >
                    <DownloadIcon />
                  </IconButton>
                  <IconButton 
                    color="primary" 
                    onClick={() => handleShareRecording(recording)}
                    aria-label="share"
                  >
                    <ShareIcon />
                  </IconButton>
                  <IconButton 
                    color="error" 
                    onClick={() => handleDeleteRecording(recording)}
                    aria-label="delete"
                    sx={{ marginLeft: 'auto' }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      
      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Recording</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this recording? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={confirmDeleteRecording} color="error" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Dashboard;
