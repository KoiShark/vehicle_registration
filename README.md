# 🚗 Vehicle Registration System

This project combines an **Odoo v16** module (`ridery_vehicle_registration`) with a **Node.js API** (`ridery_vehicle_registration_api`) for comprehensive vehicle registration management.

![System Architecture](https://via.placeholder.com/800x400?text=Vehicle+Registration+System+Architecture)

## 📦 System Requirements

### Core Requirements
- **Odoo v16** (Python 3.7+)
- **Node.js** v22.18.0
- **PostgreSQL** 12+

---

## 🛠️ Installation Guide

### 1. Odoo Module Installation

```bash
# Clone repository
git clone https://github.com/KoiShark/vehicle_registration.git
cd vehicle_registration/ridery_vehicle_registration

# Install module
cp -r vehicle_registration /path/to/odoo/addons/

## Activation Steps:

1. Log in to Odoo as administrator
2. Enable Developer Mode
3. Navigate to **Apps → Update Apps List**
4. Search for "Vehicle Registration"
5. Click **Install**

### 2. Vehicle API Setup

cd /vehicle_registration/ridery_vehicle_registration_api

# Install dependencies
npm install

# Run API
npm run dev

## 🌐 Available Endpoints

| Endpoint                     | Method | Description                          |
|------------------------------|--------|--------------------------------------|
| `/api/vehicles`              | GET    | Get all registered vehicles          |
| `/api/vehicles/:id`          | GET    | Get specific vehicle by ID           |
| `/api/vehicles/register`     | POST   | Register new vehicle (Odoo default)  |

The API server will be running at:  
🔗 [http://localhost:3000](http://localhost:3000)
