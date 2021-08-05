from flask import Blueprint, render_template, request, redirect, url_for, flash
from console_inventory.forms import UserLoginForm
from console_inventory.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        user = User(email, password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created: {email}', 'user-created')
        return redirect(url_for('site.home'))
        
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

    return render_template('signin.html', form = form)