from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(

    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:topsecret@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello_world():
    return 'Hello World!'

# query strings
@app.route('/new/')
def query_strings(greeting='hello'):
    query_val = request.args.get('name', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)


# no query strings
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='mina'):
    return '<h1> hello there! {} </h1>'.format(name)


# strings
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'


# numbers
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> the number your picked is ' + str(num) + '</h1>'

# numbers 2
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1> the product is: {}'.format(num1+num2) + '</h1>'


# floats
@app.route('/products/<float:num1>/<float:num2>')
def product_two_numbers(num1, num2):
    return '<h1> the product is : {}'.format(num1 * num2) + '</h1>'


# using TEMPLATES
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

@app.route('/watch')
def movies_2017():
    movie_list =['autopsy of jane doe',
                 'neon demon',
                 'ghost in the shell',
                 'kong: skull island',
                 'john wick 2',
                 'spiderman - homecoming']
    return render_template('movies.html',
                           movies=movie_list,
                           name='Hary')


@app.route('/tables')
def movies_plus():
    movie_dict = {'autopsy of jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost in the shell': 1.50,
                 'kong: skull island': 3.50,
                 'john wick 2': 2.52,
                 'spiderman - homecoming': 1.48}
    return render_template('table_data.html',
                           movies=movie_dict,
                           name='Sally')

@app.route('/filters')
def filter_data():
    movie_dict = {'autopsy of jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost in the shell': 1.50,
                 'kong: skull island': 3.50,
                 'john wick 2': 2.52,
                 'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movie_dict,
                           name=None,
                           film='a christmas carol')


@app.route('/macros')
def jina_macros():
    movie_dict = {'autopsy of jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost in the shell': 1.50,
                 'kong: skull island': 3.50,
                 'john wick 2': 2.52,
                 'spiderman - homecoming': 1.48}

    return render_template('using_macros.html',
                           movies=movie_dict)


@app.route('/scrolling')
def scrolling_text():
    movie_dict = {'autopsy of jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost in the shell': 1.50,
                 'kong: skull island': 3.50,
                 'john wick 2': 2.52,
                 'spiderman - homecoming': 1.48}

    return render_template('scrolling_text.html',
                           movies=movie_dict)


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        # self.id = id
        self.name = name

    def __repr__(self):
        return 'The id {} , name is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))


    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id


    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run()
