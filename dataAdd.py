from app import app, db
from models import Customer, Author, Book, Order, OrderItem, Payment
import random

print("Adding sample data...")

with app.app_context():   # <<< FIX: add this wrapper

    # ----------- AUTHORS -----------
    authors_list = [
        "J.K. Rowling",
        "Stephen King",
        "George Orwell",
        "Jane Austen",
        "J.R.R. Tolkien",
        "Ernest Hemingway",
        "Agatha Christie",
        "Mark Twain",
        "C.S. Lewis",
        "F. Scott Fitzgerald"
    ]

    for i, name in enumerate(authors_list, start=1):
        a = Author(author_id=i, name=name)
        db.session.add(a)

    # ----------- BOOKS -----------
    books_list = [
        "Harry Potter",
        "The Shining",
        "1984",
        "Pride and Prejudice",
        "Lord of the Rings",
        "The Old Man and the Sea",
        "Murder on the Orient Express",
        "Huckleberry Finn",
        "The Chronicles of Narnia",
        "The Great Gatsby"
    ]

    for i, title in enumerate(books_list, start=1):
        b = Book(
            book_id=i,
            title=title,
            author_id=i,
            price=10.99 + i,
            genre="Fiction",
            stock_quantity=random.randint(10, 30)
        )
        db.session.add(b)

    # ----------- CUSTOMERS -----------
    for i in range(1, 11):
        c = Customer(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
            phone=f"555-000{i}",
            address=f"{i} Main Street"
        )
        db.session.add(c)

    # ----------- ORDERS -----------
    for i in range(1, 11):
        o = Order(
            order_id=i,
            customer_id=i,
            order_date="2025-01-01",
            total_amount=19.99 + i
        )
        db.session.add(o)

    # ----------- ORDER ITEMS -----------
    for i in range(1, 11):
        oi = OrderItem(
            order_id=i,
            book_id=i,
            quantity=random.randint(1, 5)
        )
        db.session.add(oi)

    # ----------- PAYMENTS -----------
    for i in range(1, 11):
        p = Payment(
            payment_id=i,
            order_id=i,
            payment_date="2025-01-01",
            amount=19.99 + i,
            method="Credit Card"
        )
        db.session.add(p)

    db.session.commit()

print("Data inserted successfully!")
