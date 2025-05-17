const express = require('express');
const { check } = require('express-validator');
const { 
  getRecordings, 
  getRecording, 
  createRecording, 
  updateRecording, 
  deleteRecording 
} = require('../controllers/recordings');
const { protect } = require('../middleware/auth');

const router = express.Router();

// Protect all routes
router.use(protect);

// Get all recordings and create new recording
router.route('/')
  .get(getRecordings)
  .post([
    check('title', 'Title is required').not().isEmpty()
  ], createRecording);

// Get, update and delete recording by ID
router.route('/:id')
  .get(getRecording)
  .put([
    check('title', 'Title is required').not().isEmpty()
  ], updateRecording)
  .delete(deleteRecording);

module.exports = router;
