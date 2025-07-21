from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, CensusForm
from models import db, User, CensusEntry
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace_this_with_a_random_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    entries = CensusEntry.query.order_by(CensusEntry.entry_date).all()
    return render_template('dashboard.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = CensusForm()
    if form.validate_on_submit():
        existing = CensusEntry.query.filter_by(entry_date=form.entry_date.data).first()
        if existing:
            flash('An entry for this date already exists. You can edit it below.')
            return redirect(url_for('edit_entry', entry_id=existing.id))
        entry = CensusEntry(
            entry_date=form.entry_date.data,
            m_old_male=form.m_old_male.data,
            m_old_female=form.m_old_female.data,
            m_old_child=form.m_old_child.data,
            m_new_male=form.m_new_male.data,
            m_new_female=form.m_new_female.data,
            m_new_child=form.m_new_child.data,
            e_old_male=form.e_old_male.data,
            e_old_female=form.e_old_female.data,
            e_old_child=form.e_old_child.data,
            e_new_male=form.e_new_male.data,
            e_new_female=form.e_new_female.data,
            e_new_child=form.e_new_child.data,
        )
        db.session.add(entry)
        db.session.commit()
        flash('Census data added!')
        return redirect(url_for('dashboard'))
    return render_template('add_entry.html', form=form)

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = CensusEntry.query.get_or_404(entry_id)
    form = CensusForm(obj=entry)
    if form.validate_on_submit():
        # Prevent changing to a date that causes a duplicate
        existing = CensusEntry.query.filter(
            CensusEntry.entry_date == form.entry_date.data,
            CensusEntry.id != entry.id
        ).first()
        if existing:
            flash('Another entry for this date already exists.')
            return render_template('edit_entry.html', form=form, entry=entry)

        entry.entry_date = form.entry_date.data
        entry.m_old_male = form.m_old_male.data
        entry.m_old_female = form.m_old_female.data
        entry.m_old_child = form.m_old_child.data
        entry.m_new_male = form.m_new_male.data
        entry.m_new_female = form.m_new_female.data
        entry.m_new_child = form.m_new_child.data
        entry.e_old_male = form.e_old_male.data
        entry.e_old_female = form.e_old_female.data
        entry.e_old_child = form.e_old_child.data
        entry.e_new_male = form.e_new_male.data
        entry.e_new_female = form.e_new_female.data
        entry.e_new_child = form.e_new_child.data
        db.session.commit()
        flash('Census entry updated.')
        return redirect(url_for('dashboard'))
    return render_template('edit_entry.html', form=form, entry=entry)

@app.route('/download')
@login_required
def download():
    # Fetch query parameters
    month = request.args.get('month')  # e.g., '2025-06'
    year = request.args.get('year')    # e.g., '2025'
    query = CensusEntry.query
    if month:
        year_part, month_part = month.split('-')
        query = query.filter(
            db.extract('year', CensusEntry.entry_date) == int(year_part),
            db.extract('month', CensusEntry.entry_date) == int(month_part)
        )
    elif year:
        query = query.filter(db.extract('year', CensusEntry.entry_date) == int(year))
    query = query.order_by(CensusEntry.entry_date)
    entries = query.all()
    data = []
    for e in entries:
        morning_total = (
            (e.m_old_male or 0) + (e.m_old_female or 0) + (e.m_old_child or 0) +
            (e.m_new_male or 0) + (e.m_new_female or 0) + (e.m_new_child or 0)
        )
        evening_total = (
            (e.e_old_male or 0) + (e.e_old_female or 0) + (e.e_old_child or 0) +
            (e.e_new_male or 0) + (e.e_new_female or 0) + (e.e_new_child or 0)
        )
        grand_total = morning_total + evening_total
        data.append({
            'Date': e.entry_date.strftime('%Y-%m-%d'),
            'Morning Old Male': e.m_old_male,
            'Morning Old Female': e.m_old_female,
            'Morning Old Child': e.m_old_child,
            'Morning New Male': e.m_new_male,
            'Morning New Female': e.m_new_female,
            'Morning New Child': e.m_new_child,
            'Morning Total': morning_total,
            'Evening Old Male': e.e_old_male,
            'Evening Old Female': e.e_old_female,
            'Evening Old Child': e.e_old_child,
            'Evening New Male': e.e_new_male,
            'Evening New Female': e.e_new_female,
            'Evening New Child': e.e_new_child,
            'Evening Total': evening_total,
            'Grand Total': grand_total,
        })
    df = pd.DataFrame(data)
    filename = 'census_data.xlsx'
    df.to_excel(filename, index=False)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
