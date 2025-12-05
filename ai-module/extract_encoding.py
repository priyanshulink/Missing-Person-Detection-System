"""
Extract Face Encoding from Image
Standalone script to extract face encoding from a single image
"""

import sys
import json
import face_recognition
import numpy as np

def extract_face_encoding(image_path):
    """
    Extract face encoding from image file
    
    Args:
        image_path: Path to image file
        
    Returns:
        dict: Result with encoding or error
    """
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image, model='hog')
        
        if len(face_locations) == 0:
            return {
                'success': False,
                'error': 'No face detected in image',
                'faces_detected': 0
            }
        
        if len(face_locations) > 1:
            # Multiple faces detected, use the largest one
            face_locations = [max(face_locations, key=lambda loc: (loc[2] - loc[0]) * (loc[1] - loc[3]))]
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if len(face_encodings) == 0:
            return {
                'success': False,
                'error': 'Could not encode face',
                'faces_detected': len(face_locations)
            }
        
        # Convert numpy array to list for JSON serialization
        encoding = face_encodings[0].tolist()
        
        return {
            'success': True,
            'encoding': encoding,
            'faces_detected': len(face_locations),
            'face_location': {
                'top': int(face_locations[0][0]),
                'right': int(face_locations[0][1]),
                'bottom': int(face_locations[0][2]),
                'left': int(face_locations[0][3])
            }
        }
        
    except FileNotFoundError:
        return {
            'success': False,
            'error': f'Image file not found: {image_path}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'No image path provided'
        }))
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = extract_face_encoding(image_path)
    
    # Output result as JSON
    print(json.dumps(result))
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)
