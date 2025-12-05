/**
 * Face Recognition Utilities
 * Helper functions for face encoding comparison
 */

/**
 * Calculate Euclidean distance between two vectors (optimized)
 */
const euclideanDistance = (vector1, vector2) => {
  if (vector1.length !== vector2.length) {
    throw new Error('Vectors must have the same length');
  }
  
  // Use typed arrays for faster computation if available
  const len = vector1.length;
  let sum = 0;
  
  // Unroll loop for better performance (process 4 elements at a time)
  let i = 0;
  const remainder = len % 4;
  const limit = len - remainder;
  
  for (; i < limit; i += 4) {
    const diff0 = vector1[i] - vector2[i];
    const diff1 = vector1[i + 1] - vector2[i + 1];
    const diff2 = vector1[i + 2] - vector2[i + 2];
    const diff3 = vector1[i + 3] - vector2[i + 3];
    sum += diff0 * diff0 + diff1 * diff1 + diff2 * diff2 + diff3 * diff3;
  }
  
  // Handle remaining elements
  for (; i < len; i++) {
    const diff = vector1[i] - vector2[i];
    sum += diff * diff;
  }
  
  return Math.sqrt(sum);
};

/**
 * Calculate cosine similarity between two vectors (optimized)
 */
const cosineSimilarity = (vector1, vector2) => {
  if (vector1.length !== vector2.length) {
    throw new Error('Vectors must have the same length');
  }
  
  const len = vector1.length;
  let dotProduct = 0;
  let magnitude1 = 0;
  let magnitude2 = 0;
  
  // Unroll loop for better performance
  let i = 0;
  const remainder = len % 4;
  const limit = len - remainder;
  
  for (; i < limit; i += 4) {
    const v1_0 = vector1[i], v2_0 = vector2[i];
    const v1_1 = vector1[i + 1], v2_1 = vector2[i + 1];
    const v1_2 = vector1[i + 2], v2_2 = vector2[i + 2];
    const v1_3 = vector1[i + 3], v2_3 = vector2[i + 3];
    
    dotProduct += v1_0 * v2_0 + v1_1 * v2_1 + v1_2 * v2_2 + v1_3 * v2_3;
    magnitude1 += v1_0 * v1_0 + v1_1 * v1_1 + v1_2 * v1_2 + v1_3 * v1_3;
    magnitude2 += v2_0 * v2_0 + v2_1 * v2_1 + v2_2 * v2_2 + v2_3 * v2_3;
  }
  
  // Handle remaining elements
  for (; i < len; i++) {
    const v1 = vector1[i], v2 = vector2[i];
    dotProduct += v1 * v2;
    magnitude1 += v1 * v1;
    magnitude2 += v2 * v2;
  }
  
  magnitude1 = Math.sqrt(magnitude1);
  magnitude2 = Math.sqrt(magnitude2);
  
  if (magnitude1 === 0 || magnitude2 === 0) {
    return 0;
  }
  
  return dotProduct / (magnitude1 * magnitude2);
};

/**
 * Calculate similarity between two face encodings (optimized)
 * Returns a value between 0 and 1 (higher is more similar)
 * Uses same method as Python face_recognition library: similarity = 1 - distance
 */
const calculateSimilarity = (encoding1, encoding2) => {
  try {
    // Quick validation
    if (!encoding1 || !encoding2 || encoding1.length !== encoding2.length) {
      return 0;
    }
    
    // Use Euclidean distance
    const distance = euclideanDistance(encoding1, encoding2);
    
    // Convert distance to similarity using same method as Python face_recognition
    // similarity = 1 - distance (clamped to 0-1 range)
    // Distance of 0 = 100% similarity (1.0)
    // Distance of 0.4 = 60% similarity (0.6)
    // Distance of 0.6 = 40% similarity (0.4)
    const clampedDistance = Math.min(distance, 1.0);
    const similarity = 1 - clampedDistance;
    
    return Math.max(similarity, 0);  // Ensure non-negative
    
  } catch (error) {
    console.error('Error calculating similarity:', error);
    return 0;
  }
};

/**
 * Check if two face encodings match based on threshold
 */
const isFaceMatch = (encoding1, encoding2, threshold = 0.6) => {
  const similarity = calculateSimilarity(encoding1, encoding2);
  return similarity >= threshold;
};

/**
 * Find best match from a list of face encodings
 */
const findBestMatch = (targetEncoding, encodingsList, threshold = 0.6) => {
  let bestMatch = null;
  let bestSimilarity = 0;
  
  for (let i = 0; i < encodingsList.length; i++) {
    const similarity = calculateSimilarity(targetEncoding, encodingsList[i]);
    
    if (similarity > bestSimilarity && similarity >= threshold) {
      bestSimilarity = similarity;
      bestMatch = {
        index: i,
        similarity: similarity
      };
    }
  }
  
  return bestMatch;
};

/**
 * Normalize face encoding vector
 */
const normalizeEncoding = (encoding) => {
  const magnitude = Math.sqrt(
    encoding.reduce((sum, val) => sum + val * val, 0)
  );
  
  if (magnitude === 0) {
    return encoding;
  }
  
  return encoding.map(val => val / magnitude);
};

/**
 * Validate face encoding format
 */
const isValidEncoding = (encoding) => {
  if (!Array.isArray(encoding)) {
    return false;
  }
  
  if (encoding.length !== 128) {
    return false;
  }
  
  // Check if all elements are numbers
  return encoding.every(val => typeof val === 'number' && !isNaN(val));
};

module.exports = {
  euclideanDistance,
  cosineSimilarity,
  calculateSimilarity,
  isFaceMatch,
  findBestMatch,
  normalizeEncoding,
  isValidEncoding
};
