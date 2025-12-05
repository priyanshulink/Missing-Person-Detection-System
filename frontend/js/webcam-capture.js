/**
 * Webcam Capture Module
 * Handles webcam capture for adding persons
 */

class WebcamCapture {
    constructor() {
        this.stream = null;
        this.videoElement = null;
        this.capturedImage = null;
    }

    async startWebcam(videoElementId) {
        try {
            this.videoElement = document.getElementById(videoElementId);
            
            if (!this.videoElement) {
                throw new Error('Video element not found');
            }

            // Request webcam access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                },
                audio: false
            });

            this.videoElement.srcObject = this.stream;
            await this.videoElement.play();

            return true;
        } catch (error) {
            console.error('Error accessing webcam:', error);
            alert('Could not access webcam. Please check permissions.');
            return false;
        }
    }

    capturePhoto() {
        if (!this.videoElement) {
            throw new Error('Webcam not started');
        }

        // Create canvas to capture frame
        const canvas = document.createElement('canvas');
        canvas.width = this.videoElement.videoWidth;
        canvas.height = this.videoElement.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.videoElement, 0, 0);

        // Convert to blob
        return new Promise((resolve, reject) => {
            canvas.toBlob((blob) => {
                if (blob) {
                    this.capturedImage = blob;
                    resolve(blob);
                } else {
                    reject(new Error('Failed to capture image'));
                }
            }, 'image/jpeg', 0.95);
        });
    }

    getDataURL() {
        if (!this.videoElement) {
            return null;
        }

        const canvas = document.createElement('canvas');
        canvas.width = this.videoElement.videoWidth;
        canvas.height = this.videoElement.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.videoElement, 0, 0);

        return canvas.toDataURL('image/jpeg', 0.95);
    }

    stopWebcam() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }

        if (this.videoElement) {
            this.videoElement.srcObject = null;
        }
    }

    getCapturedImage() {
        return this.capturedImage;
    }
}

// Create global instance
const webcamCapture = new WebcamCapture();
