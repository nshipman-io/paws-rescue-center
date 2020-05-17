from flask import Flask, render_template, abort, session, redirect, url_for
from forms import SignUpForm, SignInForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "KfbFLD5f545p5Vo5FANe4jyV"
pets = [
        {"id": 1, "name": "Nelly", "age": "5 weeks", "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
        {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
        {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
        {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."}, 
    ]

users = [
         {"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.com", "password": "adminpass"},
    ]

@app.route("/")
def home():

    return render_template("home.html",pets=pets)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    pet = next((pet for pet in pets if pet_id is pet["id"]), None)
    if pet is None:
        abort(404, description="No pet with given ID found.")

    return render_template("details.html",pet=pet)

@app.route("/signup",methods=["GET","POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Form submitted and Valid")
        user = {"id":len(users)+1, "full_name":form.name.data, "email":form.email.data, "password":form.password.data}
        users.append(user)
        print(f'Adding user: {user["full_name"]} to database.')
        return render_template("signup.html", message="Successfully signed up")
    elif form.errors:
        print(form.errors.items())
        print(form.name.errors)
        print(form.email.errors)
        print(form.password.errors)
        print(form.confirm.errors)
    return render_template("signup.html",form=form)

@app.route("/signin",methods=["GET","POST"])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        session_user = None
        i = 0
        while session_user is None and i < len(users):
            user = users[i]
            if form.email.data == user["email"]:
                session_user = user
            else:
                i+=1
        if session_user is None:
            return render_template("signin.html",message="Email not found",form=form)
        if form.password.data != session_user["password"]:
            print(f'Wrong password entered for user: {session_user["email"]}')
            return render_template("signin.html",message="Wrong password",form=form)
        else:
            session["USERNAME"] = session_user["full_name"]
            return redirect(url_for('home'))

    return render_template("signin.html",form=form)

@app.route("/signout")
def signout():
    session.pop("USERNAME",None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)