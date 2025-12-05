/**
 * Surveillance Control Routes
 * Handles starting/stopping surveillance system
 */

const express = require('express');
const router = express.Router();
const { spawn, exec } = require('child_process');
const path = require('path');
const { authenticate } = require('../middleware/auth');

let surveillanceProcess = null;

/**
 * Start surveillance system
 */
router.post('/start', authenticate, (req, res) => {
    try {
        if (surveillanceProcess) {
            return res.json({
                message: 'Surveillance already running',
                status: 'running'
            });
        }

        // Path to surveillance script
        const scriptPath = path.join(__dirname, '../../ai-module/yolo_integrated_surveillance.py');
        
        // Start surveillance process
        surveillanceProcess = spawn('python', [scriptPath], {
            detached: false,
            stdio: 'pipe'
        });

        surveillanceProcess.stdout.on('data', (data) => {
            console.log(`[Surveillance] ${data.toString().trim()}`);
        });

        surveillanceProcess.stderr.on('data', (data) => {
            console.error(`[Surveillance Error] ${data.toString().trim()}`);
        });

        surveillanceProcess.on('close', (code) => {
            console.log(`[Surveillance] Process exited with code ${code}`);
            surveillanceProcess = null;
        });

        console.log('✅ Surveillance system started');

        res.json({
            message: 'Surveillance system started successfully',
            status: 'started',
            pid: surveillanceProcess.pid
        });

    } catch (error) {
        console.error('Error starting surveillance:', error);
        res.status(500).json({
            error: 'Failed to start surveillance system',
            details: error.message
        });
    }
});

/**
 * Stop surveillance system
 */
router.post('/stop', authenticate, (req, res) => {
    try {
        if (!surveillanceProcess) {
            return res.json({
                message: 'Surveillance not running',
                status: 'stopped'
            });
        }

        surveillanceProcess.kill();
        surveillanceProcess = null;

        console.log('✅ Surveillance system stopped');

        res.json({
            message: 'Surveillance system stopped successfully',
            status: 'stopped'
        });

    } catch (error) {
        console.error('Error stopping surveillance:', error);
        res.status(500).json({
            error: 'Failed to stop surveillance system',
            details: error.message
        });
    }
});

/**
 * Get surveillance status
 */
router.get('/status', authenticate, (req, res) => {
    res.json({
        status: surveillanceProcess ? 'running' : 'stopped',
        pid: surveillanceProcess ? surveillanceProcess.pid : null
    });
});

/**
 * Get surveillance process (for internal use)
 */
router.getProcess = () => surveillanceProcess;

/**
 * Stop surveillance process (for internal use)
 */
router.stopProcess = () => {
    if (surveillanceProcess) {
        try {
            // Kill the process forcefully (Windows compatible)
            surveillanceProcess.kill('SIGTERM');
            
            // Also try to kill by PID on Windows
            if (process.platform === 'win32') {
                exec(`taskkill /F /PID ${surveillanceProcess.pid}`, (err) => {
                    if (err) console.log('Taskkill error:', err.message);
                });
            }
            
            surveillanceProcess = null;
            return true;
        } catch (err) {
            console.error('Error stopping surveillance:', err);
            surveillanceProcess = null;
            return false;
        }
    }
    return false;
};

module.exports = router;
