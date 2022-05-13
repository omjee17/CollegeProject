import json
import os
from pydoc import doc
from unittest import result
import numpy as np
from flask import Flask, flash, render_template, request, send_from_directory, session
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

class doctor(db.Model):
   id = db.Column('doctor_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   phone = db.Column(db.String(10))
   specialization = db.Column(db.String(50))
   def __init__(self, name, city, phone,email, specialization):
    self.name = name
    self.city = city
    self.phone = phone
    self.email = email
    self.specialization = specialization


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


db.create_all()
# doctor add
@app.route('/getDoctors')
def show_all():
   return render_template('show.html', doctor = doctor.query.all() )


@app.route('/docForm', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city']:
         flash('Please enter all the fields', 'error')
      else:
         Doctor = doctor(request.form['name'], request.form['city'],
            request.form['phone'], request.form['email'], request.form['specialization'])
        
         db.session.add(Doctor)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('home.html')


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
    dos={
        "Fungal infection":"Wash your clothes daily in hot water, sun dry, and iron them before wearing. Wear loose cotton clothes. Keep your nails well-trimmed and clean.",
        "Allergy":"Take medications prescribed by your allergist regularly in the recommended dosage.",
        "GERD":"Do sleep on your left side to avoid putting extra pressure on the stomach. Also, keep your head elevated 4 to 6 inches if you suffer from nighttime acid reflux.",
        "Diabetes": "Eat more whole wheat bread and rotis, brown rice, and oats. Whole-grain starches give you more vitamins, minerals, and fibre than refined or white versions",
        "Gastroenteritis": "Drink antacids regularly. Also, keep your head elevated 4 to 6 inches if you suffer from nighttime acid reflux.",
        "Hypertension ": "Lose weight if you are overweight or obese.Eat a healthy diet, including more of fruits, vegetables, and low fat dairy products, less saturated and total fat.Potassium is an important for the maintenance of high blood pressure e.g coconut water, banana etc.",        
        "Migraine": " should take proper sleep. Don't skip meals. Keep body hydrated",        
        "Jaundice": "eating a balanced diet.exercising regularly.limiting alcohol consumption.",
        "Malaria": "Keep yourself hydrated at all times.Remember to reapply insect repellent frequently",
        "Chicken pox": "A cool bath with added baking soda, aluminum acetate, uncooked oatmeal.Calamine lotion dabbed on the spots. A soft, bland diet if chickenpox sores develop in the mouth.",
        "Pneumonia": "Drink warm beverages. take steamy baths and use a humidifier to help open your airways and ease your breathing.",
        "Dengue": "Use mosquito repellents and nets. Install screens on your doors and windows. Wear full-sleeve clothes to avoid mosquito bites. Keep yourself hydrated throughout the day and carry water. Do see a doctor if you show any symptoms of dengue",
        "Typhoid": "Keep yourself hydrated at all times.Remember to reapply insect repellent frequently",
        "hepatitis A": "Always wash your hands thoroughly after using the restroom and when you come in contact with an infected person's blood, stools, or other bodily fluid. Avoid unclean food and water",
        "Hepatitis B": "DO get plenty of rest and eat a well-balanced diet. DO use condoms when having sex.",
        "Hepatitis C": "DO get plenty of rest and eat a well-balanced diet. DO use condoms when having sex. DO avoid exposing others to your blood and other body fluids. DO call your health care provider if symptoms don't go away in 4 or 6 weeks or new symptoms develop.",
        "Tuberculosis": "Skip tobacco in all forms. Limit coffee and other caffeinated drinks. Limit refined products, like sugar, white breads, and white rice.",
        "Common Cold": "Always sneezing or coughing into a tissue, then discarding the tissue carefully and washing your hands at once.If there is no tissue available, coughing or sneezing into the upper shirt sleeve, covering the nose and mouth completely.Washing hands regularly with soapy water for at least 20 seconds.Keeping surfaces at work and in the home.",
        "Pneumonia": "Drink warm beverages. take steamy baths and use a humidifier to help open your airways and ease your breathing.       ",
        "Heart attack": "Always sneezing or coughing into a tissue, then discarding the tissue carefully and washing your hands at once.If there is no tissue available, coughing or sneezing into the upper shirt sleeve, covering the nose and mouth completely.Washing hands regularly with soapy water for at least 20 seconds.Keeping surfaces at work and in the home.",
        "Arthritis": "Focus on stretching, range-of-motion exercises and gradual progressive strength training. Include low-impact aerobic exercise, such as walking, cycling or water exercises, to improve your mood and help control your weight",
        "Acne": "Wash your face no more than twice each day with warm water and mild soap made especially for acne.Do not scrub the skin or burst the pimples, as this may push the infection further down, causing more blocking, swelling, and redness.Try to keep cool and dry in hot and humid climates, to prevent sweating.Keep hair clean, as it collects sebum and skin residue. ",
        "Urinary tract infection":"Along with an antibiotic, what you drink and eat during a UTI can help you get better faster. DO drink a lot of water, even if you're not thirsty. This will help flush out the bacteria. ",
    }

    dont={
        "Fungal infection": "Wear tight and wet clothes. Do manicures and pedicures especially in the rainy season.Share towels, napkins, or other clothes.Self-treat a fungal infection. It is best to reach out to a doctor in case you notice one.Use steroid creams without consulting a doctor",
        "Allergy": "Take more medication than recommended in an attempt to lessen your symptoms. Don't: Mow lawns or be around freshly cut grass; mowing stirs up pollens and molds. Hang sheets or clothing out to dry.",
        "GERD": "Don't eat spicy, acidic, or fatty foods or drink too much alcohol or lots of caffeinated or carbonated drinks. Limit chocolate, garlic, onions, and peppermint.",
        "Diabetes": "Avoid white bread, white rice, deep-fried foods and Indian sweets like laddoos, halwas and rasgullas, as they will quickly increase blood sugar.",
        "Gastroenteritis": "Don't eat spicy, acidic, or fatty foods or drink too much alcohol or lots of caffeinated or carbonated drinks. Limit chocolate, garlic, onions, and peppermint.",
        "Hypertension ": "Reduce the salt intake.Avoid canned, prepackaged, or processed foods. Avoid smoking and alcohol. Avoid stress.",
        "Migraine": "Don't exercise too much. Don't look to screen for long time.",
        "Jaundice": "avoiding herbal medications without consulting a healthcare professional first.avoiding taking more than the recommended dose of prescribed medications",
        "Malaria": "You must make sure to avoid fatty foods as much as possible. One must keep away from cold foods such as cucumber, watermelon, orange, banana and papaya.",
        "Chicken pox": "People should avoid close contact with people known to have chickenpox, avoid sharing objects with them, isolate any household members with chickenpox from others, and disinfect surfaces an infected person may have touched.",
        "Pneumonia": "Stay away from smoke to let your lungs heal. This includes smoking, secondhand smoke and wood smoke.",
        "Dengue": " Do not let water collect in open spaces and surroundings. Do not self-medicate if you have symptoms of dengue like fever and body ache. Avoid consuming paracetamol and aspirin-based medicines without medical supervision. Avoid giving steroids or antibiotics to dengue patients.",
        "Typhoid": "You must make sure to avoid fatty foods as much as possible. One must keep away from cold foods such as cucumber, watermelon, orange, banana and papaya.",
        "hepatitis A": " Your liver may have difficulty processing medications and alcohol. If you have hepatitis, don't drink alcohol. It can cause more liver damage",
        "Hepatitis B": "DO avoid exposing others to your blood and other body fluids. DO call your health care provider if symptoms don't go away in 4 or 6 weeks or new symptoms develop",
        "Hepatitis C": "Avoid drinking alcoholic beverages. Don't take a supplement, especially one with iron, until you've talked to your medical provider. Don't take acetaminophen or any over-the-counter drug without your doctor's knowledge.",
        "Tuberculosis": "Don't drink alcohol — it can add to the risk of liver damage from some of the drugs used to treat your TB.",
        "Common Cold": "Avoiding close contact with anyone who has a cold.Avoiding touching the face, especially the eyes, nose, and mouth.",
        "Pneumonia": "Stay away from smoke to let your lungs heal. This includes smoking, secondhand smoke and wood smoke.",
        "Heart attack": "Never leave the patient alone.Don’t wait to see if the symptoms go away.Do not give the person anything by mouth unless a heart medication has been prescribed.",
        "Arthritis": "Running.Jumping.Tennis.High-impact aerobics.Repeating the same movement, such as a tennis serve, again and again",
        "Acne": "Avoid greasy hair products, such as those containing cocoa butter.Avoid popping pimples, as this makes scarring likelier.Avoid excessive sun exposure, as it can cause the skin to produce more sebum. ",
        "Urinary tract infection":"DON'T drink coffee, alcohol or caffeine until the infection is gone.",
    }

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

    lists=output.tolist()
    json_str=json.dumps(lists)
    # return json_str
    
    str=json_str[0]
    x=json_str[2:-2].strip()
    print(dos[x])
    print(x)
    
    return render_template("submit.html",s=x,doslist=dos[x].split('.'),dontlist=dont[x].split('.'),doctor=doctor.query.all())

