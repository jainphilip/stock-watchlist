# 📈 Stock Watchlist

A Flask web application that allows users to build and manage a personal stock watchlist using live market data from the Yahoo Finance API.

---

## ✨ Features

- Add stocks to a watchlist
- Remove stocks from the watchlist
- Display:
  - Current Price
  - Daily Change
  - Daily Change (%)
  - Daily High
  - Daily Low
  - Trading Volume
- Persistent watchlist using JSON
- Flash messages for user feedback
- Clean and responsive interface

---

## 🛠️ Technologies Used

- Python
- Flask
- HTML5
- CSS3
- Yahoo Finance API (`yfinance`)
- JSON

---

## 📂 Project Structure

```
Stock-Watchlist/
│
├── app.py
├── utils.py
├── watchlist.json
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   └── styles.css
│
└── templates/
    └── index.html
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/stock-watchlist.git
```

### 2. Navigate into the project

```bash
cd stock-watchlist
```

### 3. (Optional) Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open your browser

```
http://127.0.0.1:5000
```

---

## 📸 Preview

<img width="1920" height="1080" alt="Screenshot 2026-08-04 195350" src="https://github.com/user-attachments/assets/bb473b84-2d2a-4227-bc6d-ea16a6f6c760" />



---

## 📄 License

This project is intended for educational purposes.
