const Recording = require('../models/Recording');
const { validationResult } = require('express-validator');
const AWS = require('aws-sdk');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Configure AWS if not using local storage
let s3;
if (!process.env.LOCAL_STORAGE) {
  AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION
  });

  s3 = new AWS.S3();
}

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function(req, file, cb) {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 100 * 1024 * 1024 }, // 100MB limit
  fileFilter: function(req, file, cb) {
    const filetypes = /webm|mp4|mov|avi/;
    const mimetype = filetypes.test(file.mimetype);
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase());

    if (mimetype && extname) {
      return cb(null, true);
    }
    cb(new Error('Error: Videos Only!'));
  }
}).single('video');

// @desc    Get all recordings for a user
// @route   GET /api/recordings
// @access  Private
exports.getRecordings = async (req, res) => {
  try {
    const recordings = await Recording.find({ user: req.user.id }).sort('-createdAt');

    res.status(200).json(recordings);
  } catch (err) {
    console.error(err);
    res.status(500).json({
      message: 'Server error'
    });
  }
};

// @desc    Get single recording
// @route   GET /api/recordings/:id
// @access  Private
exports.getRecording = async (req, res) => {
  try {
    const recording = await Recording.findById(req.params.id);

    if (!recording) {
      return res.status(404).json({
        message: 'Recording not found'
      });
    }

    // Make sure user owns recording
    if (recording.user.toString() !== req.user.id) {
      return res.status(401).json({
        message: 'Not authorized to access this recording'
      });
    }

    res.status(200).json(recording);
  } catch (err) {
    console.error(err);
    res.status(500).json({
      message: 'Server error'
    });
  }
};

// @desc    Create new recording
// @route   POST /api/recordings
// @access  Private
exports.createRecording = async (req, res) => {
  try {
    // Handle file upload
    upload(req, res, async function(err) {
      if (err) {
        return res.status(400).json({
          message: err.message
        });
      }

      if (!req.file) {
        return res.status(400).json({
          message: 'Please upload a video file'
        });
      }

      // Check for validation errors
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        // Remove uploaded file if validation fails
        fs.unlinkSync(req.file.path);
        return res.status(400).json({ errors: errors.array() });
      }

      try {
        let fileUrl;

        if (process.env.LOCAL_STORAGE === 'true') {
          // For local development, just use the file path
          const uploadDir = process.env.UPLOAD_PATH || './uploads';

          // Make sure upload directory exists
          if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
          }

          // Create user directory
          const userDir = path.join(uploadDir, req.user.id.toString());
          if (!fs.existsSync(userDir)) {
            fs.mkdirSync(userDir, { recursive: true });
          }

          // Move file to permanent location
          const fileName = `${Date.now()}-${path.basename(req.file.path)}`;
          const newPath = path.join(userDir, fileName);

          fs.copyFileSync(req.file.path, newPath);

          // Create URL for local file
          fileUrl = `/uploads/${req.user.id}/${fileName}`;
        } else {
          // Upload file to S3
          const fileContent = fs.readFileSync(req.file.path);
          const params = {
            Bucket: process.env.AWS_BUCKET_NAME,
            Key: `recordings/${req.user.id}/${Date.now()}-${path.basename(req.file.path)}`,
            Body: fileContent,
            ContentType: req.file.mimetype
          };

          const s3Data = await s3.upload(params).promise();
          fileUrl = s3Data.Location;
        }

        // Create recording in database
        const recording = await Recording.create({
          title: req.body.title,
          description: req.body.description || '',
          url: fileUrl,
          thumbnailUrl: '', // Generate thumbnail in a production app
          duration: req.body.duration || 0,
          size: req.file.size,
          user: req.user.id
        });

        // Remove temporary file
        fs.unlinkSync(req.file.path);

        res.status(201).json(recording);
      } catch (error) {
        // Remove uploaded file if S3 upload fails
        if (fs.existsSync(req.file.path)) {
          fs.unlinkSync(req.file.path);
        }
        throw error;
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({
      message: 'Server error'
    });
  }
};

// @desc    Update recording
// @route   PUT /api/recordings/:id
// @access  Private
exports.updateRecording = async (req, res) => {
  try {
    let recording = await Recording.findById(req.params.id);

    if (!recording) {
      return res.status(404).json({
        message: 'Recording not found'
      });
    }

    // Make sure user owns recording
    if (recording.user.toString() !== req.user.id) {
      return res.status(401).json({
        message: 'Not authorized to update this recording'
      });
    }

    // Update recording
    recording = await Recording.findByIdAndUpdate(
      req.params.id,
      {
        title: req.body.title,
        description: req.body.description
      },
      { new: true, runValidators: true }
    );

    res.status(200).json(recording);
  } catch (err) {
    console.error(err);
    res.status(500).json({
      message: 'Server error'
    });
  }
};

// @desc    Delete recording
// @route   DELETE /api/recordings/:id
// @access  Private
exports.deleteRecording = async (req, res) => {
  try {
    const recording = await Recording.findById(req.params.id);

    if (!recording) {
      return res.status(404).json({
        message: 'Recording not found'
      });
    }

    // Make sure user owns recording
    if (recording.user.toString() !== req.user.id) {
      return res.status(401).json({
        message: 'Not authorized to delete this recording'
      });
    }

    // Delete file
    if (recording.url) {
      if (process.env.LOCAL_STORAGE === 'true') {
        // For local storage, delete the file from the filesystem
        try {
          const filePath = path.join(process.cwd(), recording.url);
          if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
          }
        } catch (err) {
          console.error('Error deleting local file:', err);
        }
      } else {
        // Delete from S3
        const key = recording.url.split('/').slice(-2).join('/');

        const params = {
          Bucket: process.env.AWS_BUCKET_NAME,
          Key: `recordings/${key}`
        };

        await s3.deleteObject(params).promise();
      }
    }

    // Delete from database
    await recording.deleteOne();

    res.status(200).json({
      success: true,
      data: {}
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({
      message: 'Server error'
    });
  }
};
