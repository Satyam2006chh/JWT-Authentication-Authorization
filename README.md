# JWT Authentication & Authorization with FastAPI

A secure REST API built with FastAPI that implements JWT-based authentication and authorization for user management.

## 📋 Project Overview

This project demonstrates a complete authentication system using JSON Web Tokens (JWT) with FastAPI. It includes user registration, login, and protected routes that require authentication.

## 🚀 Features

- **User Registration** - Create new user accounts with email validation
- **User Login** - Authenticate users and issue JWT tokens
- **Protected Routes** - Access user profile with JWT authentication
- **Password Hashing** - Secure password storage using bcrypt
- **Token-based Auth** - Stateless authentication using JWT
- **SQLite Database** - Lightweight database for user storage
- **Role-based System** - User role management (default: "user")

## 🛠️ Technologies Used

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI applications

### Authentication & Security
- **python-jose[cryptography]** - JWT token creation and verification
- **passlib[bcrypt]** - Password hashing using bcrypt algorithm
- **OAuth2PasswordBearer** - OAuth2 authentication scheme

### Database
- **SQLAlchemy** - SQL toolkit and ORM for database operations
- **SQLite** - Lightweight database for data persistence

### Utilities
- **python-dotenv** - Environment variable management
- **python-multipart** - Form data parsing for login endpoint
- **Pydantic** - Data validation using Python type annotations

## 📁 Project Structure

```
JWT-Authentication-Authorization/
├── app/
│   ├── routers/
│   │   └── users.py          # User routes (register, login, profile)
│   ├── auth.py                # Authentication logic & JWT handling
│   ├── database.py            # Database configuration & session
│   ├── main.py                # FastAPI app initialization
│   ├── models.py              # SQLAlchemy database models
│   └── schemas.py             # Pydantic schemas for validation
├── .env                       # Environment variables (SECRET_KEY, etc.)
├── .gitignore                 # Git ignore file
├── requirements.txt           # Python dependencies
└── users.db                   # SQLite database (auto-generated)
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7+
- pip

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd JWT-Authentication-Authorization
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./users.db
```

⚠️ **Important**: Change the `SECRET_KEY` to a strong, random string in production!

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Endpoints

### 1. Register User
**POST** `/users/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "message": "User created successfully"
}
```

### 2. Login
**POST** `/users/login`

Authenticate and receive JWT token.

**Request Body (Form Data):**
```
username: johndoe
password: securepassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Current User Profile
**GET** `/users/me`

Get authenticated user's profile (Protected Route).

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "role": "user"
}
```

## 🔐 How It Works

### Authentication Flow

1. **Registration**: User submits credentials → Password is hashed with bcrypt → User stored in database
2. **Login**: User submits credentials → Password verified → JWT token generated and returned
3. **Protected Routes**: User sends JWT in Authorization header → Token verified → Access granted

### JWT Token Structure

The JWT token contains:
- **sub**: Username (subject)
- **exp**: Expiration timestamp
- **Signature**: Encrypted with SECRET_KEY using HS256 algorithm

### Security Features

- Passwords are hashed using bcrypt (never stored in plain text)
- JWT tokens expire after 30 minutes (configurable)
- OAuth2 password bearer scheme for token authentication
- Database queries use SQLAlchemy ORM to prevent SQL injection

## 🧪 Testing the API

### Using cURL

**Register:**
```bash
curl -X POST "http://127.0.0.1:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'
```

**Login:**
```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test123"
```

**Get Profile:**
```bash
curl -X GET "http://127.0.0.1:8000/users/me" \
  -H "Authorization: Bearer <your-token-here>"
```

### Using FastAPI Docs

Visit `http://127.0.0.1:8000/docs` for interactive API documentation (Swagger UI).

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Secret key for JWT signing | (required) |
| `ALGORITHM` | JWT encoding algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `DATABASE_URL` | Database connection string | sqlite:///./users.db |

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available for educational purposes.

## 🔮 Future Enhancements

- [ ] Refresh token implementation
- [ ] Role-based access control (RBAC)
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Rate limiting
- [ ] PostgreSQL/MySQL support
- [ ] Docker containerization

---

**Built with ❤️ using FastAPI**
