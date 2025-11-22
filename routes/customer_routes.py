from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models import db, Customer

customer_bp = Blueprint('customer', __name__)


@customer_bp.route('/')
def home():
    return render_template('index.html')


@customer_bp.route('/customers')
@login_required
def customers():
    return render_template('customers.html', customers=Customer.query.all())


@customer_bp.route('/customer/add', methods=['GET', 'POST'])
@login_required
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


@customer_bp.route('/customer/delete/<int:id>')
@login_required
def delete_customer(id):
    db.session.delete(Customer.query.get(id))
    db.session.commit()
    return redirect('/customers')
