import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
import pickle
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app=Flask(__name__, static_folder='Static')
model=pickle.load(open('model.pkl','rb'))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


# @app.route("/")
# def home():
#     print("Helloo")
#     return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route("/loginNew", methods=['GET', 'POST'])
def loginMera():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



# apna wala



# template_dir = os.path.abspath('/templates/index.html')#


@app.route("/")
@app.route("/frontPage.html")
def hello():
    return render_template('frontPage.html')

@app.route("/docForm.html")
def helloDoc():
    return render_template('docForm.html')

@app.route("/index.html")
def helloSymptoms():
    return render_template('index.html')

@app.route("/sub",methods=['POST'])
def submit():
    if request.method=="POST": 

        sym1=request.form.get("symptom1")
        sym2=request.form.get("symptom2")
        sym3=request.form.get("symptom3")
        sym4=request.form.get("symptom4")
        sym5=request.form.get("symptom5")
        sym6=request.form.get("symptom6")
        # print(sym1,sym2,sym3,sym4,sym5,sym6)

        first_symptom=int(sym1[0:2])
        second_symptom=int(sym2[0:2])
        third_symptom=int(sym3[0:2])
        fourth_symptom=int(sym4[0:2])
        fivth_symptom=int(sym5[0:2])
        sixth_symptom=int(sym6[0:2])

        li=[0]*70

        if first_symptom!=0:
            li[first_symptom-1]=1
        if second_symptom!=0:
            li[second_symptom-1]=1
        if third_symptom!=0:    
            li[third_symptom-1]=1
        if fourth_symptom!=0:
            li[fourth_symptom-1]=1
        if fivth_symptom!=0:
            li[fivth_symptom-1]=1
        if sixth_symptom!=0:
            li[sixth_symptom-1]=1
       

        final_features=[np.array(li)]
        output=model.predict(final_features)

    # lists=output.tolist()
    # json_str=json.dumps(lists)
    # return json_str

    
    return render_template("submit.html",s=output)

