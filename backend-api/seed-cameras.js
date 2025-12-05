/**
 * Seed Cameras Script
 * Populates database with sample camera configurations
 */

const mongoose = require('mongoose');
const Camera = require('./models/Camera');
require('dotenv').config();

const sampleCameras = [
  {
    cameraId: 'cam01',
    name: 'Main Gate Camera',
    location: 'Front Entrance',
    streamUrl: 'http://192.168.1.20:8080/video',
    status: 'active',
    description: 'Main entrance monitoring camera'
  },
  {
    cameraId: 'cam02',
    name: 'Library Hall Camera',
    location: 'Library First Floor',
    streamUrl: 'http://10.20.215.113:8080/video',
    status: 'active',
    description: 'Library hall surveillance (Working camera)'
  },
  {
    cameraId: 'cam03',
    name: 'Parking Lot Camera',
    location: 'Building A Parking',
    streamUrl: 'http://192.168.1.45:8080/video',
    status: 'active',
    description: 'Parking area monitoring'
  },
  {
    cameraId: 'cam04',
    name: 'Cafeteria Camera',
    location: 'Ground Floor Cafeteria',
    streamUrl: 'http://192.168.1.50:8080/video',
    status: 'active',
    description: 'Cafeteria surveillance'
  },
  {
    cameraId: 'cam_local',
    name: 'Local Webcam',
    location: 'Development Machine',
    streamUrl: '0',  // Use 0 for default webcam
    status: 'active',
    description: 'Local development camera'
  }
];

async function seedCameras() {
  try {
    // Connect to MongoDB
    const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/person_detection';
    
    await mongoose.connect(MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    
    console.log('✅ Connected to MongoDB');
    
    // Clear existing cameras (optional)
    const clearExisting = process.argv.includes('--clear');
    if (clearExisting) {
      await Camera.deleteMany({});
      console.log('🗑️  Cleared existing cameras');
    }
    
    // Insert sample cameras
    for (const cameraData of sampleCameras) {
      try {
        // Check if camera already exists
        const existing = await Camera.findOne({ cameraId: cameraData.cameraId });
        
        if (existing) {
          console.log(`⚠️  Camera ${cameraData.cameraId} already exists, skipping...`);
          continue;
        }
        
        const camera = new Camera(cameraData);
        await camera.save();
        console.log(`✅ Added camera: ${cameraData.name} (${cameraData.cameraId})`);
      } catch (error) {
        console.error(`❌ Error adding camera ${cameraData.cameraId}:`, error.message);
      }
    }
    
    console.log('\n✅ Camera seeding completed');
    
    // Display all cameras
    const allCameras = await Camera.find({});
    console.log(`\n📹 Total cameras in database: ${allCameras.length}`);
    
    allCameras.forEach(cam => {
      console.log(`  - ${cam.name} (${cam.cameraId}) - ${cam.location} [${cam.status}]`);
    });
    
  } catch (error) {
    console.error('❌ Error seeding cameras:', error);
  } finally {
    await mongoose.connection.close();
    console.log('\n👋 Database connection closed');
  }
}

// Run the seeder
seedCameras();
