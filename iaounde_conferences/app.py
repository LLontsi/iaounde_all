from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from functools import wraps
from config import Config, create_upload_dir
from config import Config
from models import db, Conference, User
from forms import ConferenceForm, LoginForm, UserForm
from flask import send_from_directory

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Connectez-vous pour accéder à cette page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Créer les dossiers et tables
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with app.app_context():
    db.create_all()
    create_upload_dir(app)
    # Créer super admin par défaut
    if not User.query.filter_by(role='super_admin').first():
        admin = User(username='admin', email='admin@iaounde.com', role='super_admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Super admin créé: admin / admin123")

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_super_admin():
            flash('Accès refusé.', 'error')
            return redirect(url_for('admin_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def save_logo(logo_file):
    if logo_file:
        filename = secure_filename(logo_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logo_file.save(logo_path)
        return filename
    return None

# ROUTES PUBLIQUES
@app.route('/')
def index():
    """Page d'accueil publique"""
    conferences = Conference.query.order_by(Conference.periode_debut.desc()).all()
    return render_template('index.html', conferences=conferences)

@app.route('/api/conferences')
def api_conferences():
    """API JSON pour les conférences"""
    conferences = Conference.query.all()
    return jsonify([{
        'id': c.id,
        'nom': c.nom,
        'periode_debut': c.periode_debut.strftime('%Y-%m-%d'),
        'periode_fin': c.periode_fin.strftime('%Y-%m-%d'),
        'logo': c.logo_url,
        'description': c.description,
        'lien_site': c.lien_site
    } for c in conferences])

# AUTHENTIFICATION
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('admin_dashboard'))
        flash('Identifiants incorrects.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnecté.', 'info')
    return redirect(url_for('index'))

# ADMIN - DASHBOARD
@app.route('/admin')
@login_required
def admin_dashboard():
    total_conferences = Conference.query.count()
    total_users = User.query.count()
    conferences_recentes = Conference.query.order_by(Conference.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                         total_conferences=total_conferences,
                         total_users=total_users,
                         conferences_recentes=conferences_recentes)

# ADMIN - CONFÉRENCES
@app.route('/admin/conferences')
@login_required
def admin_conferences():
    page = request.args.get('page', 1, type=int)
    conferences = Conference.query.order_by(Conference.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/conferences.html', conferences=conferences)

@app.route('/admin/conferences/add', methods=['GET', 'POST'])
@login_required
def admin_add_conference():
    form = ConferenceForm()
    if form.validate_on_submit():
        if form.periode_fin.data < form.periode_debut.data:
            flash('Date de fin invalide.', 'error')
            return render_template('admin/add_conference.html', form=form)
        
        logo_filename = save_logo(form.logo.data)
        conference = Conference(
            nom=form.nom.data,
            periode_debut=form.periode_debut.data,
            periode_fin=form.periode_fin.data,
            logo=logo_filename,
            description=form.description.data,
            lien_site=form.lien_site.data,
            created_by=current_user.id
        )
        db.session.add(conference)
        db.session.commit()
        flash('Conférence ajoutée!', 'success')
        return redirect(url_for('admin_conferences'))
    
    return render_template('admin/add_conference.html', form=form)

@app.route('/admin/conferences/<int:id>')
@login_required
def admin_view_conference(id):
    conference = Conference.query.get_or_404(id)
    return render_template('admin/view_conference.html', conference=conference)

@app.route('/admin/conferences/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_conference(id):
    conference = Conference.query.get_or_404(id)
    form = ConferenceForm(obj=conference)
    
    if form.validate_on_submit():
        if form.periode_fin.data < form.periode_debut.data:
            flash('Date de fin invalide.', 'error')
            return render_template('admin/edit_conference.html', form=form, conference=conference)
        
        if form.logo.data:
            if conference.logo:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], conference.logo)
                if os.path.exists(old_path):
                    os.remove(old_path)
            conference.logo = save_logo(form.logo.data)
        
        conference.nom = form.nom.data
        conference.periode_debut = form.periode_debut.data
        conference.periode_fin = form.periode_fin.data
        conference.description = form.description.data
        conference.lien_site = form.lien_site.data
        conference.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Conférence modifiée!', 'success')
        return redirect(url_for('admin_view_conference', id=conference.id))
    
    return render_template('admin/edit_conference.html', form=form, conference=conference)

@app.route('/admin/conferences/<int:id>/delete', methods=['POST'])
@login_required
def admin_delete_conference(id):
    conference = Conference.query.get_or_404(id)
    if conference.logo:
        logo_path = os.path.join(app.config['UPLOAD_FOLDER'], conference.logo)
        if os.path.exists(logo_path):
            os.remove(logo_path)
    
    db.session.delete(conference)
    db.session.commit()
    flash('Conférence supprimée!', 'success')
    return redirect(url_for('admin_conferences'))

# ADMIN - UTILISATEURS (Super Admin uniquement)
@app.route('/admin/users')
@login_required
@super_admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
@super_admin_required
def admin_add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Utilisateur {user.username} créé!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/add_user.html', form=form)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Servir tous les fichiers uploadés"""
    upload_base = os.path.dirname(app.config['UPLOAD_FOLDER'])  # /app/uploads
    return send_from_directory(upload_base, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
