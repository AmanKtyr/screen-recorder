# Web Screen Recorder

A professional web-based screen recording application that allows users to record their screen directly from a browser. This project is designed as a final year college project.

## Features

- **Screen Recording**: Capture your screen with high quality and performance
- **Audio Recording**: Record microphone audio along with your screen capture
- **User Authentication**: Register and login to save and manage your recordings
- **Recording Management**: View, play, download, share, and delete your recordings
- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

### Frontend
- React.js
- Material-UI
- MediaRecorder API
- React Router
- Axios

### Backend
- Node.js
- Express.js
- MongoDB
- JWT Authentication
- AWS S3 (for video storage)
- Multer (for file uploads)

## Installation and Setup

### Prerequisites
- Node.js (v14 or higher)
- MongoDB
- AWS Account (for S3 storage)

### Setup Instructions

1. Clone the repository
```
git clone https://github.com/yourusername/web-screen-recorder.git
cd web-screen-recorder
```

2. Install dependencies for both client and server
```
# Install server dependencies
cd server
npm install

# Install client dependencies
cd ../client
npm install
```

3. Configure environment variables
```
# In the server directory, create a .env file based on .env.example
cp .env.example .env
# Edit the .env file with your MongoDB URI, JWT secret, and AWS credentials
```

4. Run the application
```
# Start the server (from the server directory)
npm run dev

# Start the client (from the client directory)
npm start
```

5. Access the application
```
Open your browser and navigate to http://localhost:3000
```

## Usage

1. **Register/Login**: Create an account or login to save your recordings
2. **Start Recording**: Navigate to the recorder page and click "Start Recording"
3. **Select Screen**: Choose which screen, window, or tab to record
4. **Configure Audio**: Select audio source (microphone, system audio, or none)
5. **Control Recording**: Use the controls to pause, resume, or stop recording
6. **Save Recording**: After stopping, you can save the recording to your account or download it
7. **Manage Recordings**: View, play, download, share, or delete your recordings from the dashboard

## Project Structure

```
web-screen-recorder/
├── client/                 # Frontend React application
│   ├── public/             # Public assets
│   └── src/                # React source files
│       ├── components/     # Reusable components
│       ├── pages/          # Page components
│       ├── utils/          # Utility functions
│       ├── assets/         # Static assets
│       └── styles/         # CSS styles
├── server/                 # Backend Node.js application
│   ├── config/             # Configuration files
│   ├── controllers/        # Route controllers
│   ├── middleware/         # Custom middleware
│   ├── models/             # Mongoose models
│   └── routes/             # API routes
└── README.md               # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder)
- [Material-UI](https://mui.com/)
- [React.js](https://reactjs.org/)
- [Node.js](https://nodejs.org/)
- [MongoDB](https://www.mongodb.com/)
- [Express.js](https://expressjs.com/)
