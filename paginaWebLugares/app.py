from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from models import collectionSitios, collectionUsuarios, User, generarID
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse
from forms import LoginForm, RegistroForm, AgregarLugarForm
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'pinwino'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 600

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('lugares'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(form.username.data)
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('lugares')
            return redirect(next_page)
        else:
            error = "Usuario o contraseña incorrectos."
    return render_template('login.html', form=form, error=error)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    error = None
    form = RegistroForm()
    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        password = form.password.data
        usuarioExistente = User.find_by_username(username)
        if usuarioExistente is None:
            hashed_password = generate_password_hash(password)
            user_id = collectionUsuarios.insert_one({
                "username": username,
                "name": name,
                "password": hashed_password
            }).inserted_id
            user = User(user_id, username, name, hashed_password)
            login_user(user)
            return redirect(url_for('lugares'))
        else:
            error = "El usuario ya existe."
    return render_template('registro.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def lugares():
    return render_template('pagina_principal.html')

@app.route('/ver-lugares')
@login_required
def ver_lugares():
    lugares = collectionSitios.find()
    return render_template('ver_lugares.html', lugares=lugares)

@app.route('/agregar-lugar', methods=['GET', 'POST'])
@login_required
def agregar_lugar():
    error = None
    form = AgregarLugarForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        latitud = float(form.latitud.data)
        longitud = float(form.longitud.data)
        id = generarID("sitioid")
        
        lugarValido = collectionSitios.find_one({"nombre": nombre})
        if lugarValido is not None:
            error = "El lugar ya existe."
        else:
            collectionSitios.insert_one({
                "_id": id, # Cambiar por "id = generarID()
                "latitud": latitud,
                "longitud": longitud,
                "nombre_sitio": nombre
            })
            return redirect(url_for('ver_lugares'))
    return render_template('agregar_lugar.html', form=form, error=error)
    
@app.route('/eliminar-lugares', methods=['POST'])
@login_required
def eliminar_lugares():
    if request.method == 'POST':
        lugares = request.form.getlist('lugares')
        for lugar in lugares:
            collectionSitios.delete_one({"_id": int(lugar)})
    return redirect(url_for('ver_lugares'))

@app.route('/users')
@login_required
def users():
    users_list = collectionUsuarios.find()
    return render_template('usuarios.html', users=users_list)
