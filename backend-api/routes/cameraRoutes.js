const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

// Path to the seed-cameras.js file
const SEED_CAMERAS_PATH = path.join(__dirname, '../seed-cameras.js');

// Helper function to read cameras from seed-cameras.js
function readCameras() {
    try {
        const fileContent = fs.readFileSync(SEED_CAMERAS_PATH, 'utf8');
        // Extract the cameras array from the file
        const match = fileContent.match(/const cameras = (\[.*?\]);/s);
        if (!match) return [];
        
        // Parse the cameras array
        return JSON.parse(match[1]);
    } catch (error) {
        console.error('Error reading cameras:', error);
        return [];
    }
}

// Helper function to save cameras to seed-cameras.js
function saveCameras(cameras) {
    try {
        const content = `/**
 * Camera Configurations
 * This file is auto-generated. Do not edit manually.
 */

const cameras = ${JSON.stringify(cameras, null, 2)};

module.exports = { cameras };`;
        
        fs.writeFileSync(SEED_CAMERAS_PATH, content, 'utf8');
        return true;
    } catch (error) {
        console.error('Error saving cameras:', error);
        return false;
    }
}

// Get all cameras
router.get('/api/seed-cameras', (req, res) => {
    try {
        const cameras = readCameras();
        res.json({ cameras });
    } catch (error) {
        console.error('Error getting cameras:', error);
        res.status(500).json({ error: 'Failed to get cameras' });
    }
});

// Add a new camera
router.post('/api/seed-cameras', (req, res) => {
    try {
        const newCamera = req.body;
        const cameras = readCameras();
        
        // Add the new camera
        cameras.push(newCamera);
        
        // Save to file
        if (saveCameras(cameras)) {
            res.status(201).json(newCamera);
        } else {
            throw new Error('Failed to save cameras');
        }
    } catch (error) {
        console.error('Error adding camera:', error);
        res.status(500).json({ error: 'Failed to add camera' });
    }
});

// Update camera status
router.put('/api/seed-cameras/:cameraId/status', (req, res) => {
    try {
        const { cameraId } = req.params;
        const { status } = req.body;
        
        const cameras = readCameras();
        const cameraIndex = cameras.findIndex(c => c.cameraId === cameraId);
        
        if (cameraIndex === -1) {
            return res.status(404).json({ error: 'Camera not found' });
        }
        
        // Update status
        cameras[cameraIndex].status = status;
        
        // Save to file
        if (saveCameras(cameras)) {
            res.json({ success: true });
        } else {
            throw new Error('Failed to update camera status');
        }
    } catch (error) {
        console.error('Error updating camera status:', error);
        res.status(500).json({ error: 'Failed to update camera status' });
    }
});

// Delete a camera
router.delete('/api/seed-cameras/:cameraId', (req, res) => {
    try {
        const { cameraId } = req.params;
        const cameras = readCameras();
        
        // Filter out the camera to delete
        const updatedCameras = cameras.filter(c => c.cameraId !== cameraId);
        
        // If no camera was removed, return 404
        if (updatedCameras.length === cameras.length) {
            return res.status(404).json({ error: 'Camera not found' });
        }
        
        // Save to file
        if (saveCameras(updatedCameras)) {
            res.json({ success: true });
        } else {
            throw new Error('Failed to delete camera');
        }
    } catch (error) {
        console.error('Error deleting camera:', error);
        res.status(500).json({ error: 'Failed to delete camera' });
    }
});

module.exports = router;
