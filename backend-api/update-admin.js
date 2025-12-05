/**
 * Update Admin Credentials Script
 * Updates the admin user with new username and password
 */

const mongoose = require('mongoose');
const User = require('./models/User');
require('dotenv').config();

async function updateAdmin() {
    try {
        console.log('Connecting to MongoDB...');
        await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/person_detection');
        console.log('✅ Connected to MongoDB');
        
        // Find existing admin user
        const existingAdmin = await User.findOne({ username: 'admin' });
        
        if (existingAdmin) {
            console.log('Found existing admin user, updating...');
            
            // Update credentials
            existingAdmin.username = 'ompriyanshu12@gmail.com';
            existingAdmin.email = 'ompriyanshu12@gmail.com';
            existingAdmin.password = 'pradeep3133'; // Will be hashed automatically by User model
            existingAdmin.fullName = 'Om Priyanshu';
            existingAdmin.role = 'admin';
            
            await existingAdmin.save();
            
            console.log('✅ Admin credentials updated successfully!');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log('New Login Credentials:');
            console.log('Username: ompriyanshu12@gmail.com');
            console.log('Password: pradeep3133');
            console.log('Role: admin');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        } else {
            console.log('No existing admin found, creating new admin...');
            
            // Create new admin
            const newAdmin = new User({
                username: 'ompriyanshu12@gmail.com',
                email: 'ompriyanshu12@gmail.com',
                password: 'pradeep3133', // Will be hashed automatically
                fullName: 'Om Priyanshu',
                role: 'admin'
            });
            
            await newAdmin.save();
            
            console.log('✅ New admin user created successfully!');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
            console.log('Login Credentials:');
            console.log('Username: ompriyanshu12@gmail.com');
            console.log('Password: pradeep3133');
            console.log('Role: admin');
            console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        }
        
        await mongoose.connection.close();
        console.log('✅ Database connection closed');
        process.exit(0);
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

updateAdmin();
