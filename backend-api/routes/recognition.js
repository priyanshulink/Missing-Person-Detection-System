/**
 * Recognition Routes
 * Handles face recognition and matching
 */

const express = require('express');
const router = express.Router();
const Person = require('../models/Person');
const Report = require('../models/Report');
const Camera = require('../models/Camera');
const { sendNotification } = require('../services/firebase');
const { calculateSimilarity } = require('../utils/faceUtils');

// In-memory cache for person encodings (refreshed periodically)
let personsCache = null;
let cacheTimestamp = 0;
const CACHE_TTL = 30000; // 30 seconds cache

// Function to get cached persons or fetch from database
async function getCachedPersons() {
  const now = Date.now();
  
  // Return cache if valid
  if (personsCache && (now - cacheTimestamp) < CACHE_TTL) {
    return personsCache;
  }
  
  // Fetch from database - only missing persons
  const persons = await Person.find({
    isActive: true,
    status: 'missing',  // Only match against missing persons
    'faceEncodings.0': { $exists: true }
  }).lean(); // Use lean() for faster queries
  
  // Update cache
  personsCache = persons;
  cacheTimestamp = now;
  
  return persons;
}

// Function to invalidate cache (call when persons are added/updated)
function invalidateCache() {
  personsCache = null;
  cacheTimestamp = 0;
}

// Face recognition endpoint
router.post('/', async (req, res) => {
  try {
    const { encoding, metadata } = req.body;
    
    // Validate input
    if (!encoding || !Array.isArray(encoding) || encoding.length !== 128) {
      return res.status(400).json({
        error: 'Valid face encoding (128-dimensional vector) is required'
      });
    }
    
    // Get all active persons with face encodings (from cache)
    const persons = await getCachedPersons();
    
    if (persons.length === 0) {
      return res.json({
        match_found: false,
        message: 'No persons in database'
      });
    }
    
    // Find best match using optimized comparison
    let bestMatch = null;
    let bestSimilarity = 0;
    const threshold = parseFloat(process.env.FACE_MATCH_THRESHOLD) || 0.6;  // 60% similarity minimum
    
    // Early exit if no persons
    if (persons.length === 0) {
      return res.json({
        match_found: false,
        message: 'No persons in database'
      });
    }
    
    // Optimized matching loop
    for (const person of persons) {
      // Skip persons without encodings
      if (!person.faceEncodings || person.faceEncodings.length === 0) continue;
      
      for (const storedEncoding of person.faceEncodings) {
        const similarity = calculateSimilarity(encoding, storedEncoding.encoding);
        
        // Early exit if perfect match found
        if (similarity > 0.95) {
          bestSimilarity = similarity;
          bestMatch = person;
          break;
        }
        
        if (similarity > bestSimilarity && similarity >= threshold) {
          bestSimilarity = similarity;
          bestMatch = person;
        }
      }
      
      // Break if perfect match found
      if (bestSimilarity > 0.95) break;
    }
    
    // If match found, create report and send alerts
    if (bestMatch) {
      // Try to find camera by cameraId
      let camera = null;
      if (metadata?.camera_id) {
        camera = await Camera.findOne({ cameraId: metadata.camera_id });
      }
      
      // Create report
      const reportData = {
        person: bestMatch._id,
        matchDetails: {
          similarity: bestSimilarity,
          confidence: metadata?.detection_confidence || 0,
          faceEncoding: encoding
        },
        detectionInfo: {
          cameraId: metadata?.camera_id || 'unknown',
          cameraName: camera?.name || metadata?.camera_name || 'Unknown Camera',
          cameraLocation: camera?.location || metadata?.camera_location || 'Unknown Location',
          timestamp: metadata?.timestamp ? new Date(metadata.timestamp) : new Date(),
          location: metadata?.location,
          bbox: metadata?.bbox ? {
            x1: metadata.bbox[0],
            y1: metadata.bbox[1],
            x2: metadata.bbox[2],
            y2: metadata.bbox[3]
          } : undefined
        },
        alertSent: false
      };
      
      // Link camera if found
      if (camera) {
        reportData.camera = camera._id;
      }
      
      const report = new Report(reportData);
      
      await report.save();
      
      // Send Socket.io notification
      const io = req.app.get('io');
      if (io) {
        io.emit('match_found', {
          reportId: report._id,
          personId: bestMatch._id,
          personName: bestMatch.name,
          similarity: bestSimilarity,
          cameraId: metadata?.camera_id,
          cameraName: metadata?.camera_name || 'Unknown Camera',
          cameraLocation: metadata?.camera_location || 'Unknown Location',
          timestamp: report.detectionInfo.timestamp
        });
      }
      
      // Send Firebase Cloud Messaging notification
      try {
        const cameraName = metadata?.camera_name || 'Unknown Camera';
        const cameraLocation = metadata?.camera_location || 'Unknown Location';
        
        await sendNotification({
          title: 'Person Identified',
          body: `${bestMatch.name} detected with ${(bestSimilarity * 100).toFixed(1)}% similarity at ${cameraLocation}`,
          data: {
            reportId: report._id.toString(),
            personId: bestMatch._id.toString(),
            personName: bestMatch.name,
            similarity: bestSimilarity.toString(),
            cameraName: cameraName,
            cameraLocation: cameraLocation
          }
        });
        
        report.alertSent = true;
        report.alertDetails = {
          sentAt: new Date(),
          method: 'fcm'
        };
        await report.save();
        
      } catch (notificationError) {
        console.error('Notification error:', notificationError);
      }
      
      return res.json({
        match_found: true,
        person_id: bestMatch._id,
        name: bestMatch.name,
        similarity: bestSimilarity,
        status: bestMatch.status,
        priority: bestMatch.priority,
        report_id: report._id
      });
    }
    
    // No match found
    res.json({
      match_found: false,
      message: 'No matching person found'
    });
    
  } catch (error) {
    console.error('Recognition error:', error);
    res.status(500).json({
      error: error.message || 'Error processing face recognition'
    });
  }
});

// Batch recognition endpoint
router.post('/batch', async (req, res) => {
  try {
    const { encodings } = req.body;
    
    if (!Array.isArray(encodings) || encodings.length === 0) {
      return res.status(400).json({
        error: 'Array of encodings is required'
      });
    }
    
    const results = [];
    
    for (const item of encodings) {
      // Process each encoding (simplified version)
      const { encoding, metadata } = item;
      
      if (!encoding || !Array.isArray(encoding) || encoding.length !== 128) {
        results.push({
          match_found: false,
          error: 'Invalid encoding'
        });
        continue;
      }
      
      // Get all active missing persons
      const persons = await Person.find({
        isActive: true,
        status: 'missing',  // Only match against missing persons
        'faceEncodings.0': { $exists: true }
      });
      
      let bestMatch = null;
      let bestSimilarity = 0;
      const threshold = parseFloat(process.env.FACE_MATCH_THRESHOLD) || 0.6;
      
      for (const person of persons) {
        for (const storedEncoding of person.faceEncodings) {
          const similarity = calculateSimilarity(encoding, storedEncoding.encoding);
          
          if (similarity > bestSimilarity && similarity >= threshold) {
            bestSimilarity = similarity;
            bestMatch = person;
          }
        }
      }
      
      if (bestMatch) {
        results.push({
          match_found: true,
          person_id: bestMatch._id,
          name: bestMatch.name,
          similarity: bestSimilarity
        });
      } else {
        results.push({
          match_found: false
        });
      }
    }
    
    res.json({
      results,
      total: encodings.length,
      matches: results.filter(r => r.match_found).length
    });
    
  } catch (error) {
    console.error('Batch recognition error:', error);
    res.status(500).json({
      error: error.message || 'Error processing batch recognition'
    });
  }
});

// Export router and cache invalidation function
router.invalidateCache = invalidateCache;

module.exports = router;
