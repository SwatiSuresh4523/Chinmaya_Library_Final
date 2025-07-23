from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta, date
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "chinmaya-secret"
DB_PATH = "library.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ----------------- Login Required Decorator ---------------- #
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            flash("🔐 Please login to continue", "warning")
            return redirect(url_for('login'))
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "Chinmaya" and password == "4523":
            session['user'] = username
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Replace with actual email lookup
        if email == 'admin@library.com':
            flash('Password reset link sent to your email 📩', 'info')
        else:
            flash('Email not found ⚠️', 'warning')
        return redirect(url_for('forgot_password'))
    return render_template('forgot.html')

import sqlite3
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('fullname')
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'Student')
        class_or_group = request.form.get('class_or_group', '')
        phone = request.form.get('phone', '')
        gender = request.form.get('gender', '')
        join_date = datetime.now().strftime('%Y-%m-%d')
        books_borrowed = 0
        last_activity = join_date

        conn = sqlite3.connect('library.db')
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (name, role, email, class_or_group, phone, gender, join_date, books_borrowed, last_activity, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, role, email, class_or_group, phone, gender, join_date, books_borrowed, last_activity, password))

        conn.commit()
        conn.close()

        flash(f'Registration successful for {name} 🎉', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/view_users')
def view_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('view_users.html', users=users)

@app.route('/user/<int:user_id>')
def view_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    return render_template('view_user.html', user=user)
@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch the user
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    if not user:
        return "User not found", 404

    if request.method == "POST":
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        class_or_group = request.form.get('class_or_group')
        gender = request.form.get('gender')

        cur.execute('''
            UPDATE users
            SET name=?, role=?, email=?, phone=?, class_or_group=?, gender=?
            WHERE id=?
        ''', (name, role, email, phone, class_or_group, gender, user_id))
        conn.commit()
        conn.close()
        return redirect("/users")  # or your users list page

    conn.close()
    return render_template("edit_user.html", user=user)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return redirect(url_for('view_users'))


# Export to Excel
import pdfkit
import io

@app.route('/export_users_pdf')
def export_users_pdf():
    conn = sqlite3.connect('library.db')
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}
            h1 {{
                text-align: center;
                color: #004080;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #999;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>📄 Chinmaya Library - User Report</h1>
        {df.to_html(index=False, border=0)}
        <p style="text-align:center; margin-top:30px;">Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</p>
    </body>
    </html>
    """

    # 👇 Path to your wkhtmltopdf
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf = pdfkit.from_string(html, False, configuration=config)

    return send_file(
        io.BytesIO(pdf),
        download_name="Chinmaya_Users_Report.pdf",
        as_attachment=True
    )


# ------------------ BOOK ENTRY SECTION ------------------
@app.route("/book_entry")
def book_entry():
    return render_template("book_entry.html")

@app.route("/add_book", methods=["POST"])
def add_book():
    ...
    accession = request.form.get("accession")
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    year = request.form.get("year")
    category = request.form.get("category")
    status = request.form.get("status", "Available")

    cover_file = request.files.get("cover_image")
    cover_filename = None

    if cover_file and cover_file.filename != "":
        cover_filename = secure_filename(cover_file.filename)
        cover_file.save(os.path.join("static/uploads", cover_filename))  # Save in static/uploads

    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            accession TEXT UNIQUE,
            isbn TEXT,
            title TEXT,
            author TEXT,
            publisher TEXT,
            year TEXT,
            category TEXT,
            status TEXT,
            cover_image TEXT
        )
    """)

    cur.execute("SELECT 1 FROM books WHERE accession = ?", (accession,))
    if cur.fetchone() is not None:
        conn.close()
        flash(f"❌ Book with accession number '{accession}' already exists.", "danger")
        return redirect(url_for("book_entry"))

    cur.execute("""
        INSERT INTO books (accession, isbn, title, author, publisher, year, category, status, cover_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (accession, isbn, title, author, publisher, year, category, status, cover_filename))

    conn.commit()
    conn.close()

    flash("✅ Book added successfully with cover image!", "success")
    return redirect(url_for("book_entry"))

# ------------------ HOME & STATIC ROUTES ------------------

@app.route("/books_dashboard")
def books_dashboard():
    return render_template("books_dashboard.html")

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 📊 Dashboard Statistics
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    today = datetime.now().strftime("%Y-%m-%d")
    cur.execute("SELECT COUNT(*) FROM issues WHERE issue_date = ?", (today,))
    today_issues = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issues WHERE due_date < ? AND return_date IS NULL", (today,))
    total_overdue = cur.fetchone()[0]

    stats = {
        "total_books": total_books,
        "total_students": total_students,
        "today_issues": today_issues,
        "total_overdue": total_overdue
    }

    # 🆕 Latest Books
    cur.execute("SELECT title, author, accession FROM books ORDER BY rowid DESC LIMIT 5")
    latest_books = cur.fetchall()

    # 👤 Latest Accounts
    cur.execute("SELECT name, class, account_no FROM students ORDER BY rowid DESC LIMIT 5")
    latest_accounts = cur.fetchall()

    # 📗 Recent Issues
    cur.execute("""
        SELECT b.title, b.author
        FROM issues i
        JOIN books b ON i.book_id = b.book_id
        ORDER BY i.issue_date DESC
        LIMIT 5
    """)
    latest_issues = cur.fetchall()

    # ⏳ Overdue Books
    cur.execute("""
        SELECT b.title as book_title, s.name, i.due_date
        FROM issues i
        JOIN books b ON i.book_id = b.book_id
        JOIN students s ON i.account_no = s.account_no
        WHERE i.due_date < ? AND i.return_date IS NULL
        ORDER BY i.due_date ASC
        LIMIT 5
    """, (today,))
    overdue_books = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        stats=stats,
        latest_books=latest_books,
        latest_accounts=latest_accounts,
        latest_issues=latest_issues,
        overdue_books=overdue_books
    )

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

import os

def is_valid_image(filepath):
    full_path = os.path.join('static', filepath)
    return os.path.exists(full_path) and os.path.getsize(full_path) > 1000  # >1KB = not corrupted

@app.route('/view_books')
def view_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books ORDER BY added_on DESC').fetchall()
    total_books = conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    available_books = conn.execute("SELECT COUNT(*) FROM books WHERE status='Available'").fetchone()[0]
    issued_books = conn.execute("SELECT COUNT(*) FROM books WHERE status='Issued'").fetchone()[0]

    categories = [row['category'] for row in conn.execute('SELECT DISTINCT category FROM books').fetchall()]
    years = [str(row['year']) for row in conn.execute('SELECT DISTINCT year FROM books').fetchall()]
    authors = [row['author'] for row in conn.execute('SELECT DISTINCT author FROM books').fetchall()]
    conn.close()

    return render_template('view_books.html', books=books, total_books=total_books,
                           available_books=available_books, issued_books=issued_books,
                           categories=categories, years=years, authors=authors)

from flask import request, jsonify
@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        accession = request.form["accession"]
        isbn = request.form["isbn"]
        category = request.form["category"]
        year = request.form["year"]

        cur.execute("""
            UPDATE books SET 
                title = ?, 
                author = ?, 
                publisher = ?, 
                accession = ?, 
                isbn = ?, 
                category = ?, 
                year = ?
            WHERE id = ?
        """, (title, author, publisher, accession, isbn, category, year, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for("view_books"))

    book = cur.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    if not book:
        return "Book not found", 404

    return render_template("edit_book.html", book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload_cover', methods=['POST'])
def upload_cover():
    if 'cover_image' not in request.files or 'book_id' not in request.form:
        return jsonify({"error": "No file or book ID provided"}), 400
    file = request.files['cover_image']
    book_id = request.form['book_id']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file securely, e.g., to static/uploads with book_id.jpg
    import os
    from werkzeug.utils import secure_filename
    upload_folder = 'static/uploads'
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(f"{book_id}.jpg")
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    # Update book record cover_url path
    cover_url = f"/static/uploads/{filename}"

    try:
        conn = get_db_connection()
        conn.execute('UPDATE books SET cover_url=? WHERE id=?', (cover_url, book_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# 📚 Book History Route


@app.route('/book_history/<int:book_id>')
def book_history(book_id):
    user_role = request.args.get("user_role", "")
    overdue_only = request.args.get("overdue_only") == "on"
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")

    conn = get_db_connection()
    cur = conn.cursor()

    # Get book details
    book = cur.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not book:
        conn.close()
        return "Book not found", 404

    # Build filter conditions
    filters = "WHERE ir.book_id = ?"
    params = [book_id]

    if user_role:
        filters += " AND ir.user_role = ?"
        params.append(user_role)
    if date_from:
        filters += " AND ir.issue_date >= ?"
        params.append(date_from)
    if date_to:
        filters += " AND ir.issue_date <= ?"
        params.append(date_to)
    if overdue_only:
        filters += " AND ir.return_date IS NULL AND julianday('now') - julianday(ir.issue_date) > ?"
        params.append(15)

    # Get issue-return history
    query = f"""
        SELECT ir.*, 
               COALESCE(s.name, t.name) AS user_name,
               ir.user_role AS role,
               julianday(COALESCE(ir.return_date, date('now'))) - julianday(ir.issue_date) AS days_issued,
               CASE 
                   WHEN ir.return_date IS NULL AND julianday('now') - julianday(ir.issue_date) > 15 THEN 1 
                   ELSE 0 
               END AS is_overdue
        FROM issue_return ir
        LEFT JOIN students s ON ir.user_id = s.id AND ir.user_role = 'Student'
        LEFT JOIN teachers t ON ir.user_id = t.id AND ir.user_role = 'Teacher'
        {filters}
        ORDER BY ir.issue_date DESC
    """
    history = cur.execute(query, params).fetchall()

    # Basic stats
    total_issued = cur.execute("SELECT COUNT(*) FROM issue_return WHERE book_id = ?", (book_id,)).fetchone()[0]
    currently_issued = cur.execute("SELECT COUNT(*) FROM issue_return WHERE book_id = ? AND return_date IS NULL", (book_id,)).fetchone()[0]
    overdue_count = cur.execute("""
        SELECT COUNT(*) FROM issue_return 
        WHERE book_id = ? AND return_date IS NULL AND julianday('now') - julianday(issue_date) > 15
    """, (book_id,)).fetchone()[0]

    conn.close()

    return render_template("book_history.html",
                           book=book,
                           history=history,
                           roles=['Student', 'Teacher'],
                           selected_role=user_role,
                           show_overdue_only=overdue_only,
                           date_from=date_from,
                           date_to=date_to,
                           total_issued=total_issued,
                           currently_issued=currently_issued,
                           overdue_count=overdue_count,
                           max_days=15)

from flask import send_file
import pandas as pd
import io

@app.route('/export_history_excel/<int:book_id>')
def export_history_excel(book_id):
    user_role = request.args.get('user_role')
    overdue_only = request.args.get('overdue_only') == 'on'
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
        SELECT 
            COALESCE(s.name, t.name, 'Unknown') AS user_name,
            CASE 
                WHEN s.id IS NOT NULL THEN 'Student' 
                WHEN t.id IS NOT NULL THEN 'Teacher' 
                ELSE 'Unknown' 
            END AS user_role,
            ir.issue_date,
            ir.return_date,
            ir.remarks
        FROM issue_return ir
        LEFT JOIN students s ON ir.user_id = s.id
        LEFT JOIN teachers t ON ir.user_id = t.id
        WHERE ir.book_id = ?
    """
    params = [book_id]

    if user_role:
        if user_role == 'Student':
            query += " AND s.id IS NOT NULL"
        elif user_role == 'Teacher':
            query += " AND t.id IS NOT NULL"

    if date_from:
        query += " AND ir.issue_date >= ?"
        params.append(date_from)

    if date_to:
        query += " AND ir.issue_date <= ?"
        params.append(date_to)

    cur.execute(query, params)
    rows = cur.fetchall()

    data = []
    for r in rows:
        days_issued = 0
        if r['issue_date']:
            from datetime import datetime
            issue_dt = datetime.strptime(r['issue_date'], "%Y-%m-%d")
            return_dt = datetime.strptime(r['return_date'], "%Y-%m-%d") if r['return_date'] else datetime.today()
            days_issued = (return_dt - issue_dt).days
        if overdue_only and days_issued <= 14:
            continue
        data.append({
            'User Name': r['user_name'],
            'Role': r['user_role'],
            'Issue Date': r['issue_date'],
            'Return Date': r['return_date'] if r['return_date'] else 'Not Returned',
            'Days Issued': days_issued,
            'Remarks': r['remarks']
        })

    df = pd.DataFrame(data)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, mimetype='text/csv', as_attachment=True,
                     download_name=f'book_{book_id}_history.csv')
# 📥 Bulk Upload Page
@app.route("/upload_books_page")
def upload_books_page():
    return render_template("upload_books.html")
   
# 📄 Download Excel Template
@app.route("/download_books_template")
def download_books_template():
    template_path = os.path.join("static", "template", "book_template.xlsx")
    return send_file(template_path, as_attachment=True)

# 📄 Export All Books to Excel
@app.route("/download_all_books_excel")
def download_all_books_excel():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM books", conn)
    path = os.path.join("static", "downloads", "all_books.xlsx")
    df.to_excel(path, index=False)
    conn.close()
    return send_file(path, as_attachment=True)

# 🖨️ Export All Books to PDF
@app.route("/download_all_books_pdf")
def download_all_books_pdf():
    from fpdf import FPDF

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT accession, title, author, publisher, category, year, status FROM books")
    books = cur.fetchall()
    conn.close()

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, "Chinmaya Smart Library - Book List", ln=True, align='C')

    col_width = 40
    headers = ["Accession", "Title", "Author", "Publisher", "Category", "Year", "Status"]
    for h in headers:
        pdf.cell(col_width, 10, h, 1)
    pdf.ln()

    for book in books:
        for field in book:
            pdf.cell(col_width, 10, str(field), 1)
        pdf.ln()

    pdf_path = os.path.join("static", "downloads", "books_list.pdf")
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True)

# ============================================================
# 📚 Chinmaya Library – Book Upload & Download Routes Section
# ============================================================
@app.route("/upload_excel")
def upload_excel():
    return render_template("upload_excel.html")

# ---------------------- DB Connection -----------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ 1. BULK UPLOAD for All Types ------------------

@app.route("/upload_excel/<upload_type>", methods=["POST"])
def upload_excel_by_type(upload_type):
    file = request.files['excel_file']
    
    if not file or file.filename == '':
        flash("Please select a file.")
        return redirect(url_for("upload_books_page"))

    if not file.filename.endswith((".xls", ".xlsx")):
        flash("Please upload a valid Excel file.")
        return redirect(url_for("upload_books_page"))

    filename = secure_filename(file.filename)
    filepath = os.path.join("static/uploads", filename)
    os.makedirs("static/uploads", exist_ok=True)
    file.save(filepath)

    import pandas as pd
    df = pd.read_excel(filepath)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        if upload_type == "books":
            for _, row in df.iterrows():
                cur.execute(
                    "INSERT INTO books (accession, title, author, publisher, category, year, publication) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (row['accession'], row['title'], row['author'], row['publisher'], row['category'], row['year'], row['publication'])
                )
        conn.commit()
        flash("✅ Books uploaded successfully.")
    except Exception as e:
        conn.rollback()
        flash(f"❌ Error uploading books: {e}")
    finally:
        conn.close()

    return redirect(url_for("upload_books_page"))


# ------------------ 2. DOWNLOAD TEMPLATES ------------------

@app.route("/download_template/<template_type>")
def download_template(template_type):
    wb = Workbook()
    ws = wb.active
    ws.title = "Template"

    if template_type == "books":
        ws.append(["Accession", "ISBN", "Title", "Author", "Publisher", "Category", "Year", "Publication"])
    elif template_type == "students":
        ws.append(["Name", "Class", "Roll No", "Phone"])
    elif template_type == "teachers":
        ws.append(["Name", "Subject", "Phone"])
    elif template_type == "categories":
        ws.append(["Category Name"])
    else:
        flash("❌ Invalid template type.", "danger")
        return redirect(url_for("upload_books_page"))

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, download_name=f"{template_type}_template.xlsx", as_attachment=True)

# ------------------ 3. EXPORT EXISTING DATA ------------------

@app.route("/export_data/excel")
def export_data_excel():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT accession, isbn, title, author, publisher, category, year, publication FROM books")
    books = cur.fetchall()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Books"
    ws.append(["Accession", "ISBN", "Title", "Author", "Publisher", "Category", "Year", "Publication"])
    for book in books:
        ws.append(book)

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(output, download_name="books_export.xlsx", as_attachment=True)

@app.route("/export_data/pdf")
def export_data_pdf():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT accession, title, author, category FROM books ORDER BY accession ASC")
    books = cur.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="📚 Chinmaya Library - Book List", ln=True, align="C")
    pdf.ln(10)

    for book in books:
        line = f"Acc: {book[0]} | {book[1]} by {book[2]} [{book[3]}]"
        pdf.multi_cell(0, 10, txt=line)

    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return send_file(output, download_name="books_export.pdf", as_attachment=True)

# ------------------ 4. OPEN BULK UPLOAD PAGE ------------------

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 📊 Stats
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE return_date IS NULL")
    total_issued = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE return_date IS NOT NULL")
    total_returned = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE return_date IS NULL AND due_date < date('now')")
    not_returned = cur.fetchone()[0]

    cur.execute("SELECT SUM(fine) FROM issue_return")
    total_fine = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE DATE(issue_date)=DATE('now')")
    today_issued = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE strftime('%m', issue_date)=strftime('%m', 'now')")
    month_issued = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE strftime('%m', issue_date)=strftime('%m', 'now', '-1 month')")
    last_month_issued = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT user_id) FROM issue_return WHERE strftime('%m', issue_date)=strftime('%m', 'now', '-1 month')")
    last_month_students = cur.fetchone()[0]

    cur.execute("SELECT user_name, COUNT(*) as count FROM issue_return GROUP BY user_name ORDER BY count DESC LIMIT 5")
    top_students = cur.fetchall()

    cur.execute("""
        SELECT books.title, COUNT(*) as count FROM issue_return
        JOIN books ON books.book_id = issue_return.book_id
        GROUP BY books.title ORDER BY count DESC LIMIT 5
    """)
    top_books = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM books WHERE book_id NOT IN (SELECT book_id FROM issue_return)")
    never_issued_count = cur.fetchone()[0]

    db_size = f"{round(os.path.getsize(DB_PATH)/1024, 2)} KB"

    cur.execute("SELECT COUNT(*) FROM issue_return WHERE DATE(issue_date)=DATE('now')")
    qr_logs_today = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT user_id) FROM issue_return WHERE DATE(issue_date)=DATE('now')")
    active_users = cur.fetchone()[0]

    cur.execute("SELECT user_name, book_id, issue_date, due_date, return_date, fine FROM issue_return ORDER BY issue_date DESC LIMIT 50")
    rows = cur.fetchall()

    report_data = [
        {
            "user_name": row["user_name"],
            "book_title": f"Book ID {row['book_id']}",
            "issue_date": row["issue_date"],
            "due_date": row["due_date"],
            "return_date": row["return_date"],
            "fine": row["fine"]
        } for row in rows
    ]

    recent_activity = [f"{row['user_name']} issued {row['book_title']} on {row['issue_date']}" for row in report_data[:5]]
    announcements = ["New 📚 books added this week!", "⏳ Return overdue books before fine!"]

    last_login_user = "Chinmaya"
    last_login_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    conn.close()

    return render_template("dashboard.html",
        total_books=total_books,
        total_issued=total_issued,
        total_returned=total_returned,
        not_returned=not_returned,
        overdue=not_returned,
        total_fine=total_fine,
        today_issued=today_issued,
        month_issued=month_issued,
        total_students=total_students,
        total_teachers=total_teachers,
        last_month_issued=last_month_issued,
        last_month_students=last_month_students,
        top_students=top_students,
        top_books=top_books,
        never_issued_count=never_issued_count,
        db_size=db_size,
        qr_logs_today=qr_logs_today,
        active_users=active_users,
        report_data=report_data,
        recent_activity=recent_activity,
        announcements=announcements,
        last_login_user=last_login_user,
        last_login_time=last_login_time
    )

from flask import render_template
import sqlite3
@app.route("/reports")
def reports():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Get issue-return data with user name and book title
        cur.execute("""
            SELECT 
                ir.user_id,
                COALESCE(s.name, t.name, 'Unknown') AS user_name,
                b.title AS book_title,
                ir.book_id,
                ir.issue_date,
                ir.return_date,
                ir.fine,
                CASE 
                    WHEN ir.return_date IS NULL OR ir.return_date = '' THEN 'Issued'
                    ELSE 'Returned'
                END AS status
            FROM issue_return ir
            LEFT JOIN students s ON ir.user_id = s.id
            LEFT JOIN teachers t ON ir.user_id = t.id
            LEFT JOIN books b ON ir.book_id = b.id
            ORDER BY ir.issue_date DESC
        """)
        report_data = cur.fetchall()

        # Class-wise issued count (for Chart.js)
        cur.execute("""
            SELECT s.class AS class, COUNT(*) as count
            FROM issue_return ir
            LEFT JOIN students s ON ir.user_id = s.id
            WHERE s.class IS NOT NULL
            GROUP BY s.class
        """)
        class_rows = cur.fetchall()
        class_labels = [row["class"] for row in class_rows]
        class_data = [row["count"] for row in class_rows]

    return render_template("reports.html", report_data=report_data, class_labels=class_labels, class_data=class_data)

@app.route("/download_report_excel")
def download_report_excel():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                ir.user_id,
                COALESCE(s.name, t.name, 'Unknown') AS user_name,
                b.title AS book_title,
                ir.book_id,
                ir.issue_date,
                ir.return_date,
                ir.fine,
                CASE 
                    WHEN ir.return_date IS NULL OR ir.return_date = '' THEN 'Issued'
                    ELSE 'Returned'
                END AS status
            FROM issue_return ir
            LEFT JOIN students s ON ir.user_id = s.id
            LEFT JOIN teachers t ON ir.user_id = t.id
            LEFT JOIN books b ON ir.book_id = b.id
            ORDER BY ir.issue_date DESC
        """)
        rows = cur.fetchall()

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Library Report")

    headers = ["Account No", "Name", "Book Title", "Book ID", "Issue Date", "Return Date", "Status", "Fine"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    for row_num, row in enumerate(rows, start=1):
        worksheet.write(row_num, 0, row["user_id"])
        worksheet.write(row_num, 1, row["user_name"])
        worksheet.write(row_num, 2, row["book_title"])
        worksheet.write(row_num, 3, row["book_id"])
        worksheet.write(row_num, 4, row["issue_date"])
        worksheet.write(row_num, 5, row["return_date"] or "Not Returned")
        worksheet.write(row_num, 6, row["status"])
        worksheet.write(row_num, 7, row["fine"] or 0)

    workbook.close()
    output.seek(0)

    return send_file(output,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True,
                     download_name="library_report.xlsx")

@app.route("/gallery")
def gallery():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT filename, category FROM gallery_images")
    images = cur.fetchall()
    return render_template("gallery.html", images=images)
import os
from flask import request, redirect, flash, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_gallery', methods=['GET', 'POST'])
def upload_gallery():
    if request.method == 'POST':
        caption = request.form['caption']
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Optionally: save caption info to DB here
            flash('Image uploaded successfully!')
            return redirect(url_for('gallery'))
        else:
            flash('Invalid file format.')
            return redirect(request.url)
    return render_template('upload_gallery.html')

@app.route("/promote")
def promote():
    return render_template("promote.html")

@app.route("/daily_report")
def daily_report():
    return render_template("daily_report.html")

@app.route("/ai_assist")
def ai_assist():
    return render_template("ai_assist.html")

@app.route("/ai_query", methods=["POST"])
def ai_query():
    query = request.form.get("query")
    response = "This is a sample response for: " + query  # Replace with actual AI API call
    return render_template("ai_assist.html", response=response)

@app.route("/get_book_details", methods=["POST"])
def get_book_details():
    book_id = request.form.get("book_id")
    # Add logic to fetch book from DB
    response = f"Details for Book ID: {book_id} — Title: ABC, Author: XYZ"
    return render_template("ai_assist.html", response=response)

@app.route("/suggest_subject_books", methods=["POST"])
def suggest_subject_books():
    subject = request.form.get("subject")
    # Add logic to fetch suggestions
    response = f"Recommended books for subject '{subject}': Book1, Book2, Book3"
    return render_template("ai_assist.html", response=response)

@app.route("/announcements")
def announcements():
    return render_template("announcements.html")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    isbn = request.args.get('isbn', '').strip()
    accession_no = request.args.get('accession_no', '').strip()
    year = request.args.get('year', '')
    status = request.args.get('status', '')

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    sql = "SELECT * FROM books WHERE 1=1"
    params = []

    if query:
        sql += " AND (title LIKE ? OR author LIKE ? OR category LIKE ?)"
        like_query = f"%{query}%"
        params.extend([like_query, like_query, like_query])
    if isbn:
        sql += " AND isbn LIKE ?"
        params.append(f"%{isbn}%")
    if accession_no:
        sql += " AND accession_no LIKE ?"
        params.append(f"%{accession_no}%")
    if year:
        sql += " AND year = ?"
        params.append(year)
    if status:
        sql += " AND status = ?"
        params.append(status)

    cur.execute(sql, params)
    results = cur.fetchall()
    conn.close()

    return render_template("search.html", results=results, query=query)
@app.route("/book/<int:book_id>")
def book_details(book_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cur.fetchone()
    conn.close()

    if book:
        return render_template("book_details.html", book=book)
    else:
        return "Book not found", 404
def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.form
        conn.execute('''
            INSERT INTO wishlist (name, user_id, class_group, title, author, publisher, date, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['user_id'], data['class_group'],
            data['title'], data['author'], data['publisher'],
            data['date'], data['reason']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('wishlist'))

    wishes = conn.execute('SELECT * FROM wishlist ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('wishlist.html', wishes=wishes)

@app.route('/wishlist/update/<int:wish_id>/<action>')
def update_wishlist_status(wish_id, action):
    status = 'Approved' if action == 'approve' else 'Rejected'
    conn = get_db_connection()
    conn.execute('UPDATE wishlist SET status = ? WHERE id = ?', (status, wish_id))
    conn.commit()
    conn.close()
    return redirect(url_for('wishlist'))

@app.route('/wishlist_report')
def wishlist_report():
    conn = get_db_connection()
    wishes = conn.execute('SELECT * FROM wishlist').fetchall()
    conn.close()
    return render_template('wishlist_report.html', wishes=wishes)


@app.route("/sync_excel")
def sync_excel():
    return render_template("sync_excel.html")

@app.route("/history")
def history():
    return render_template("history.html")

# ------------------ DATABASE SETUP ------------------

def create_students_table():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                account_no TEXT PRIMARY KEY,
                name TEXT,
                roll_no TEXT,
                class TEXT,
                contact TEXT,
                photo_url TEXT,
                admission_date TEXT,
                active INTEGER DEFAULT 1,
                books_issued INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        conn.commit()

# ------------------ ACCOUNT DASHBOARD ------------------

@app.route("/accounts")
def accounts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM teachers")
        total_teachers = cur.fetchone()[0]

        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        cur.execute("SELECT COUNT(*) FROM students WHERE created_at >= ?", (one_week_ago,))
        recent_students = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM teachers WHERE created_at >= ?", (one_week_ago,))
        recent_teachers = cur.fetchone()[0]
        recent_accounts = recent_students + recent_teachers

        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute("SELECT COUNT(*) FROM issues WHERE return_date IS NULL AND due_date < ?", (today,))
        overdue_count = cur.fetchone()[0]

        cur.execute("SELECT SUM(fine_collected) FROM returns WHERE return_date = ?", (today,))
        fine_today = cur.fetchone()[0] or 0

        upcoming_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        cur.execute("SELECT COUNT(*) FROM issues WHERE return_date IS NULL AND due_date <= ?", (upcoming_date,))
        upcoming_returns = cur.fetchone()[0]

        cur.execute("SELECT * FROM students")
        students = cur.fetchall()

        cur.execute("SELECT * FROM teachers")
        teachers = cur.fetchall()

    except Exception as e:
        print("❌ Database Error:", e)
        total_students = total_teachers = recent_accounts = overdue_count = 0
        fine_today = upcoming_returns = 0
        students = []
        teachers = []

    conn.close()

    return render_template("accounts.html",
                           total_students=total_students,
                           total_teachers=total_teachers,
                           recent_accounts=recent_accounts,
                           overdue_count=overdue_count,
                           fine_today=fine_today,
                           upcoming_returns=upcoming_returns,
                           students=students,
                           teachers=teachers)

# ------------------ STUDENT ROUTES ------------------

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    create_students_table()

    if request.method == "POST":
        account_no = request.form.get("account_no")
        name = request.form.get("name")
        roll_no = request.form.get("roll_no")
        student_class = request.form.get("class")
        contact = request.form.get("contact")
        admission_date = request.form.get("admission_date")

        photo = request.files.get("photo")
        photo_filename = ""
        if photo and photo.filename:
            photo_filename = f"{account_no}_{photo.filename}"
            photo_path = os.path.join("static/uploads/", photo_filename)
            photo.save(photo_path)
            photo_url = "/" + photo_path.replace("\\", "/")
        else:
            photo_url = "/static/img/default_user.png"

        created_at = datetime.now().strftime("%Y-%m-%d")

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO students (
                    account_no, name, roll_no, class, contact,
                    photo_url, admission_date, active,
                    books_issued, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, 0, ?)
            """, (
                account_no, name, roll_no, student_class,
                contact, photo_url, admission_date, created_at
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print("❌ Error saving student:", e)

        return redirect(url_for("accounts"))

    return render_template("add_student.html")
@app.route("/toggle_student_status/<account_no>")
def toggle_student_status(account_no):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Get current status
    cur.execute("SELECT active FROM students WHERE account_no = ?", (account_no,))
    current_status = cur.fetchone()

    if current_status:
        new_status = 0 if current_status[0] == 1 else 1
        cur.execute("UPDATE students SET active = ? WHERE account_no = ?", (new_status, account_no))
        conn.commit()

    conn.close()
    return redirect(url_for("accounts"))


from werkzeug.utils import secure_filename
import pandas as pd

from flask import request, redirect, flash
import pandas as pd

@app.route("/upload_students", methods=["GET", "POST"])
def upload_students():
    if request.method == "POST":
        file = request.files["excel_file"]

        if not file.filename.endswith((".xls", ".xlsx")):
            return "<h4>❌ Invalid file format. Upload only Excel file.</h4>"

        try:
            df = pd.read_excel(file)

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            for _, row in df.iterrows():
                cur.execute("""
                    INSERT INTO students (account_no, name, class, section, contact, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row["account_no"],
                    row["name"],
                    row["class"],
                    row.get("section", ""),
                    row.get("contact", ""),
                    row.get("created_at", datetime.now().strftime("%Y-%m-%d"))
                ))

            conn.commit()
            conn.close()

            return "<h4>✅ Students uploaded successfully!</h4>"

        except Exception as e:
            return f"<h4>❌ Upload failed: {str(e)}</h4>"

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📤 Upload Students – Chinmaya Library</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="container mt-5">
        <h3>📤 Upload Students Excel</h3>
        <form method="POST" enctype="multipart/form-data" class="mt-4">
            <input type="file" name="excel_file" accept=".xlsx,.xls" required class="form-control mb-3">
            <button type="submit" class="btn btn-success">Upload</button>
            <a href="/accounts" class="btn btn-secondary">Back</a>
        </form>
        <p class="mt-3">📥 <a href="/download_students_template">Download Template</a> before uploading</p>
    </body>
    </html>
    '''
@app.route("/download_students_template")
def download_students_template():
    df = pd.DataFrame([{
        "account_no": "6001",
        "name": "Arjun Sharma",
        "class": "6",
        "section": "A",
        "contact": "9876543210",
        "created_at": "2025-07-01"
    }])
    df.to_excel("students_template.xlsx", index=False)
    return send_file("students_template.xlsx", as_attachment=True)


@app.route("/download_students_excel")
def download_students_excel():
    try:
        import pandas as pd

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT account_no, name, class, section, contact, created_at FROM students", conn)
        conn.close()

        filename = "students.xlsx"
        filepath = os.path.join("static", filename)
        df.to_excel(filepath, index=False)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return f"❌ Excel export failed: {e}"


from xhtml2pdf import pisa
from io import BytesIO
from flask import make_response

@app.route("/download_students_pdf")
def download_students_pdf():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT account_no, name, class, section, contact, created_at FROM students")
        students = cur.fetchall()
        conn.close()

        # HTML for PDF
        html = render_template("students_pdf_template.html", students=students)

        # Convert HTML to PDF
        pdf = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf)
        if pisa_status.err:
            return "❌ Failed to create PDF"

        response = make_response(pdf.getvalue())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=students.pdf"
        return response

    except Exception as e:
        return f"❌ PDF export failed: {e}"


@app.route("/promote_students", methods=["GET", "POST"])
def promote_students():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        from_class = request.form["from_class"]
        to_class = request.form["to_class"]
        section = request.form.get("section")

        try:
            if section:
                cur.execute("""
                    UPDATE students
                    SET class = ?
                    WHERE class = ? AND section = ?
                """, (to_class, from_class, section))
            else:
                cur.execute("""
                    UPDATE students
                    SET class = ?
                    WHERE class = ?
                """, (to_class, from_class))

            conn.commit()
            msg = f"✅ Students promoted from {from_class} to {to_class}."
        except Exception as e:
            msg = f"❌ Error: {e}"
        finally:
            conn.close()
            return render_template("promote_students.html", msg=msg)

    # For GET request
    cur.execute("SELECT DISTINCT class FROM students ORDER BY class")
    classes = [r["class"] for r in cur.fetchall()]

    cur.execute("SELECT DISTINCT section FROM students ORDER BY section")
    sections = [r["section"] for r in cur.fetchall()]
    conn.close()

    return render_template("promote_students.html", classes=classes, sections=sections)


@app.route("/edit_student/<account_no>", methods=["GET", "POST"])
def edit_student(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get student info
    cur.execute("SELECT * FROM students WHERE account_no = ?", (account_no,))
    student = cur.fetchone()

    if not student:
        conn.close()
        return f"<h4>❌ Student {account_no} not found.</h4>"

    # Classes and sections for dropdown
    classes = ['6', '7', '8', '9', '10', 'Plus 1', 'Plus 2']
    sections = ['A', 'B', 'C']

    if request.method == "POST":
        name = request.form["name"]
        student_class = request.form["class"]
        section = request.form["section"]
        contact = request.form["contact"]

        cur.execute("""
            UPDATE students SET name = ?, class = ?, section = ?, contact = ?
            WHERE account_no = ?
        """, (name, student_class, section, contact, account_no))
        conn.commit()
        conn.close()

        return redirect("/accounts")

    conn.close()
    return render_template("edit_student.html",
                           student=student,
                           classes=classes,
                           sections=sections)


@app.route("/delete_student/<account_no>", methods=["GET", "POST"])
def delete_student(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get student info
    cur.execute("SELECT * FROM students WHERE account_no = ?", (account_no,))
    student = cur.fetchone()

    if not student:
        conn.close()
        return f"<h4>❌ Student with Account No {account_no} not found.</h4>"

    if request.method == "POST":
        cur.execute("DELETE FROM students WHERE account_no = ?", (account_no,))
        conn.commit()
        conn.close()
        return redirect("/accounts")

    conn.close()
    return render_template("delete_student.html", student=student)


@app.route("/student_history/<account_no>")
def student_history(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get student info
    cur.execute("SELECT * FROM students WHERE account_no = ?", (account_no,))
    student = cur.fetchone()

    if not student:
        conn.close()
        return f"<h4>❌ Student {account_no} not found.</h4>"

    # Get issue and return history
    cur.execute("""
        SELECT i.book_id, b.title, i.issue_date, i.due_date, r.return_date, r.fine_collected
        FROM issues i
        LEFT JOIN books b ON i.book_id = b.book_id
        LEFT JOIN returns r ON i.issue_id = r.issue_id
        WHERE i.account_no = ?
        ORDER BY i.issue_date DESC
    """, (account_no,))
    history = cur.fetchall()

    conn.close()
    return render_template("student_history.html", student=student, history=history)


@app.route("/renew_student/<account_no>", methods=["GET", "POST"])
def renew_student(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        new_admission_date = request.form.get("admission_date")
        # Update admission_date and activate the student
        cur.execute("""
            UPDATE students
            SET admission_date = ?, active = 1
            WHERE account_no = ?
        """, (new_admission_date, account_no))
        conn.commit()
        conn.close()
        return redirect(url_for("accounts"))

    # GET method - display form
    cur.execute("SELECT * FROM students WHERE account_no = ?", (account_no,))
    student = cur.fetchone()
    conn.close()

    if not student:
        return "<h3>❌ Student not found.</h3>"

    return render_template("renew_student.html", student=student)


@app.route("/exchange_book/<account_no>", methods=["GET", "POST"])
def exchange_book(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get student info
    cur.execute("SELECT * FROM students WHERE account_no = ?", (account_no,))
    student = cur.fetchone()

    if not student:
        conn.close()
        return "<h3>❌ Student not found.</h3>"

    # Get books issued to student
    cur.execute("""
        SELECT i.book_id, b.title
        FROM issues i
        JOIN books b ON i.book_id = b.book_id
        WHERE i.account_no = ? AND i.return_date IS NULL
    """, (account_no,))
    issued_books = cur.fetchall()

    if request.method == "POST":
        old_book_id = request.form.get("old_book_id")
        new_book_id = request.form.get("new_book_id")
        today = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        # 1. Mark old book as returned
        cur.execute("""
            UPDATE issues SET return_date = ?, fine_collected = 0
            WHERE account_no = ? AND book_id = ? AND return_date IS NULL
        """, (today, account_no, old_book_id))

        cur.execute("INSERT INTO returns (account_no, book_id, return_date, fine_collected) VALUES (?, ?, ?, ?)",
                    (account_no, old_book_id, today, 0))

        # 2. Issue new book
        cur.execute("INSERT INTO issues (account_no, book_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
                    (account_no, new_book_id, today, due_date))

        # 3. Update student book count
        cur.execute("UPDATE students SET books_issued = books_issued WHERE account_no = ?", (account_no,))

        conn.commit()
        conn.close()

        return redirect(url_for("accounts"))

    # Get available books to issue
    cur.execute("SELECT book_id, title FROM books WHERE available = 1")
    available_books = cur.fetchall()

    conn.close()
    return render_template("exchange_book.html", student=student, issued_books=issued_books, available_books=available_books)
# Config upload folder
UPLOAD_FOLDER = "static/uploads/photos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# --- DATABASE SETUP ---
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create users table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'teacher')),
            class TEXT,
            section TEXT,
            password_hash TEXT NOT NULL,
            photo_filename TEXT,
            active INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()
    return "Database initialized successfully"

    # Create users table if not exists
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    app.run(debug=True)

# Serve user photos
@app.route('/uploads/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ------------------ TEACHER ROUTES ------------------

@app.route("/add_teacher", methods=["GET", "POST"])
def add_teacher():
    # Auto-create teacher table if it doesn't exist
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                account_no TEXT PRIMARY KEY,
                name TEXT,
                subject TEXT,
                contact TEXT,
                photo_url TEXT,
                joining_date TEXT,
                active INTEGER DEFAULT 1,
                books_issued INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        conn.commit()

    if request.method == "POST":
        account_no = request.form.get("account_no")
        name = request.form.get("name")
        subject = request.form.get("subject")
        contact = request.form.get("contact")
        joining_date = request.form.get("joining_date")

        photo = request.files.get("photo")
        photo_filename = ""
        if photo and photo.filename:
            photo_filename = f"{account_no}_{photo.filename}"
            photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
            photo.save(photo_path)
            photo_url = "/" + photo_path.replace("\\", "/")
        else:
            photo_url = "/static/img/default_user.png"

        created_at = datetime.now().strftime("%Y-%m-%d")

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO teachers (
                    account_no, name, subject, contact,
                    photo_url, joining_date, active,
                    books_issued, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 1, 0, ?)
            """, (
                account_no, name, subject, contact,
                photo_url, joining_date, created_at
            ))
            conn.commit()
        except Exception as e:
            print("❌ Error saving teacher:", e)

        return redirect(url_for("accounts"))

    return render_template("add_teacher.html")


import pandas as pd

@app.route("/upload_teachers", methods=["GET", "POST"])
def upload_teachers():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".xlsx"):
            df = pd.read_excel(file)

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                for index, row in df.iterrows():
                    try:
                        cur.execute("""
                            INSERT OR IGNORE INTO teachers
                            (account_no, name, subject, contact, photo_url, joining_date, active, books_issued, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, 1, 0, ?)
                        """, (
                            row['account_no'],
                            row['name'],
                            row['subject'],
                            row.get('contact', ''),
                            "/static/img/default_user.png",
                            row.get('joining_date', ''),
                            datetime.now().strftime("%Y-%m-%d")
                        ))
                    except Exception as e:
                        print("Upload Error:", e)
                conn.commit()

            return redirect(url_for("accounts"))

    return render_template("upload_teachers.html")


@app.route("/download_teachers_excel")
def download_teachers_excel():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT account_no, name, subject, contact, joining_date FROM teachers", conn)
    conn.close()

    filename = "teachers_export.xlsx"
    df.to_excel(filename, index=False)

    return send_file(filename, as_attachment=True)

from fpdf import FPDF

@app.route("/download_teachers_pdf")
def download_teachers_pdf():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT account_no, name, subject, contact, joining_date FROM teachers", conn
        )
        conn.close()

        html = render_template("teachers_pdf.html", table=df.to_html(index=False, escape=False))

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding='utf-8')

        response = make_response(result.getvalue())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=teachers.pdf"
        return response

    except Exception as e:
        return f"<h3>Error generating PDF: {e}</h3>"

@app.route("/edit_teacher/<account_no>", methods=["GET", "POST"])
def edit_teacher(account_no):
    if request.method == "POST":
        name = request.form.get("name")
        subject = request.form.get("subject")
        contact = request.form.get("contact")
        joining_date = request.form.get("joining_date")

        # Check if new photo uploaded
        photo = request.files.get("photo")
        if photo and photo.filename:
            photo_filename = f"{account_no}_{photo.filename}"
            photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
            photo.save(photo_path)
            photo_url = "/" + photo_path.replace("\\", "/")
        else:
            # Keep existing photo
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("SELECT photo_url FROM teachers WHERE account_no = ?", (account_no,))
                photo_url = cur.fetchone()[0]

        # Update the teacher info
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE teachers SET name=?, subject=?, contact=?, photo_url=?, joining_date=?
                WHERE account_no=?
            """, (name, subject, contact, photo_url, joining_date, account_no))
            conn.commit()

        return redirect(url_for("accounts"))

    else:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM teachers WHERE account_no = ?", (account_no,))
            teacher = cur.fetchone()

        return render_template("edit_teacher.html", teacher=teacher)


@app.route("/delete_teacher/<account_no>")
def delete_teacher(account_no):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Optional: delete related data if needed (like books issued)
        cur.execute("DELETE FROM teachers WHERE account_no = ?", (account_no,))
        conn.commit()
        conn.close()
        print(f"✅ Teacher {account_no} deleted successfully.")
        return redirect(url_for("accounts"))

    except Exception as e:
        print(f"❌ Error deleting teacher: {e}")
        return f"<h3>❌ Error deleting teacher {account_no}</h3>"


@app.route("/teacher_history/<account_no>")
def teacher_history(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # Get teacher info
        cur.execute("SELECT * FROM teachers WHERE account_no = ?", (account_no,))
        teacher = cur.fetchone()

        # Get issue/return history
        cur.execute("""
            SELECT b.title, i.issue_date, i.due_date, r.return_date, r.fine_collected
            FROM issues i
            LEFT JOIN books b ON i.book_id = b.book_id
            LEFT JOIN returns r ON i.issue_id = r.issue_id
            WHERE i.account_no = ? AND i.user_type = 'teacher'
            ORDER BY i.issue_date DESC
        """, (account_no,))
        history = cur.fetchall()

    except Exception as e:
        print("❌ Error loading teacher history:", e)
        teacher = None
        history = []

    conn.close()
    return render_template("teacher_history.html", teacher=teacher, history=history)

@app.route("/renew_teacher/<account_no>")
def renew_teacher(account_no):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Extend due date by 7 days for all active issues (not returned)
        cur.execute("""
            UPDATE issues
            SET due_date = DATE(due_date, '+7 days')
            WHERE account_no = ? AND user_type = 'teacher' AND return_date IS NULL
        """, (account_no,))
        conn.commit()
        conn.close()

        print(f"✅ Renewed books for teacher {account_no}")
        return redirect(url_for("accounts"))

    except Exception as e:
        print(f"❌ Error renewing books: {e}")
        return f"<h3>❌ Error renewing books for {account_no}</h3>"


@app.route("/exchange_teacher_book/<account_no>", methods=["GET", "POST"])
def exchange_teacher_book(account_no):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        try:
            old_issue_id = request.form["issue_id"]
            new_book_id = request.form["new_book_id"]
            today = datetime.now().strftime("%Y-%m-%d")
            due = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")

            # 1. Return the old book
            cur.execute("""
                INSERT INTO returns (issue_id, return_date, fine_collected)
                VALUES (?, ?, ?)
            """, (old_issue_id, today, 0))

            # 2. Issue the new book
            cur.execute("""
                INSERT INTO issues (book_id, account_no, user_type, issue_date, due_date)
                VALUES (?, ?, 'teacher', ?, ?)
            """, (new_book_id, account_no, today, due))

            conn.commit()
            conn.close()
            return redirect(url_for("accounts"))
        except Exception as e:
            conn.close()
            return f"<h3>❌ Exchange Error: {e}</h3>"

    # GET method — show the form
    cur.execute("SELECT * FROM teachers WHERE account_no = ?", (account_no,))
    teacher = cur.fetchone()

    # Find currently issued book(s)
    cur.execute("""
        SELECT issues.issue_id, books.title
        FROM issues
        JOIN books ON issues.book_id = books.book_id
        WHERE issues.account_no = ? AND issues.user_type = 'teacher' AND issues.return_date IS NULL
    """, (account_no,))
    current_issues = cur.fetchall()

    # Available books to choose from
    cur.execute("SELECT * FROM books WHERE status = 'available'")
    available_books = cur.fetchall()

    conn.close()
    return render_template("exchange_teacher.html", teacher=teacher,
                           current_issues=current_issues,
                           available_books=available_books)

# ✅ Home route to render Issue & Return page

@app.route("/issue")
def issue_return():
    stats = {
        'issued_today': 0,
        'returned_today': 0,
        'issued_month': 0,
        'returned_month': 0,
        'not_returned': 0,
        'overdue': 0,
        'total_fine': 0
    }
    history = []
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    today = date.today()
    first_day = today.replace(day=1)
    try:
        cur.execute("SELECT COUNT(*) FROM issued_books WHERE issue_date = ?", (today,))
        stats['issued_today'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE return_date = ?", (today,))
        stats['returned_today'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE issue_date >= ?", (first_day,))
        stats['issued_month'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE return_date >= ?", (first_day,))
        stats['returned_month'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL")
        stats['not_returned'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL AND due_date < ?", (today,))
        stats['overdue'] = cur.fetchone()[0]

        cur.execute("SELECT SUM(fine) FROM issued_books")
        total = cur.fetchone()[0]
        stats['total_fine'] = total if total else 0

        cur.execute("SELECT * FROM issued_books ORDER BY id DESC LIMIT 100")
        rows = cur.fetchall()
        for row in rows:
            book = get_book_data(row[1])
            history.append({
                'book_title': book.get('title', ''),
                'book_author': book.get('author', ''),
                'book_id': row[1],
                'user_name': row[2],
                'user_id': row[3],
                'issue_date': row[4],
                'due_date': row[5],
                'return_date': row[6],
                'fine': row[7]
            })
    except Exception as e:
        flash("Database Error: " + str(e))
    conn.close()
    return render_template("issue_return.html", stats=stats, history=history)

# ✅ Helper to return book info

def issue_return():
    stats = {
        'issued_today': 0,
        'returned_today': 0,
        'overdue': 0,
        'available': "—"
    }
    history = []
    today = date.today()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM issued_books WHERE issue_date = ?", (today,))
        stats['issued_today'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE return_date = ?", (today,))
        stats['returned_today'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL AND due_date < ?", (today,))
        stats['overdue'] = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM books")
        stats['available'] = cur.fetchone()[0]

        cur.execute("SELECT * FROM issued_books ORDER BY id DESC LIMIT 100")
        rows = cur.fetchall()
        for row in rows:
            book = get_book_data(row[1])
            history.append({
                'book_title': book.get('title', ''),
                'book_author': book.get('author', ''),
                'book_id': row[1],
                'user_name': row[2],
                'user_id': row[3],
                'issue_date': row[4],
                'due_date': row[5],
                'return_date': row[6],
                'fine': row[7]
            })
    except Exception as e:
        flash("⚠️ Error: " + str(e))
    conn.close()
    return render_template("issue_return.html", stats=stats, history=history)

# ✅ Book Data Helper
def get_book_data(accession_no):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT title, author FROM books WHERE accession = ?", (accession_no,))
    row = cur.fetchone()

    # Check if book is already issued
    cur.execute("SELECT COUNT(*) FROM issued_books WHERE accession_no = ? AND return_date IS NULL", (accession_no,))
    issued = cur.fetchone()[0]
    conn.close()

    if row:
        return {
            "title": row[0],
            "author": row[1],
            "available": issued == 0
        }
    else:
        return {}

# ✅ Fetch User Details
@app.route("/get_user/<account_no>")
def get_user(account_no):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name, 'Student' FROM students WHERE account_no = ?", (account_no,))
    row = cur.fetchone()

    if not row:
        cur.execute("SELECT name, 'Teacher' FROM teachers WHERE account_no = ?", (account_no,))
        row = cur.fetchone()

    conn.close()
    if row:
        return jsonify({"name": row[0], "role": row[1]})
    return jsonify({"error": "User not found"})

# ✅ Fetch Active Issue Details
@app.route("/get_book/<accession_no>")
def get_book(accession_no):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT title, author FROM books WHERE accession = ?", (accession_no,))
    row = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM issued_books WHERE accession_no = ? AND return_date IS NULL", (accession_no,))
    issued = cur.fetchone()[0]
    conn.close()

    if row:
        return jsonify({
            "title": row[0],
            "author": row[1],
            "available": issued == 0
        })
    else:
        return jsonify({"error": "Book not found"})
@app.route("/get_issue_details/<accession_no>")
def get_issue_details(accession_no):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Fetch from issued_books where not returned yet
    cur.execute("SELECT student_name, issue_date, due_date FROM issued_books WHERE accession_no = ? AND return_date IS NULL", (accession_no,))
    row = cur.fetchone()
    conn.close()

    if row:
        book = get_book_data(accession_no)
        return jsonify({
            "user_name": row[0],
            "issue_date": row[1],
            "due_date": row[2],
            "title": book.get("title", "")
        })

    return jsonify({"error": "No active issue found"})

# ✅ Issue Book
@app.route("/issue_book", methods=["POST"])
def issue_book():
    accession_no = request.form.get("book_id")
    account_no = request.form.get("user_id").upper()
    issue_date = request.form.get("issue_date")
    due_date = request.form.get("due_date")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM students WHERE account_no = ?", (account_no,))
    row = cur.fetchone()
    if not row:
        cur.execute("SELECT name FROM teachers WHERE account_no = ?", (account_no,))
        row = cur.fetchone()

    if not row:
        conn.close()
        flash("❌ Invalid Account ID")
        return redirect("/issue")

    cur.execute("SELECT COUNT(*) FROM issued_books WHERE accession_no = ? AND return_date IS NULL", (accession_no,))
    already_issued = cur.fetchone()[0]
    if already_issued > 0:
        flash("⚠️ Book is already issued!")
        conn.close()
        return redirect("/issue")

    user_name = row[0]
    cur.execute("INSERT INTO issued_books (accession_no, student_name, user_id, issue_date, due_date) VALUES (?, ?, ?, ?, ?)",
                (accession_no, user_name, account_no, issue_date, due_date))
    conn.commit()
    conn.close()
    flash("✅ Book issued successfully!")
    return redirect("/issue")

# ✅ Return Book
@app.route("/return_book", methods=["POST"])
def return_book():
    accession_no = request.form.get("return_book_id")
    return_date = request.form.get("return_date")
    fine = request.form.get("fine") or 0

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("UPDATE issued_books SET return_date = ?, fine = ? WHERE accession_no = ? AND return_date IS NULL",
                (return_date, fine, accession_no))
    conn.commit()
    conn.close()
    flash("✅ Book returned successfully!")
    return redirect("/issue")
@app.route("/download_issue_receipt")
def download_issue_receipt():
    book_id = request.args.get("book_id")
    user_id = request.args.get("user_id")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM issued_books WHERE accession_no = ? AND user_id = ? ORDER BY id DESC LIMIT 1",
                (book_id, user_id))
    row = cur.fetchone()
    conn.close()

    if not row:
        return "❌ Error: No issue record found!", 404

    book = get_book_data(book_id)
    user_name = row[2]
    issue_date = row[4]
    due_date = row[5]

    filename = f"issue_receipt_{book_id}_{user_id}.txt"
    content = f"""📚 Chinmaya Smart Library – Book Issue Receipt

Book Title   : {book.get('title', 'N/A')}
Book ID      : {book_id}
Issued To    : {user_name} ({user_id})
Issue Date   : {issue_date}
Due Date     : {due_date}
Status       : ✅ Issued

Thank you for using Chinmaya Library!
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return send_file(filename, as_attachment=True)
@app.route("/download_return_receipt")
def download_return_receipt():
    book_id = request.args.get("book_id")
    fine = request.args.get("fine", "0")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ✅ Get the latest returned record with fine and return_date
    cur.execute("""
        SELECT * FROM issued_books 
        WHERE accession_no = ? AND return_date IS NOT NULL 
        ORDER BY return_date DESC, id DESC LIMIT 1
    """, (book_id,))
    
    row = cur.fetchone()
    conn.close()

    if not row:
        return "❌ No return record found", 404

    user_name = row[2]
    return_date = row[6]
    due_date = row[5]

    # Fine calculation again (optional)
    try:
        overdue_days = (datetime.strptime(return_date, "%Y-%m-%d") - datetime.strptime(due_date, "%Y-%m-%d")).days
        if overdue_days < 0:
            overdue_days = 0
    except Exception:
        overdue_days = 0

    book = get_book_data(book_id)

    filename = f"return_receipt_{book_id}.txt"
    content = f"""📗 Chinmaya Smart Library – Book Return Receipt

Book Title   : {book.get('title', 'N/A')}
Book ID      : {book_id}
Returned By  : {user_name}
Return Date  : {return_date}
Due Date     : {due_date}
Overdue Days : {overdue_days}
Fine         : ₹{fine}

Please return books on time. Thank you!
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return send_file(filename, as_attachment=True)

# 🔧 Ensure events table exists
def init_events_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        date TEXT,
        time TEXT,
        location TEXT,
        category TEXT,
        poster TEXT
    )
    """)
    conn.commit()
    conn.close()

init_events_table()

# ✅ Route: View Events Page
@app.route("/events")
def events():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today = datetime.now().date()
    c.execute("SELECT * FROM events")
    rows = c.fetchall()
    conn.close()

    upcoming_events = []
    past_events = []

    for row in rows:
        event_date = datetime.strptime(row[3], "%Y-%m-%d").date()
        event = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'date': row[3],
            'time': row[4],
            'location': row[5],
            'category': row[6],
            'poster': row[7]
        }
        if event_date >= today:
            upcoming_events.append(event)
        else:
            past_events.append(event)

    # Sort by date
    upcoming_events = sorted(upcoming_events, key=lambda x: x['date'])
    past_events = sorted(past_events, key=lambda x: x['date'], reverse=True)

    return render_template("events.html",
                           upcoming_events=upcoming_events,
                           past_events=past_events)

# ✅ Route: Add New Event
@app.route("/add_event", methods=["POST"])
def add_event():
    title = request.form['title']
    description = request.form['description']
    date = request.form['date']
    time = request.form['time']
    location = request.form['location']
    category = request.form['category']
    poster_file = request.files['poster']

    poster_filename = None
    if poster_file and poster_file.filename != "":
        poster_filename = os.path.join(UPLOAD_FOLDER, poster_file.filename)
        poster_file.save(poster_filename)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO events (title, description, date, time, location, category, poster)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, date, time, location, category, poster_filename))
    conn.commit()
    conn.close()

    return redirect(url_for('events'))

# 🔧 Create 'news' table if not exists
def init_news_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            date TEXT,
            priority TEXT,
            attachment TEXT
        )
    """)
    conn.commit()
    conn.close()

# 🟡 Call initializer at start
init_news_table()

# ✅ Route: News Page
@app.route("/news")
def news():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM news ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()

    news_list = []
    for row in rows:
        news_item = {
            'id': row[0],
            'title': row[1],
            'content': row[2],
            'date': row[3],
            'priority': row[4],
            'attachment': row[5]
        }
        news_list.append(news_item)

    return render_template("news.html", news_list=news_list)

# ✅ Route: Add News POST Handler
@app.route("/add_news", methods=["POST"])
def add_news():
    title = request.form['title']
    content = request.form['content']
    date = request.form['date']
    priority = request.form['priority']
    file = request.files['attachment']

    attachment_path = None
    if file and file.filename != "":
        filename = file.filename
        attachment_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(attachment_path)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO news (title, content, date, priority, attachment)
        VALUES (?, ?, ?, ?, ?)
    """, (title, content, date, priority, attachment_path))
    conn.commit()
    conn.close()

    return redirect(url_for('news'))


import pandas as pd

# ✅ Initialize DB
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                role TEXT,
                category TEXT,
                message TEXT,
                filename TEXT,
                date TEXT,
                status TEXT DEFAULT 'Pending',
                reply TEXT
            )
        ''')
        conn.commit()

init_db()

import sqlite3
import os

DB_PATH = "library.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Function to create the table automatically
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                role TEXT,
                email TEXT,
                title TEXT,
                description TEXT,
                filename TEXT,
                date TEXT,
                status TEXT DEFAULT 'Open'
            )
        ''')
        conn.commit()

# ✅ Call this function when app starts
init_db()

# ✅ Ask Librarian Page
@app.route("/ask_librarian", methods=["GET", "POST"])
def ask_librarian():
    if request.method == "POST":
        name = request.form['name']
        role = request.form['role']
        category = request.form['category']
        message = request.form['message']
        file = request.files.get('file')
        
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO queries (name, role, category, message, filename, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, role, category, message, filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        return redirect(url_for("my_queries"))
    
    return render_template("ask_librarian.html")

# ✅ My Queries Page
@app.route("/my_queries")
def my_queries():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, role, category, message, filename, date, status, reply FROM queries ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("my_queries.html", queries=data)

# ✅ Help Page
@app.route("/help")
def help_page():
    return render_template("help.html")

# ✅ Librarian Reply Center
@app.route("/reply_center", methods=["GET", "POST"])
def reply_center():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == "POST":
        query_id = request.form["query_id"]
        reply_text = request.form["reply"]
        cur.execute("UPDATE queries SET reply = ?, status = 'Replied' WHERE id = ?", (reply_text, query_id))
        conn.commit()

    cur.execute("SELECT id, name, role, category, message, filename, status, reply FROM queries ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("reply_center.html", queries=data)

# ✅ Query Status Page
@app.route("/query_status")
def query_status():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, status, reply, date FROM queries ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("query_status.html", statuses=data)

# ✅ Download Excel Report
@app.route("/download_queries")
def download_queries():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM queries", conn)
    filepath = os.path.join("static", "query_report.xlsx")
    df.to_excel(filepath, index=False)
    conn.close()
    return send_file(filepath, as_attachment=True)
@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        email = request.form["email"]
        title = request.form["title"]
        description = request.form["description"]
        file = request.files["file"]
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        filename = ""

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO queries (name, role, email, title, description, filename, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, role, email, title, description, filename, date))
            conn.commit()
        return redirect("/ask")

    # GET method: Show form + all queries
    search = request.args.get("search", "")
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        if search:
            cur.execute("SELECT * FROM queries WHERE name LIKE ? OR title LIKE ? ORDER BY id DESC", 
                        (f"%{search}%", f"%{search}%"))
        else:
            cur.execute("SELECT * FROM queries ORDER BY id DESC")
        queries = cur.fetchall()
    return render_template("ask_librarian.html", queries=queries)

if __name__ == "__main__":
    app.run(debug=True)
