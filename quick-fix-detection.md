# Quick Fix for Detection Issues

## 🔍 Why Detection Might Not Work

1. **Different lighting** - Photo vs live webcam
2. **Different angle** - Photo was front-facing, you're at an angle
3. **Different distance** - Too close or too far from camera
4. **Glasses/accessories** - Wearing something different
5. **Threshold too high** - Need lower similarity threshold

## ✅ Solutions (Try in Order)

### **Solution 1: Test Your Similarity Score**

Run this to see exact match percentage:
```bash
python test-live-detection.py
```

- Webcam will open
- Press **SPACE** to test
- Look at similarity percentage
- Need ≥40% to trigger alert

### **Solution 2: Lower Threshold (DONE)**

I just lowered it to 40% (was 45%). Restart surveillance:

```bash
# Stop surveillance
Get-Process python | Stop-Process -Force

# Restart (login again to dashboard)
```

### **Solution 3: Add More Photos**

Add 2-3 more photos of yourself:

1. Go to dashboard → Persons
2. Find your person ("om singh")
3. Click "Add Photo" or edit
4. Upload photos from:
   - Different angles (left, right, front)
   - Different lighting
   - With/without glasses

### **Solution 4: Improve Lighting**

- Face the camera directly
- Ensure good lighting on your face
- Avoid backlighting (light behind you)
- Move closer to camera (but not too close)

### **Solution 5: Check Face Detection**

Make sure YOLO is detecting you as a person:
- Look at surveillance window
- Should see RED or GREEN box around you
- If no box → YOLO isn't detecting person
- If RED box → Face detected but no match
- If GREEN box → Match found!

## 🎯 Quick Test Steps

1. **Run test script**:
   ```bash
   python test-live-detection.py
   ```

2. **Position yourself**:
   - Face camera directly
   - Good lighting
   - Normal distance (2-3 feet)

3. **Press SPACE** to test

4. **Check results**:
   - If similarity is 35-39% → Need lower threshold or more photos
   - If similarity is <30% → Add more photos
   - If similarity is ≥40% → Should work! Restart surveillance

## 🔧 Manual Threshold Adjustment

Edit this file:
```
ai-module/yolo_integrated_surveillance.py
Line 33: CONFIDENCE_THRESHOLD = 0.40
```

Try these values:
- `0.40` - Current (40% match needed)
- `0.35` - More lenient (35% match needed)
- `0.30` - Very lenient (30% match needed)

**Lower = More false positives but catches more matches**

## 📊 Expected Behavior

**When working correctly:**
```
1. YOLO detects person → RED box appears
2. Face recognition runs → Extracts encoding
3. Compares with database → Calculates similarity
4. If ≥40% → GREEN box + Alert
5. Dashboard shows: "🚨 om singh detected!"
```

## 🚀 After Fixing

Once detection works:
1. You'll see GREEN box around your face
2. Backend logs: "🚨 ALERT: om singh detected!"
3. Dashboard shows alert notification
4. Report created in database

---

**Try the test script first to see your exact similarity score!**
