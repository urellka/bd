from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db.db'
db = SQLAlchemy(app)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    books_genres = db.relationship('Book', backref='genre')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    books = db.relationship('Book', backref='author')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    book_name = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    book_text = db.Column(db.Text, nullable=False)
    book_release_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/book-list')
def book_list():
    books = Book.query.order_by(Book.id.desc()).all()
    authors = Author.query.order_by(Author.id.desc()).all()
    return render_template("book-list.html", books=books, authors=authors)


@app.route('/book-list/<int:id>')
def book_detail(id):
    book = Book.query.get(id)
    author = 'Автор отсутствует в БД'
    genre = 'Отсутствует в БД'
    if book.genre_id != 0:
        genre = Genre.query.join(Book, Genre.id == Book.genre_id).filter(book.genre_id == Genre.id).first().genre
    if book.author_id != 0:
        author = Author.query.join(Book, Author.id == Book.author_id).filter(book.author_id == Author.id).first().name
    return render_template("book_detail.html", book=book, author=author, genre=genre, book_id=id)


@app.route('/book-list/<int:id>/delete')
def book_delete(id):
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/book-list')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


@app.route('/create-book', methods=['POST', 'GET'])
def create_book():
    authors = Author.query.order_by(Author.id.desc()).all()
    genres = Genre.query.order_by(Genre.id.desc()).all()
    if request.method == "POST":
        author_id = "0"
        genre_id = "0"
        if Author.query.filter(Author.name == request.form['author']).first() != None:
            author_id = Author.query.filter(Author.name == request.form['author']).first().id
        if Genre.query.filter(Genre.genre == request.form['genre']).first() != None:
            genre_id = Genre.query.filter(Genre.genre == request.form['genre']).first().id
        name = request.form['name']
        text = request.form['text']
        book = Book(author_id=author_id, book_name=name, genre_id=genre_id, book_text=text)

        try:
           db.session.add(book)
           db.session.commit()
           return redirect('/book-list')
        except:
           return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-book.html", authors=authors, genres=genres)


@app.route('/create-author', methods=['POST', 'GET'])
def create_author():
    if request.method == "POST":
        initials = request.form['new_author']
        author = Author(name=initials)

        try:
           db.session.add(author)
           db.session.commit()
           return redirect('/create-book')
        except:
           return "При добавлении автора произошла ошибка"
    else:
        return render_template("create-author.html")


@app.route('/create-genre', methods=['POST', 'GET'])
def create_genre():
    if request.method == "POST":
        new_genre = request.form['new_genre']
        genre = Genre(genre=new_genre)

        try:
           db.session.add(genre)
           db.session.commit()
           return redirect('/create-book')
        except:
           return "При добавлении автора произошла ошибка"
    else:
        return render_template("create-genre.html")


if __name__ == "__main__":
    app.run(debug=True)