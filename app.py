from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from models import db, Customer, User, Author, Book, Order, OrderItem, Payment

from flask import Flask, render_template, request, redirect
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE DATABASE
with app.app_context():
    db.create_all()


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ----------- CUSTOMER CRUD -----------
@app.route('/customers')
@login_required
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

# ---------------- AUTHORS ----------------

@app.route('/authors')
@login_required
def authors():
    all_authors = Author.query.all()
    return render_template('authors.html', authors=all_authors)


@app.route('/author/add', methods=['GET', 'POST'])
@login_required
def add_author():
    if request.method == 'POST':
        new_author = Author(
            name=request.form['name']
        )
        db.session.add(new_author)
        db.session.commit()
        return redirect('/authors')
    return render_template('add_author.html')


@app.route('/author/delete/<int:id>')
@login_required
def delete_author(id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()
    return redirect('/authors')

# ---------------- BOOKS ----------------

@app.route('/books')
@login_required
def books():
    all_books = Book.query.all()
    authors = {a.author_id: a.name for a in Author.query.all()}
    return render_template('books.html', books=all_books, authors=authors)

@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author_id=request.form['author_id'],
            price=request.form['price'],
            genre=request.form['genre'],
            stock_quantity=request.form['stock_quantity']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect('/books')

    all_authors = Author.query.all()
    return render_template('add_book.html', authors=all_authors)

@app.route('/book/delete/<int:id>')
@login_required
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')



# ----------- CHART -----------
@app.route('/chart')
@login_required
def chart():
    customers = Customer.query.all()

    labels = []
    totals = []

    for cust in customers:
        total_amount = db.session.query(db.func.sum(Order.total_amount)).filter_by(customer_id=cust.customer_id).scalar()
        if total_amount is None:
            total_amount = 0
        labels.append(cust.name)
        totals.append(total_amount)

    # Create bar chart
    plt.figure(figsize=(12, 5))
    plt.bar(labels, totals)
    plt.xlabel("Customer")
    plt.ylabel("Total Order Amount ($)")
    plt.title("Total Spending by Customer")
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('static/chart.png')
    plt.close()

    return "<img src='/static/chart.png'>"

# ---------------- ORDERS ----------------

@app.route('/orders')
@login_required
def orders():
    all_orders = Order.query.all()
    customers = {c.customer_id: c.name for c in Customer.query.all()}
    return render_template('orders.html', orders=all_orders, customers=customers)


@app.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        book_id = request.form['book_id']
        quantity = int(request.form['quantity'])

        # get book price
        book = Book.query.get(book_id)
        total_price = book.price * quantity

        # create order
        new_order = Order(
            customer_id=customer_id,
            order_date="2025-01-01",   # you can replace this with today's date if you want
            total_amount=total_price
        )
        db.session.add(new_order)
        db.session.commit()

        # create order item (using the order_id that was created after commit)
        order_item = OrderItem(
            order_id=new_order.order_id,
            book_id=book_id,
            quantity=quantity
        )
        db.session.add(order_item)
        db.session.commit()

        return redirect('/orders')

    all_customers = Customer.query.all()
    all_books = Book.query.all()

    return render_template('add_order.html', customers=all_customers, books=all_books)


@app.route('/order/delete/<int:id>')
@login_required
def delete_order(id):
    # delete all items in this order first
    OrderItem.query.filter_by(order_id=id).delete()

    # delete order itself
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return redirect('/orders')


# ----------- REGISTER -----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            email=request.form['email'],
            password=request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


# ----------- LOGIN -----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect('/')
        return "Invalid login. Try again."
    return render_template('login.html')


# ----------- LOGOUT -----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


# ------------- RUN APP LAST -------------
if __name__ == '__main__':
    app.run(debug=True)
