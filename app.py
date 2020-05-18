from flask import Flask, render_template, abort, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import SignUpForm, SignInForm, EditPetForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "KfbFLD5f545p5Vo5FANe4jyV"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(35), nullable=False)
    full_name = db.Column(db.String, nullable=False)
    pets = db.relationship('Pet', backref='user')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    posted_by = db.Column(db.String, db.ForeignKey('user.id'))

db.create_all()

team = User(full_name="Pet Rescue Team", email="team@pawsrescue.com", password="adminpass")
nelly = Pet(name = "Nelly", age = "5 weeks", bio = "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yuki = Pet(name = "Yuki", age = "8 months", bio = "I am a handsome gentle-cat. I like to dress up in bow ties.")
basker = Pet(name = "Basker", age = "1 year", bio = "I love barking. But, I love my friends more.")
mrfurrkins = Pet(name = "Mr. Furrkins", age = "5 years", bio = "Probably napping.")

db.session.add(team)
db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mrfurrkins)

try:
    db.session.commit()
except Exception as e:
    print(e)
finally:
    db.session.close()

@app.route("/")
def home():
    pet_query = Pet.query.all()
    pets = []
    for pet_obj in pet_query:
       pet = {"id":pet_obj.id,"name":pet_obj.name,"age":pet_obj.age,"bio":pet_obj.bio}
       pets.append(pet)
    return render_template("home.html",pets=pets)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No pet with given ID found.")
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.pet.bio
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            render_template("details.html",pet = pet,form = form,message="A Pet with this name already exists!")
    return render_template("details.html",pet=pet,form=form)

@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No pet with given ID found.")
    db.session.delete(pet)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for('homepage.html'))
    
@app.route("/signup",methods=["GET","POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Form submitted and Valid")
        new_user = User(email=form.email.data,password=form.password.data,full_name=form.name.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            print(f'Adding user: {form.name.data} to database.')
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html",message="Email is already in use",form=form)
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    
    return render_template("signup.html",form=form)

@app.route("/signin",methods=["GET","POST"])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            return render_template("signin.html",message="Email not found",form=form)
        elif user.password != form.password.data:
            return render_template("signin.html",message="Wrong password",form=form)
        else:
            session["USERID"] = user.id
            return redirect(url_for('home'))
    return render_template("signin.html",form=form)

@app.route("/signout")
def signout():
    session.pop("USERID")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)