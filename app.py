from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AccountList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


@app.route("/")
def home():
    account_list = AccountList.query.all()
    return render_template("base.html", account_list=account_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    email = request.form.get("email")
    password = request.form.get("password")
    new_account_info = AccountList(title=title,email=email,password = password)
    db.session.add(new_account_info)
    db.session.commit()
    return redirect(url_for("home"))


# @app.route("/update/<int:account_id>",methods=['GET', 'POST'])
# def update(account_id):
#     # todo = AccountList.query.filter_by(id=account_id).first()
#     todo = AccountList.query.get_or_404(account_id)

#     if request.method=='POST':
#         todo.title = request.form['title']
#         todo.email = request.form['email']
#         todo.password = request.form['password']
#         db.session.commit()
#         return redirect(url_for("home"))
#     else:
#         return render_template('update.html', todo=todo)

@app.route('/update<int:account_id>', methods = ['GET', 'POST'])
def update(account_id):
 
    todo = AccountList.query.get_or_404(account_id)
    if request.method == 'POST':
        # todo = AccountList.query.get(request.form.get('account_id'))
 
        todo.title = request.form['title']
        todo.email = request.form['email']
        todo.password = request.form['password']
 
        db.session.commit()
        return redirect('/base')
    else:
        # return redirect(url_for('home'))
        render_template('update.html',account_list=todo)


@app.route("/delete/<int:account_id>")
def delete(account_id):
    todo = AccountList.query.filter_by(id=account_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)