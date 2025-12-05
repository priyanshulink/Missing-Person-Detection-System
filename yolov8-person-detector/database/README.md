# Person Database

This folder contains images of persons to be detected by the system.

## How to Add Persons

### Method 1: Using the add_person.py script (Recommended)

```bash
python add_person.py
```

This will:
1. Open your webcam
2. Let you capture a photo
3. Automatically save it with the correct name

### Method 2: Manual Addition

1. Take a clear photo of the person's face
2. Save it in the `persons/` folder
3. Name format: `firstname_lastname.jpg`

Examples:
- `persons/john_doe.jpg`
- `persons/jane_smith.jpg`
- `persons/bob_johnson.jpg`

## Photo Guidelines

For best recognition results:

✅ **DO:**
- Use good lighting (natural light is best)
- Face should be clearly visible
- Person looking at camera
- High resolution (at least 640x480)
- Save as JPG, JPEG, or PNG
- Use clear, front-facing photos

❌ **DON'T:**
- Avoid dark or backlit photos
- No sunglasses or face masks
- Avoid blurry images
- Don't use group photos
- Avoid extreme angles

## Supported Formats

- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`

## File Naming

The filename (without extension) will be used as the person's name in alerts.

Examples:
- `john_doe.jpg` → Alert: "John Doe detected"
- `jane_smith.png` → Alert: "Jane Smith detected"
- `security_guard.jpg` → Alert: "Security Guard detected"

## Multiple Photos Per Person

You can add multiple photos of the same person for better accuracy:
- `john_doe_1.jpg`
- `john_doe_2.jpg`
- `john_doe_3.jpg`

The system will treat these as separate entries, so it's better to choose the best single photo.

## Reload Database

After adding new photos while the system is running:
1. Press `r` key in the main application
2. Or restart the application

## Privacy Note

Keep this folder secure and only add photos of persons who have given consent to be monitored.
