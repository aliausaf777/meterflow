# ⚡ MeterFlow — API Gateway & Usage-Based Billing Platform

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Overview

MeterFlow is a full-stack API Gateway and Usage-Based Billing Platform built using **FastAPI** and **React**.

The platform enables developers and businesses to create APIs, generate API keys, route requests through a centralized gateway, monitor usage analytics, and manage billing through a unified dashboard.

Designed as a portfolio-grade SaaS project, MeterFlow demonstrates modern backend architecture, authentication systems, API management, analytics tracking, and billing workflows.

---

## ✨ Features

### 🔐 Authentication & Security

- JWT Authentication
- Secure Login System
- Protected API Routes
- API Key Generation
- API Key Revocation

### 🚪 API Gateway

- Route Requests Through Gateway
- API Registration & Management
- Centralized Request Processing
- Request Monitoring

### 📊 Analytics Dashboard

- API Usage Tracking
- Request Analytics
- Endpoint Monitoring
- Usage Metrics Dashboard
- Activity Insights

### 💳 Billing System

- Usage-Based Billing
- Invoice Generation
- Billing Dashboard
- Cost Tracking

### 📚 Developer Experience

- Swagger API Documentation
- FastAPI Interactive Docs
- RESTful API Design
- Modern Dashboard UI

---

## 🏗️ System Architecture

```text
┌─────────────────────────────┐
│       React Frontend        │
│     Dashboard & Billing     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        FastAPI API          │
│ Auth │ Gateway │ Billing │ Analytics
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         SQLite DB           │
│ Users │ APIs │ Usage Logs   │
└─────────────────────────────┘
```

---

## 🛠 Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

### Frontend

- React.js
- CSS

---

## 📁 Project Structure

```bash
MeterFlow/
│
├── backend/
│   ├── routers/
│   ├── models/
│   ├── services/
│   ├── database.py
│   ├── auth.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── src/components/
│
├── README.md
└── requirements.txt
```

---

## 🚀 Core Functionality

### API Management

- Register APIs
- Manage API Endpoints
- Generate API Keys
- Revoke API Keys

### Request Tracking

- Monitor API Calls
- Track Endpoint Usage
- Log Requests
- Usage Statistics

### Billing

- Usage-Based Pricing
- Billing Dashboard
- Invoice Tracking
- Consumption Reports

### Analytics

- Request Volume Metrics
- API Performance Monitoring
- User Activity Insights
- Usage Trends

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/meterflow.git

cd meterflow
```

---

## Backend Setup

### Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

### Run Backend Server

```bash
uvicorn main:app --reload
```

Backend Server:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

### Navigate to Frontend

```bash
cd frontend
```

### Install Dependencies

```bash
npm install
```

### Start Frontend

```bash
npm start
```

Frontend Application:

```text
http://localhost:3000
```

---

## 📚 API Documentation

Interactive Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to:

- Test API Endpoints
- Generate Authentication Tokens
- Explore Request Schemas
- Validate API Responses

---

## 🎯 Demo Features

The platform supports:

✅ API Registration

✅ API Gateway Routing

✅ API Key Management

✅ Request Analytics

✅ Usage Tracking

✅ Billing Dashboard

✅ Invoice Management

✅ JWT Authentication

---

## 📈 Use Cases

### SaaS Platforms

Track customer API consumption and generate usage-based invoices.

### Internal Developer Platforms

Provide centralized API access and monitoring for development teams.

### API Monetization

Offer paid API services with metered billing and analytics.

### Microservice Gateways

Manage service traffic through a single entry point.

---

## 🔒 Security Features

- JWT Authentication
- Protected Endpoints
- API Key Validation
- Request Logging
- Secure Access Control

---

## 📚 Learning Outcomes

This project helped strengthen my understanding of:

- API Gateway Architecture
- FastAPI Development
- Authentication & Authorization
- Usage-Based Billing Systems
- Request Tracking
- Analytics Dashboards
- SQLAlchemy ORM
- Frontend–Backend Integration
- SaaS Platform Development

---

## 🔮 Future Improvements

- PostgreSQL Support
- Stripe Payment Integration
- Rate Limiting
- WebSocket Live Analytics
- Team Workspaces
- Subscription Plans
- Multi-Tenant Architecture
- Docker Deployment
- Kubernetes Support
- Cloud Hosting

---

## 📈 Resume Highlights

This project demonstrates:

- Full-Stack Development
- API Gateway Design
- SaaS Architecture
- Usage-Based Billing Systems
- Authentication & Authorization
- Analytics Dashboard Development
- Database Design
- FastAPI Backend Development
- React Frontend Development
- Production-Oriented Software Engineering

---

## 🧪 Demo Credentials

> For demonstration purposes only.

**Email**

```text
mohdausafali786@gmail.com
```

**Password**

```text
0000
```

---

## 👨‍💻 Author

**Mohammed Azhad Ali Ausaf**

Full Stack Developer

---

## ⭐ Support

If you found this project useful, consider giving the repository a star.
