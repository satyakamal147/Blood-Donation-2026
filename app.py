import re
import csv
import io
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, Response, abort
)
from werkzeug.security import check_password_hash
from database_helper import (
    get_db_connection, init_db, get_next_registration_id
)

app = Flask(__name__)
app.secret_key = 'griet_mega_blood_donation_2026_super_secret_key_nss'

# Initialize database and tables on startup
init_db()

# -------------------------------------------------------------
# FRONTEND PUBLIC ROUTES
# -------------------------------------------------------------

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM registrations')
    donor_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM volunteers')
    volunteer_count = cursor.fetchone()['count']
    conn.close()

    return render_template(
        'index.html',
        donor_count=donor_count,
        volunteer_count=volunteer_count
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        college_id = request.form.get('college_id', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        age_str = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        preferred_slot = request.form.get('preferred_slot', '').strip()
        emergency_name = request.form.get('emergency_name', '').strip()
        emergency_phone = request.form.get('emergency_phone', '').strip()
        address = request.form.get('address', '').strip()
        consent = request.form.get('consent')

        # 1. Validation: required fields
        if not (full_name and mobile and email and college_id and department and 
                year and blood_group and age_str and gender and preferred_slot and 
                emergency_name and emergency_phone and consent):
            flash('Please fill out all required fields and check the consent box.', 'error')
            return redirect(url_for('register'))

        # 2. Validation: Phone number format
        if not re.match(r'^[6-9]\d{9}$', mobile):
            flash('Please enter a valid 10-digit Indian mobile number.', 'error')
            return redirect(url_for('register'))

        # 3. Validation: Age limits
        try:
            age = int(age_str)
            if age < 17 or age > 75:
                flash('Please enter a valid donor age between 17 and 75.', 'error')
                return redirect(url_for('register'))
        except ValueError:
            flash('Invalid age value provided.', 'error')
            return redirect(url_for('register'))

        # 4. Check for duplicate registration by College ID or Mobile
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT registration_id FROM registrations WHERE college_id = ? OR mobile = ?',
            (college_id, mobile)
        )
        existing = cursor.fetchone()

        if existing:
            conn.close()
            flash(f'You are already registered with Registration ID: {existing["registration_id"]}.', 'warning')
            return redirect(url_for('check_registration', search=existing["registration_id"]))

        # 5. Insert new registration
        new_reg_id = get_next_registration_id()
        cursor.execute('''
        INSERT INTO registrations (
            registration_id, full_name, mobile, email, college_id, department,
            year, blood_group, age, gender, preferred_slot, emergency_name,
            emergency_phone, address, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Registered')
        ''', (
            new_reg_id, full_name, mobile, email, college_id, department,
            year, blood_group, age, gender, preferred_slot, emergency_name,
            emergency_phone, address
        ))
        conn.commit()
        conn.close()

        flash('Registration completed successfully! Please save your Registration ID.', 'success')
        return redirect(url_for('registration_success', reg_id=new_reg_id))

    return render_template('register.html')

@app.route('/registration-success/<reg_id>')
def registration_success(reg_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registrations WHERE registration_id = ?', (reg_id,))
    donor = cursor.fetchone()
    conn.close()

    if not donor:
        flash('Registration ID not found.', 'error')
        return redirect(url_for('check_registration'))

    return render_template('success.html', donor=donor)

@app.route('/check-registration', methods=['GET', 'POST'])
def check_registration():
    donor = None
    searched = False
    query = request.args.get('search', '').strip()

    if request.method == 'POST':
        query = request.form.get('search_query', '').strip()
        searched = True

    if query:
        searched = True
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM registrations 
        WHERE UPPER(registration_id) = UPPER(?) OR mobile = ? OR UPPER(college_id) = UPPER(?)
        ''', (query, query, query))
        donor = cursor.fetchone()
        conn.close()

    return render_template('check_registration.html', donor=donor, searched=searched, query=query)

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        college_id = request.form.get('college_id', '').strip()
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
        preferred_role = request.form.get('preferred_role', '').strip()

        if not (name and college_id and phone and department and year and preferred_role):
            flash('Please fill out all fields in the volunteer form.', 'error')
            return redirect(url_for('volunteer'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO volunteers (name, college_id, department, year, phone, preferred_role)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, college_id, department, year, phone, preferred_role))
        conn.commit()
        conn.close()

        flash('Thank you for volunteering! NSS coordinators will contact you soon.', 'success')
        return redirect(url_for('volunteer'))

    return render_template('volunteer.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


# -------------------------------------------------------------
# ADMIN & COORDINATOR ROUTES
# -------------------------------------------------------------

def is_admin_logged_in():
    return session.get('admin_logged_in') is True

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if is_admin_logged_in():
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE username = ?', (username,))
        admin = cursor.fetchone()
        conn.close()

        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            session['admin_name'] = admin['name']
            flash(f'Welcome back, {admin["name"]}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin_logged_in():
        flash('Please login to access the coordinator dashboard.', 'warning')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Filters
    search_query = request.args.get('search', '').strip()
    selected_bg = request.args.get('blood_group', '').strip()
    selected_dept = request.args.get('department', '').strip()

    # Base query for donors
    query = 'SELECT * FROM registrations WHERE 1=1'
    params = []

    if search_query:
        query += ' AND (full_name LIKE ? OR registration_id LIKE ? OR mobile LIKE ? OR college_id LIKE ?)'
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    if selected_bg:
        query += ' AND blood_group = ?'
        params.append(selected_bg)

    if selected_dept:
        query += ' AND department = ?'
        params.append(selected_dept)

    query += ' ORDER BY id DESC'
    cursor.execute(query, params)
    donors = cursor.fetchall()

    # Statistics
    cursor.execute('SELECT COUNT(*) as count FROM registrations')
    total_donors = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE status = 'Confirmed'")
    confirmed_donors = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) as count FROM volunteers')
    total_volunteers = cursor.fetchone()['count']

    # Aggregations
    cursor.execute('SELECT blood_group, COUNT(*) as count FROM registrations GROUP BY blood_group ORDER BY count DESC')
    blood_group_stats = cursor.fetchall()

    cursor.execute('SELECT department, COUNT(*) as count FROM registrations GROUP BY department ORDER BY count DESC')
    dept_stats = cursor.fetchall()

    cursor.execute('SELECT preferred_slot, COUNT(*) as count FROM registrations GROUP BY preferred_slot')
    slot_stats = cursor.fetchall()

    # Distinct departments for filter dropdown
    cursor.execute('SELECT DISTINCT department FROM registrations WHERE department IS NOT NULL AND department != ""')
    all_departments = cursor.fetchall()

    # Volunteers list
    cursor.execute('SELECT * FROM volunteers ORDER BY id DESC')
    volunteers = cursor.fetchall()

    conn.close()

    return render_template(
        'admin_dashboard.html',
        donors=donors,
        volunteers=volunteers,
        total_donors=total_donors,
        confirmed_donors=confirmed_donors,
        total_volunteers=total_volunteers,
        blood_group_stats=blood_group_stats,
        dept_stats=dept_stats,
        slot_stats=slot_stats,
        all_departments=all_departments,
        search_query=search_query,
        selected_bg=selected_bg,
        selected_dept=selected_dept
    )

@app.route('/admin/update-status/<int:donor_id>', methods=['POST'])
def admin_update_status(donor_id):
    if not is_admin_logged_in():
        abort(403)

    new_status = request.form.get('status')
    if new_status in ['Registered', 'Confirmed', 'Completed', 'Cancelled']:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE registrations SET status = ? WHERE id = ?', (new_status, donor_id))
        conn.commit()
        conn.close()
        flash(f'Status updated to "{new_status}".', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-donor/<int:donor_id>', methods=['POST'])
def admin_delete_donor(donor_id):
    if not is_admin_logged_in():
        abort(403)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registrations WHERE id = ?', (donor_id,))
    conn.commit()
    conn.close()
    flash('Registration record removed.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/export-csv')
def admin_export_csv():
    if not is_admin_logged_in():
        flash('Unauthorized. Please login.', 'danger')
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT registration_id, full_name, mobile, email, college_id, 
           department, year, blood_group, age, gender, preferred_slot, 
           emergency_name, emergency_phone, address, registration_date, status 
    FROM registrations 
    ORDER BY id ASC
    ''')
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        'Registration ID', 'Full Name', 'Mobile', 'Email', 'College/Employee ID',
        'Department', 'Year', 'Blood Group', 'Age', 'Gender', 'Preferred Slot',
        'Emergency Contact', 'Emergency Phone', 'Address', 'Registration Date', 'Status'
    ])

    for r in rows:
        writer.writerow([
            r['registration_id'], r['full_name'], r['mobile'], r['email'], r['college_id'],
            r['department'], r['year'], r['blood_group'], r['age'], r['gender'], r['preferred_slot'],
            r['emergency_name'], r['emergency_phone'], r['address'], r['registration_date'], r['status']
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=GRIET_Blood_Donation_Registrations_2026.csv"}
    )

# -------------------------------------------------------------
# ERROR HANDLERS
# -------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404, title="Page Not Found", message="The page you requested could not be located."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code=500, title="Server Error", message="An unexpected error occurred. Please try again shortly."), 500

if __name__ == '__main__':
    print("==================================================")
    print(" GRIET MEGA BLOOD DONATION 2026 - FLASK SERVER")
    print(" Organized by NSS GRIET")
    print(" Server running on: http://127.0.0.1:5000")
    print(" Admin login: http://127.0.0.1:5000/admin/login")
    print(" Credentials: admin / admin@griet2026")
    print("==================================================")
    app.run(debug=True, host='127.0.0.1', port=5000)
