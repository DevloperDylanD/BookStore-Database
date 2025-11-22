from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models import db, Book, Author

book_bp = Blueprint('book', __name__)


@book_bp.route('/books')
@login_required
def books():
    authors = {a.author_id: a.name for a in Author.query.all()}
    return render_template('books.html', books=Book.query.all(), authors=authors)


@book_bp.route('/book/add', methods=['GET', 'POST'])
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

    return render_template('add_book.html', authors=Author.query.all())


@book_bp.route('/book/delete/<int:id>')
@login_required
def delete_book(id):
    db.session.delete(Book.query.get(id))
    db.session.commit()
    return redirect('/books')
