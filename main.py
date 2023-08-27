from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    nick_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'
    
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    adress = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    exp_date = db.Column(db.String(20), nullable=False)
    cvv = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'




airs = ["selfair.html","selfair2.html","selfair3.html"]

def cost(price,v,name,shit):
    name=name
    shit=shit
    return price * v

@app.route("/Self_air")
def selfair():
    return render_template(f"{random.choice(airs)}")

@app.route("/", methods = ['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

        users_db = User.query.all()

        for user in users_db:
            if user.login == form_login and user.password == form_password:
                    if user.login == 'admin6666@gmail.com' and user.password == 'admin666':
                        return redirect('/admin')
                    else:
                        return redirect('/index')
        else:
            error = 'Неправильный пользователь или пароль'
            return render_template('login.html', error = error)

    else:
        return render_template('login.html')

@app.route('/registration', methods = ['GET', 'POST'])
def reg():
    error = ''
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        nick_name = request.form['text']

        users = User.query.all()

        for user in users:
            if user.login == login:
                error = 'Такая почта уже была зарегестрирована'
                return render_template("reg.html", error=error)
        else:
            user_card = User(login=login, password=password, nick_name=nick_name)

            db.session.add(user_card)
            db.session.commit()

            return redirect('/')
    else:
        return render_template("reg.html")

@app.route('/admin')
def admin():
    users = User.query.order_by(User.id).all()
    return render_template('admin.html', users = users)

@app.route("/adv_admin")
def advanced_admin():
    users_info = Info.query.order_by(Info.id).all()
    return render_template("advanced_admin.html", users_info=users_info)

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/products')
def products():
    return render_template('products.html')

@app.route("/Alp_Fresh/<price>")
def alp_fresh(price):
    return render_template("alpfresh.html", price=price)

@app.route("/rates")
def rates():
    return render_template("rates.html")

@app.route("/Pug's_Fart/<price>")
def pugsfart(price):
    return render_template("pugsfart.html", price=price)

@app.route("/Sea_Breaze/<price>")
def seabreaze(price):
    return render_template("seabreaze.html", price=price)

@app.route("/Alp_Fresh/<price>/V")
def alpfreshv(price):
    return render_template("v.html", price=price)

@app.route("/Pug's_Fart/<price>/V")
def pugsfartv(price):
    return render_template("v.html", price=price)

@app.route("/Sea_Breaze/<price>/V")
def seabreazev(price):
    return render_template("v.html", price=price)

@app.route("/<name>/<shit>/<price>/<v>")
def v(name,shit,price,v):
    return render_template("total.html", result=cost(int(price), float(v), name=0, shit=0))



@app.route('/submit', methods=['POST'])
def error():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']
    cvv = request.form['cvv']
    number = request.form['number']

    info_card = Info(name=name, adress=address, email=email, card_number=number, exp_date=date, cvv=cvv)

    db.session.add(info_card)
    db.session.commit()

    return render_template('tryonemoretime.html',  
                           name = name, 
                           email = email, 
                           address = address, 
                           date = date, 
                           cvv = cvv, 
                           number = number
                           )
    

if __name__ == "__main__":
    app.run(debug=True)