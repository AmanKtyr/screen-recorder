import React from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { 
  Videocam as VideocamIcon,
  Mic as MicIcon,
  VolumeUp as VolumeUpIcon,
  Save as SaveIcon,
  Share as ShareIcon,
  Security as SecurityIcon,
  Check as CheckIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();
  
  const features = [
    {
      title: 'Screen Recording',
      description: 'Capture your screen with high quality and performance',
      icon: <VideocamIcon fontSize="large" color="primary" />
    },
    {
      title: 'Audio Recording',
      description: 'Record microphone audio along with your screen capture',
      icon: <MicIcon fontSize="large" color="primary" />
    },
    {
      title: 'System Audio',
      description: 'Capture system audio for complete recordings (browser support may vary)',
      icon: <VolumeUpIcon fontSize="large" color="primary" />
    },
    {
      title: 'Save & Download',
      description: 'Save your recordings to your account or download directly',
      icon: <SaveIcon fontSize="large" color="primary" />
    },
    {
      title: 'Share Recordings',
      description: 'Easily share your recordings with others',
      icon: <ShareIcon fontSize="large" color="primary" />
    },
    {
      title: 'Secure & Private',
      description: 'Your recordings are secure and private',
      icon: <SecurityIcon fontSize="large" color="primary" />
    }
  ];
  
  const handleStartRecording = () => {
    navigate('/recorder');
  };
  
  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Box sx={{ 
        textAlign: 'center', 
        py: 8,
        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
        borderRadius: 2,
        color: 'white',
        mb: 6
      }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Professional Web Screen Recorder
        </Typography>
        <Typography variant="h5" component="p" gutterBottom sx={{ mb: 4 }}>
          Record your screen directly from your browser with high quality
        </Typography>
        <Button 
          variant="contained" 
          size="large" 
          color="secondary"
          startIcon={<VideocamIcon />}
          onClick={handleStartRecording}
          sx={{ py: 1.5, px: 4, fontSize: '1.2rem' }}
        >
          Start Recording Now
        </Button>
      </Box>
      
      {/* Features Section */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom align="center" sx={{ mb: 4 }}>
          Key Features
        </Typography>
        
        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
      
      {/* How It Works Section */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom align="center" sx={{ mb: 4 }}>
          How It Works
        </Typography>
        
        <List>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="1. Click 'Start Recording'" 
              secondary="Navigate to the recorder page and click the start button" 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="2. Select what to record" 
              secondary="Choose to record your entire screen, a specific window, or a browser tab" 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="3. Configure audio settings" 
              secondary="Choose to record with microphone, system audio, both, or no audio" 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="4. Start recording" 
              secondary="Begin your recording session with our easy-to-use controls" 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckIcon color="primary" />
            </ListItemIcon>
            <ListItemText 
              primary="5. Save and share" 
              secondary="When finished, save your recording to your account or download it directly" 
            />
          </ListItem>
        </List>
      </Box>
      
      {/* Call to Action */}
      <Box sx={{ textAlign: 'center', py: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Ready to start recording?
        </Typography>
        <Button 
          variant="contained" 
          size="large" 
          color="primary"
          onClick={handleStartRecording}
          sx={{ mt: 2 }}
        >
          Go to Recorder
        </Button>
      </Box>
    </Container>
  );
};

export default Home;
