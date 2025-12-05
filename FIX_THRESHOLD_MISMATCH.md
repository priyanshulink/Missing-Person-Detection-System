# 🔍 Threshold Mismatch Issue Explained

## 🎯 The Problem

You're seeing different behavior between:
1. **Camera Surveillance (Python)** - Shows alerts at 60%+
2. **Backend API (Node.js)** - Shows alerts below 60%

## 🔍 Root Cause

The two systems use **different similarity calculation methods**:

### Python Surveillance:
```python
# Uses face_recognition library
distance = face_recognition.face_distance(known_faces, detected_face)
similarity = 1 - distance

# Threshold: distance <= 0.4 means similarity >= 60%
if distance <= 0.4:  # 60% similarity
    send_alert()
```

### Backend API:
```javascript
// Uses custom exponential decay function
distance = euclideanDistance(encoding1, encoding2)
similarity = Math.exp(-distance / 2)

// Threshold: similarity >= 0.6 means ~60% similarity
if (similarity >= 0.6) {  // ~60% similarity
    send_alert()
```

**The issue:** These two methods produce **different similarity scores** for the same face comparison!

## 📊 Example Comparison

Same face pair compared by both systems:

| System | Method | Distance | Similarity | Alert? |
|--------|--------|----------|------------|--------|
| Python | `1 - distance` | 0.35 | 65% | ✅ YES |
| Backend | `exp(-distance/2)` | 0.35 | 84% | ✅ YES |

**Notice:** Same distance (0.35) gives different similarity scores!

## ✅ Solution: Align Both Systems

We need to make the backend use the **same calculation** as Python.

### Option 1: Change Backend to Match Python (Recommended)

Update `backend-api/utils/faceUtils.js`:

```javascript
const calculateSimilarity = (encoding1, encoding2) => {
  try {
    if (!encoding1 || !encoding2 || encoding1.length !== encoding2.length) {
      return 0;
    }
    
    // Use same method as Python face_recognition
    const distance = euclideanDistance(encoding1, encoding2);
    
    // Convert to similarity (same as Python: similarity = 1 - distance)
    // Clamp distance to max of 1.0 for similarity calculation
    const clampedDistance = Math.min(distance, 1.0);
    const similarity = 1 - clampedDistance;
    
    return Math.max(similarity, 0);  // Ensure non-negative
    
  } catch (error) {
    console.error('Error calculating similarity:', error);
    return 0;
  }
};
```

This makes backend similarity match Python exactly.

### Option 2: Adjust Backend Threshold

Keep current calculation but adjust threshold to match Python behavior.

Current backend threshold: 0.6
Equivalent Python threshold: ~0.4

We need to find what backend threshold gives same results as Python's 0.4.

## 🔧 Implementation

Let me update the backend to use the same calculation as Python:
