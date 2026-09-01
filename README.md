# GRIET MEGA BLOOD DONATION 2026 🩸

Official website for the **GRIET Mega Blood Donation 2026** campaign organized by **NSS GRIET** at Gokaraju Rangaraju Institute of Engineering and Technology (Autonomous).

---

## 📌 Campaign Details
- **Project Name:** GRIET Mega Blood Donation 2026
- **Organized By:** NSS GRIET & Gokaraju Rangaraju Institute of Engineering and Technology
- **Venue:** GRIET Campus, Bachupally, Hyderabad
- **Target Goal:** 800+ Blood Units
- **Registration Deadline:** 21 September 2026

---

## 🚀 Key Features
1. **Modern Fintech/Campaign UI**: Warm white/pink palette, red accents, smooth animations, responsive cards, and clean typography.
2. **Real-Time Live Countdown**: Counts down accurately to the deadline (21 September 2026 23:59:59 IST).
3. **Live SQLite Registration Counter**: Separates registered donors count from blood units target.
4. **Donor Registration System**:
   - Comprehensive donor form (Name, Roll No, Phone, Email, Dept, Year, Blood Group, Age, Time Slot, Emergency Contact).
   - Instant Unique Registration ID generation (`GRIET-BD-0001`, `GRIET-BD-0002`, etc.).
   - Duplicate registration prevention by College ID or Phone Number.
   - Beautiful print/save confirmation card.
5. **Check Registration**: Lookup registration status by ID or Phone Number.
6. **Official Do's & Don'ts**: Direct reflection of the official NSS GRIET poster instructions.
7. **Volunteer Application**: Module for students to join the organizing crew across 8 dedicated roles.
8. **Interactive FAQ Accordion**: Immediate clarity on eligibility, preparation, and requirements.
9. **Admin / Coordinator Dashboard**:
   - Secure hashed authentication (`admin` / `admin@griet2026`).
   - Real-time analytical breakdown by Blood Group, Department, and Time Slots.
   - Search, filter, status updates (Registered, Confirmed, Completed, Cancelled).
   - One-click CSV export of donor records.

---

## 🛠️ Technology Stack
- **Backend:** Python + Flask
- **Database:** SQLite (`database/event.db`)
- **Frontend:** HTML5, Modern CSS, Vanilla JavaScript
- **Security:** Werkzeug password hashing, parameterized SQL queries, Flask sessions.

---

## 📦 Project Structure
```text
Blood Donation 2026/
├── app.py                     # Main Flask routes and logic
├── database_helper.py         # SQLite schema initialization and seed data
├── requirements.txt           # Python dependencies
├── README.md                  # Setup & usage documentation
├── database/
│   └── event.db               # SQLite database
├── templates/
│   ├── base.html              # Sticky navbar, header, flash alerts, footer
│   ├── index.html             # Hero, live countdown, target stats, Do's & Don'ts
│   ├── register.html          # Full donor registration form
│   ├── success.html           # Print-friendly registration card
│   ├── check_registration.html# Status search lookup
│   ├── volunteer.html         # NSS volunteer registration
│   ├── faq.html               # Interactive FAQ accordion
│   ├── admin_login.html       # Coordinator login
│   ├── admin_dashboard.html   # Real-time analytics, filtering, status & export
│   └── error.html             # Custom 404 & 500 error handler
└── static/
    ├── css/
    │   └── style.css          # Responsive design system
    ├── js/
    │   └── script.js          # Countdown, accordion, form validations
    └── images/
        ├── griet-logo.svg     # GRIET vector logo
        ├── nss-logo.svg       # NSS vector logo
        └── hero-illustration.svg # Hero vector illustration
```

---

## ⚡ How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
- **Public Website:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Donor Registration:** [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register)
- **Check Status:** [http://127.0.0.1:5000/check-registration](http://127.0.0.1:5000/check-registration)
- **Admin Dashboard:** [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)

---

## 🔐 Admin Credentials (Default)
- **Username:** `admin`
- **Password:** `admin@griet2026`

*To update the admin password, run Python and update the hashed password in `database/event.db` using `werkzeug.security.generate_password_hash`.*
