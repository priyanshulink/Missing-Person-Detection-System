/**
 * Firebase Cloud Messaging Service
 * Handles push notifications via Firebase
 */

const admin = require('firebase-admin');
const User = require('../models/User');

let firebaseInitialized = false;

/**
 * Initialize Firebase Admin SDK
 */
const initializeFirebase = () => {
  try {
    const credentialsPath = process.env.FIREBASE_CREDENTIALS_PATH;
    
    if (!credentialsPath) {
      throw new Error('FIREBASE_CREDENTIALS_PATH not set in environment');
    }
    
    const serviceAccount = require(credentialsPath);
    
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });
    
    firebaseInitialized = true;
    console.log('Firebase Admin SDK initialized');
    
  } catch (error) {
    console.warn('Firebase initialization skipped:', error.message);
    firebaseInitialized = false;
  }
};

/**
 * Send notification to all active users
 */
const sendNotification = async ({ title, body, data = {} }) => {
  if (!firebaseInitialized) {
    console.warn('Firebase not initialized, skipping notification');
    return { success: false, error: 'Firebase not initialized' };
  }
  
  try {
    // Get all active users with FCM tokens
    const users = await User.find({
      isActive: true,
      fcmToken: { $exists: true, $ne: null }
    });
    
    if (users.length === 0) {
      console.log('No users with FCM tokens found');
      return { success: true, sent: 0 };
    }
    
    const tokens = users.map(user => user.fcmToken);
    
    // Create message
    const message = {
      notification: {
        title,
        body
      },
      data: {
        ...data,
        timestamp: new Date().toISOString()
      },
      tokens
    };
    
    // Send multicast message
    const response = await admin.messaging().sendMulticast(message);
    
    console.log(`Notification sent: ${response.successCount} successful, ${response.failureCount} failed`);
    
    // Handle failed tokens
    if (response.failureCount > 0) {
      const failedTokens = [];
      response.responses.forEach((resp, idx) => {
        if (!resp.success) {
          failedTokens.push(tokens[idx]);
        }
      });
      
      // Remove invalid tokens
      await User.updateMany(
        { fcmToken: { $in: failedTokens } },
        { $set: { fcmToken: null } }
      );
      
      console.log(`Removed ${failedTokens.length} invalid FCM tokens`);
    }
    
    return {
      success: true,
      sent: response.successCount,
      failed: response.failureCount
    };
    
  } catch (error) {
    console.error('Error sending notification:', error);
    return {
      success: false,
      error: error.message
    };
  }
};

/**
 * Send notification to specific user
 */
const sendNotificationToUser = async (userId, { title, body, data = {} }) => {
  if (!firebaseInitialized) {
    console.warn('Firebase not initialized, skipping notification');
    return { success: false, error: 'Firebase not initialized' };
  }
  
  try {
    const user = await User.findById(userId);
    
    if (!user || !user.fcmToken) {
      return { success: false, error: 'User not found or no FCM token' };
    }
    
    const message = {
      notification: {
        title,
        body
      },
      data: {
        ...data,
        timestamp: new Date().toISOString()
      },
      token: user.fcmToken
    };
    
    await admin.messaging().send(message);
    
    console.log(`Notification sent to user ${userId}`);
    
    return { success: true };
    
  } catch (error) {
    console.error('Error sending notification to user:', error);
    
    // Remove invalid token
    if (error.code === 'messaging/invalid-registration-token' ||
        error.code === 'messaging/registration-token-not-registered') {
      await User.findByIdAndUpdate(userId, { fcmToken: null });
    }
    
    return {
      success: false,
      error: error.message
    };
  }
};

module.exports = {
  initializeFirebase,
  sendNotification,
  sendNotificationToUser
};
