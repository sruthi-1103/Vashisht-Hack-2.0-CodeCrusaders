# Vashisht-Hack-2.0-CodeCrusaders
# Food Waste Management System

## Project Overview
This is a **Flask-based web application** designed to tackle food waste by connecting surplus food providers with consumers and organizations. It includes user authentication, food tracking, and donation features.

## Features
- **User Authentication** (Sign Up, Login)
- **Admin Dashboard** (Manage users, track food waste data)
- **Food Donation System**
- **Smart Inventory Tracking**
- **Data Analytics for Food Waste Reduction**

## Tech Stack
- **Backend**: Python (Flask), Flask-MySQLdb
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Security**: Password hashing

## Installation Guide
### 1. Clone the Repository
```sh
git clone <repository-link>
cd project-folder
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Configure Database
1. Install MySQL and create a database.
2. Import `database.sql`:
```sh
mysql -u root -p < database.sql
```
3. Update `main.py` with your MySQL credentials.

### 4. Run the Application
```sh
python main.py
```
Then, open `http://127.0.0.1:5000/` in your browser.

## Demo Video
[Watch Here](https://drive.google.com/file/d/1jgwYieREzxBAQPZoch_OPBdGITN676fI/view?usp=drivesdk)

## Contribution
Feel free to fork this repo, raise issues, and contribute!

## License
MIT License

