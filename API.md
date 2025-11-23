# API Documentation

The application now exposes a RESTful API under the `/api` prefix.

## Authentication

The API uses session-based authentication backed by a remote MySQL database. You must log in to access protected endpoints.

### Health Check
**GET** `/api/health`

Checks the API status and database connection.

Response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Login
**POST** `/api/login`

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "success": true,
  "message": "Logged in successfully",
  "user": "your_username"
}
```

### Register
**POST** `/api/register`

Request body:
```json
{
  "username": "new_user",
  "password": "password123",
  "email": "user@example.com"
}
```

### Logout
**POST** `/api/logout`

## User Data

### Get Current User Profile
**GET** `/api/me`

Returns user profile information and progress summary.

Response:
```json
{
  "name": "User Name",
  "level": "Iniciante",
  "progress": {
    "completed_slides": 3,
    "total_slides": 8,
    "percentage": 37
  },
  ...
}
```

## Lessons & Progress

### Get Lessons List
**GET** `/api/lessons`

Returns the list of lessons and their completion status. If the user is logged in, `completed` status reflects their progress. If not logged in, all lessons are marked as incomplete.

Response:
```json
{
  "lessons": [
    {
      "number": 1,
      "title": "Bem-vindos...",
      "description": "...",
      "completed": true
    },
    ...
  ]
}
```

### Get Lesson Content
**GET** `/api/lessons/<lesson_number>/content`

Returns the HTML content of a specific lesson slide.

Response:
```json
{
  "content": "<h1>Bem-vindos...</h1><p>..."
}
```

### Update Progress
**POST** `/api/progress`

Marks a slide as completed. If the user is logged in, progress is saved. If not logged in, the request is accepted but no progress is persisted.

Request body:
```json
{
  "slide_number": 5
}
```
