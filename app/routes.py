from app import app, db # from app package, import app variable
from flask import render_template, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from werkzeug import secure_filename

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
  user = User.query.get(current_user.get_id())
  if not user.admin or not user.is_authenticated:
    return redirect(url_for('login'))
  users = User.query.all()
  form = AdminUsersForm()
  form.users_list.choices = [(user.id, "{}: {}".format(user.name, user.username)) for user in User.query.order_by('name') if user.username != 'admin-derek' and user != current_user]
  if request.method == 'POST':
    getUser = form.users_list.data
    selectedUser = User.query.get(getUser)
    if selectedUser.admin == False:
      selectedUser.admin = True
      db.session.commit()
    else:
      selectedUser.admin = False
      db.session.commit()
  return render_template('admin/users.html', form=form, users=users)

@app.route('/admin/new-user', methods=['GET', 'POST'])
@login_required
def newUsers():
  user = User.query.get(current_user.get_id())
  if not user.admin or not user.is_authenticated:
    return redirect(url_for('login'))
  form = AdminAddUserForm()
  if form.validate_on_submit():
    u = User(name=form.name.data, username=form.username.data, email=form.email.data, password_hash=form.username.data, admin=False)
    u.set_password(u.password_hash)
    db.session.add(u)
    db.session.commit()
  return render_template('admin/new-user.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_Required
def index():
    return render_template("index.html", name="Derek")
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index')) # Will return to the Index page if the user is authenticated
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash("Invalid email or password")
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    flash("You are signed in!")
    return redirect(url_for('index'))
  return render_template("login.html", title="Sign In", form=form)

login_user(user, remember=form.remember_me.data) #Preset to remember user credentials
next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(name=form.name.data, username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash("You are now registered!")
    return redirect(url_for('login'))
  return render_template("register.html", title="Register", form=form)
