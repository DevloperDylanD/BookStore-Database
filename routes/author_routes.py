from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models import db, Author

author_bp = Blueprint('author', __name__)


@author_bp.route('/authors')
@login_required
def authors():
    return render_template('authors.html', authors=Author.query.all())


@author_bp.route('/author/add', methods=['GET', 'POST'])
@login_required
def add_author():
    if request.method == 'POST':
        db.session.add(Author(name=request.form['name']))
        db.session.commit()
        return redirect('/authors')

    return render_template('add_author.html')


@author_bp.route('/author/delete/<int:id>')
@login_required
def delete_author(id):
    db.session.delete(Author.query.get(id))
    db.session.commit()
    return redirect('/authors')
