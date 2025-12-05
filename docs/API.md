# API Documentation

## Base URL

```
http://localhost:3000
```

## Authentication

Most endpoints require authentication via JWT token.

**Header Format**:
```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### Register User

**POST** `/api/auth/register`

Register a new user account.

**Request Body**:
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "password": "string (required, min 6 chars)",
  "fullName": "string (optional)",
  "role": "string (optional, default: viewer)"
}
```

**Response** (201):
```json
{
  "message": "User registered successfully",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "username": "username",
    "email": "email@example.com",
    "role": "viewer",
    "createdAt": "2024-01-01T00:00:00.000Z"
  }
}
```

### Login

**POST** `/api/auth/login`

Authenticate user and receive JWT token.

**Request Body**:
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Response** (200):
```json
{
  "message": "Login successful",
  "token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "username": "username",
    "email": "email@example.com",
    "role": "admin",
    "lastLogin": "2024-01-01T00:00:00.000Z"
  }
}
```

### Get Current User

**GET** `/api/auth/me`

Get current authenticated user profile.

**Headers**: Requires authentication

**Response** (200):
```json
{
  "user": {
    "id": "user_id",
    "username": "username",
    "email": "email@example.com",
    "role": "admin",
    "fullName": "John Doe",
    "isActive": true,
    "lastLogin": "2024-01-01T00:00:00.000Z",
    "createdAt": "2024-01-01T00:00:00.000Z"
  }
}
```

---

## Person Management Endpoints

### List Persons

**GET** `/api/persons`

Get list of all persons with optional filters.

**Headers**: Requires authentication

**Query Parameters**:
- `status` (optional): Filter by status (missing/found/active)
- `priority` (optional): Filter by priority (low/medium/high/critical)
- `search` (optional): Text search in name and description
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 20): Items per page

**Response** (200):
```json
{
  "persons": [
    {
      "_id": "person_id",
      "name": "John Doe",
      "age": 30,
      "gender": "male",
      "status": "missing",
      "priority": "high",
      "description": "Last seen wearing blue jacket",
      "lastSeenLocation": "Central Park",
      "faceEncodings": [
        {
          "encoding": [0.1, 0.2, ...],
          "uploadedAt": "2024-01-01T00:00:00.000Z"
        }
      ],
      "reportedBy": {
        "username": "admin",
        "fullName": "Admin User"
      },
      "createdAt": "2024-01-01T00:00:00.000Z"
    }
  ],
  "totalPages": 5,
  "currentPage": 1,
  "total": 100
}
```

### Get Person by ID

**GET** `/api/persons/:id`

Get detailed information about a specific person.

**Headers**: Requires authentication

**Response** (200):
```json
{
  "person": {
    "_id": "person_id",
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "status": "missing",
    "priority": "high",
    "description": "Description here",
    "lastSeenLocation": "Location",
    "lastSeenDate": "2024-01-01T00:00:00.000Z",
    "contactInfo": {
      "phone": "+1234567890",
      "email": "contact@example.com"
    },
    "faceEncodings": [],
    "photos": [],
    "notes": [],
    "createdAt": "2024-01-01T00:00:00.000Z"
  }
}
```

### Create Person

**POST** `/api/persons`

Add a new person to the database.

**Headers**: Requires authentication (admin/operator role)

**Request Body**:
```json
{
  "name": "string (required)",
  "age": "number (optional)",
  "gender": "string (optional, male/female/other)",
  "status": "string (optional, missing/found/active)",
  "priority": "string (optional, low/medium/high/critical)",
  "description": "string (optional)",
  "lastSeenLocation": "string (optional)",
  "lastSeenDate": "date (optional)",
  "contactInfo": {
    "phone": "string (optional)",
    "email": "string (optional)",
    "address": "string (optional)"
  },
  "tags": ["string"] (optional)
}
```

**Response** (201):
```json
{
  "message": "Person created successfully",
  "person": { ... }
}
```

### Update Person

**PUT** `/api/persons/:id`

Update person information.

**Headers**: Requires authentication (admin/operator role)

**Request Body**: Same as Create Person

**Response** (200):
```json
{
  "message": "Person updated successfully",
  "person": { ... }
}
```

### Delete Person

**DELETE** `/api/persons/:id`

Soft delete a person (sets isActive to false).

**Headers**: Requires authentication (admin role)

**Response** (200):
```json
{
  "message": "Person deleted successfully"
}
```

### Add Face Encoding

**POST** `/api/persons/:id/encodings`

Add a face encoding to a person's profile.

**Headers**: Requires authentication (admin/operator role)

**Request Body**:
```json
{
  "encoding": [0.1, 0.2, ...],  // 128-dimensional array
  "imageUrl": "string (optional)"
}
```

**Response** (200):
```json
{
  "message": "Face encoding added successfully",
  "person": { ... }
}
```

---

## Face Recognition Endpoints

### Recognize Face

**POST** `/api/recognize`

Submit a face encoding for identification.

**Request Body**:
```json
{
  "encoding": [0.1, 0.2, ...],  // 128-dimensional array (required)
  "metadata": {
    "camera_id": "string (optional)",
    "timestamp": "string (optional)",
    "location": "string (optional)",
    "bbox": [x1, y1, x2, y2],  // optional
    "detection_confidence": 0.95  // optional
  }
}
```

**Response** (200) - Match Found:
```json
{
  "match_found": true,
  "person_id": "person_id",
  "name": "John Doe",
  "similarity": 0.87,
  "status": "missing",
  "priority": "high",
  "report_id": "report_id"
}
```

**Response** (200) - No Match:
```json
{
  "match_found": false,
  "message": "No matching person found"
}
```

### Batch Recognition

**POST** `/api/recognize/batch`

Submit multiple face encodings for identification.

**Request Body**:
```json
{
  "encodings": [
    {
      "encoding": [0.1, 0.2, ...],
      "metadata": { ... }
    },
    {
      "encoding": [0.3, 0.4, ...],
      "metadata": { ... }
    }
  ]
}
```

**Response** (200):
```json
{
  "results": [
    {
      "match_found": true,
      "person_id": "person_id",
      "name": "John Doe",
      "similarity": 0.87
    },
    {
      "match_found": false
    }
  ],
  "total": 2,
  "matches": 1
}
```

---

## Report Endpoints

### List Reports

**GET** `/api/reports`

Get list of all match reports.

**Headers**: Requires authentication

**Query Parameters**:
- `personId` (optional): Filter by person ID
- `cameraId` (optional): Filter by camera ID
- `verificationStatus` (optional): pending/confirmed/false_positive
- `startDate` (optional): Filter from date
- `endDate` (optional): Filter to date
- `page` (optional, default: 1)
- `limit` (optional, default: 20)

**Response** (200):
```json
{
  "reports": [
    {
      "_id": "report_id",
      "person": {
        "name": "John Doe",
        "status": "missing",
        "priority": "high"
      },
      "matchDetails": {
        "similarity": 0.87,
        "confidence": 0.95
      },
      "detectionInfo": {
        "cameraId": "camera_0",
        "timestamp": "2024-01-01T00:00:00.000Z",
        "location": "Main Entrance",
        "bbox": { "x1": 100, "y1": 100, "x2": 200, "y2": 200 }
      },
      "verificationStatus": "pending",
      "alertSent": true,
      "createdAt": "2024-01-01T00:00:00.000Z"
    }
  ],
  "totalPages": 10,
  "currentPage": 1,
  "total": 200
}
```

### Get Report by ID

**GET** `/api/reports/:id`

Get detailed report information.

**Headers**: Requires authentication

**Response** (200):
```json
{
  "report": { ... }
}
```

### Verify Report

**PATCH** `/api/reports/:id/verify`

Update report verification status.

**Headers**: Requires authentication (admin/operator role)

**Request Body**:
```json
{
  "verificationStatus": "confirmed"  // or "false_positive"
}
```

**Response** (200):
```json
{
  "message": "Report verification updated",
  "report": { ... }
}
```

### Get Report Statistics

**GET** `/api/reports/stats/summary`

Get summary statistics for reports.

**Headers**: Requires authentication

**Query Parameters**:
- `startDate` (optional): Filter from date
- `endDate` (optional): Filter to date

**Response** (200):
```json
{
  "totalReports": 150,
  "confirmedReports": 120,
  "falsePositives": 10,
  "pendingReports": 20,
  "reportsPerCamera": [
    { "_id": "camera_0", "count": 50 },
    { "_id": "camera_1", "count": 100 }
  ]
}
```

---

## Health Check

### Check API Health

**GET** `/health`

Check if API is running and database is connected.

**Response** (200):
```json
{
  "status": "OK",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "mongodb": "connected"
}
```

---

## Error Responses

All endpoints may return error responses:

**400 Bad Request**:
```json
{
  "error": "Error message describing what went wrong"
}
```

**401 Unauthorized**:
```json
{
  "error": "No token provided"
}
```

**403 Forbidden**:
```json
{
  "error": "Insufficient permissions"
}
```

**404 Not Found**:
```json
{
  "error": "Resource not found"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal server error"
}
```

---

## Socket.io Events

### Connection

Connect to Socket.io server:
```javascript
const socket = io('http://localhost:3000');
```

### Events

**Client → Server**:
- `subscribe`: Subscribe to notifications
  ```javascript
  socket.emit('subscribe', { userId: 'user_id' });
  ```

**Server → Client**:
- `match_found`: New match detected
  ```javascript
  socket.on('match_found', (data) => {
    // data: { reportId, personId, personName, similarity, cameraId, timestamp }
  });
  ```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production.

## CORS

CORS is enabled for all origins in development. Configure appropriately for production.
