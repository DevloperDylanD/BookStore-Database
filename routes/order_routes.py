from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models import db, Order, OrderItem, Customer, Book

order_bp = Blueprint('order', __name__)


@order_bp.route('/orders')
@login_required
def orders():
    customers = {c.customer_id: c.name for c in Customer.query.all()}
    return render_template('orders.html', orders=Order.query.all(), customers=customers)


@order_bp.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_order():
    if request.method == 'POST':
        cust_id = request.form['customer_id']
        book_id = request.form['book_id']
        qty = int(request.form['quantity'])

        book = Book.query.get(book_id)
        total_price = book.price * qty

        order = Order(customer_id=cust_id, order_date="2025-01-01", total_amount=total_price)
        db.session.add(order)
        db.session.commit()

        item = OrderItem(order_id=order.order_id, book_id=book_id, quantity=qty)
        db.session.add(item)
        db.session.commit()

        return redirect('/orders')

    return render_template('add_order.html',
                           customers=Customer.query.all(),
                           books=Book.query.all())


@order_bp.route('/order/delete/<int:id>')
@login_required
def delete_order(id):
    OrderItem.query.filter_by(order_id=id).delete()
    db.session.delete(Order.query.get(id))
    db.session.commit()
    return redirect('/orders')
