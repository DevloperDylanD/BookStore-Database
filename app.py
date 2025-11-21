from flask import Flask, render_template, request, redirect
from models import db, Customer
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
db.init_app(app)

# CREATE DATABASE
with app.app_context():
    db.create_all()


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ----------- CUSTOMER CRUD -----------
@app.route('/customers')
def customers():
    all_customers = Customer.query.all()
    return render_template('customers.html', customers=all_customers)

@app.route('/customer/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        new_customer = Customer(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form['address']
        )
        db.session.add(new_customer)
        db.session.commit()
        return redirect('/customers')
    return render_template('add_customer.html')

@app.route('/customer/delete/<int:id>')
def delete_customer(id):
    cust = Customer.query.get(id)
    db.session.delete(cust)
    db.session.commit()
    return redirect('/customers')


# ----------- CHART VISUALIZATION -----------
@app.route('/chart')
def chart():
    customers = Customer.query.all()
    names = [c.name for c in customers]
    ids = [c.customer_id for c in customers]

    plt.bar(ids, range(len(ids)))
    plt.title("Customer Count Example")
    plt.xlabel("Customer ID")
    plt.ylabel("Dummy Count")
    plt.savefig('static/chart.png')
    plt.close()

    return "<img src='/static/chart.png'>"


# ------------- RUN APP -------------
if __name__ == '__main__':
    app.run(debug=True)
