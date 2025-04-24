from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Book,User


# very important (user data access from any page)
@app.context_processor
def inject_users():
    users = User.query.all()
    return dict(all_users=users)


@app.route('/')
def index():
    users = User.query.all()
    print(users)
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')  # Match form field name
        if username:
            user = User(name=username)  # User model has `name` column
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        return "Username is required", 400
    return render_template('add_user.html')

@app.route('/add_book/<int:user_id>', methods=['GET', 'POST'])
def add_book(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        title = request.form['title']
        if title:
            book = Book(title=title, user_id=user.id)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('view_user_books', user_id=user.id))
        return "Title is required", 400
    return render_template('add_book.html', user=user)

@app.route('/user/<int:user_id>')
def view_user_books(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_books.html', user=user)

@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        db.session.commit()
        return redirect(url_for('view_user_books', user_id=book.user_id))
    return render_template('update_book.html', book=book)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    user_id = book.user_id
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('view_user_books', user_id=user_id))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))