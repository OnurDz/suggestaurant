from flask import render_template, flash, redirect, url_for, request
from suggestaurant import app, db, bcrypt
from suggestaurant.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm
from suggestaurant.models import User
from flask_login import login_user, current_user, logout_user, login_required
import selection as s
import html

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, tel_no=form.tel_no.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'] )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('search'))
        else:
            flash('Login Unsuccessful! Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.tel_no = form.tel_no.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.tel_no.data = current_user.tel_no
        form.address.data = current_user.address
    image_file = url_for('static', filename='profile_pics/default.jpg')
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    entry_var = form.entry.data # hamburger
    eco = form.eco.data
    disc = form.disc.data
    distance = form.distance.data

    res_by_best = s.return_by_best()
    res_by_entry = filter_by_category(res_by_best, entry_var).head()

    res_name = res_by_entry['name'].tolist()
    res_score = res_by_entry['score'].tolist()
    res_disc = res_by_entry['discount'].tolist()

    res_name_disc = s.get_discounted(res_by_entry)['name'].tolist()
    res_name_disc_amount = s.get_discounted(res_by_entry)['discount'].tolist()

    res_name_eco = s.sort_by_eco(res_by_entry)['name']

    search_pressed = False
    if request.method == 'POST':
        search_pressed=True

    if eco == True:
        res_name=res_name_eco
    else:
        res_name=res_name

    if disc == True:
        return render_template('search.html', title='Search', form=form, arr_name=res_name_disc, arr_disc=res_name_disc_amount, search_pressed=search_pressed, disc=disc)
    else:
        return render_template('search.html', title='Search', form=form, arr_name=res_name, arr_disc = [], search_pressed=search_pressed, disc=disc)


def filter_by_category(df, food):
    return df[df.categories == food]
