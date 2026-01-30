# Clixs – Marketplace with Real-Time Chat

Clixs is a full-stack marketplace web application where users can **sell or rent items**, manage profiles, and communicate in **real-time chat** using WebSockets.
<img width="1901" height="904" alt="image" src="https://github.com/user-attachments/assets/b2bab96e-8578-4222-a95a-b6d815e954cb" />

The backend is built with **Django, Django REST Framework, and Django Channels**, and the frontend uses server-rendered templates with modern UI and JavaScript for real-time messaging.

---

## 🚀 Features

### Core Features
- Custom user authentication (phone number based)
- User registration, login, profile management
- Create, list, update, delete items (Sell / Rent)
- Upload multiple images per item
- Contact form, feedback, and report system
- Admin dashboard for moderation

### Chat Features
- One-to-one chat between buyer and seller
- Real-time messaging using WebSockets (Django Channels)
- Conversation list
- Message history per chat
- Secure and private messaging

---

## 🛠 Tech Stack

### Backend
- Python 3.x  
- Django  
- Django REST Framework  
- Django Channels  
- PostgreSQL  
- Redis (for channel layer)  

### Frontend
- Django Templates (HTML)
- CSS (Dark UI)
- Vanilla JavaScript
- WebSocket API

### Authentication
- JWT (SimpleJWT)
- Custom User Model (phone number login)

---

## 📂 Project Structure (Simplified)
<pre>
Clixs/
├── api/
│ ├── models.py # User, Item, Chat, Message, etc.
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ ├── consumers.py # WebSocket consumer
│ ├── routing.py # WebSocket routes
│
├── Clixs/
│ ├── settings.py
│ ├── asgi.py # Channels + WebSocket config
│ ├── urls.py
│
├── templates/
│ ├── chats.html
│ ├── home.html
│ ├── login.html
│ └── ...
│
├── manage.py
└── README.md
</pre>

---

## 🔗 API Endpoints (Chat Related)

    GET /api/v1/chats/
    POST /api/v1/chats/create/
    GET /api/v1/chats/<chat_id>/messages/
    POST /api/v1/messages/send/
    WS ws://<host>/ws/chat/<chat_id>/

---

## ⚙️ Setup Instructions

### 1. Clone the repository
    git clone github.com/Akshatswami610/Clixs
    cd Clixs

### 2. Create a virtual environment
    python -m venv venv
    source venv/bin/activate   # Linux / Mac
    venv\Scripts\activate     # Windows
    
### 3. Install dependencies
    pip install -r requirements.txt
    
### 4. Configure environment variables
  #### Create a .env file:
      SECRET_KEY=your-secret-key
      NAME=clixs
      USER=postgres
      PASSWORD=your-db-password
      HOST=localhost
      PORT=5432
      
### 5. Run Redis (for WebSockets)
    redis-server
    
### 6. Apply migrations
    python manage.py makemigrations
    python manage.py migrate
    
### 7. Create superuser
    python manage.py createsuperuser
    
### 8. Run the development server
    python manage.py runserver
    
Open in browser:
http://127.0.0.1:8000/

---

## 🔌 WebSocket Configuration
  ### WebSocket URL pattern:
    ws://127.0.0.1:8000/ws/chat/<chat_id>/
    
  ### Channels is configured in:
  - Clixs/asgi.py

  - api/routing.py

  - api/consumers.py

Redis is used as the channel layer.

---

## 🧪 Testing Chat
1. Log in as two different users in two browsers

2. Create or open a chat

3. Messages should appear in real-time without refresh

---

## 🔐 Security Notes
  - JWT authentication for APIs

 - WebSocket authentication via AuthMiddlewareStack

 - Buyer/seller validation in chat consumer

 - Only chat participants can send/receive messages

---

## 📌 Future Improvements
 - Typing indicator

 - Read receipts

 - Online/offline status

 - Push notifications

 - Group chats

---

## 👨‍💻 Author
Developed and Designed by [Akshat Swami](https://akshatswamipy.vercel.app)

---

## 📄 License
This project is for educational and personal use.
