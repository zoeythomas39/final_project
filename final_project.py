# imports

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os.path
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SelectField, SubmitField, StringField
import secrets
from flask_bootstrap import Bootstrap5
import re
from sqlalchemy import func
from wtforms.fields import HiddenField

# connecting database, creating flask app

db = SQLAlchemy()

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

csrf = CSRFProtect(app)

db_name = 'final_project.db'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

bootstrap = Bootstrap5(app)

class Elliott(db.Model):
    __tablename__ = 'elliott_smith'
    Index = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String)
    Album = db.Column(db.String)
    Date = db.Column(db.String)
    Year = db.Column(db.String)
    Lyrics = db.Column(db.String)
    Love = db.Column(db.String)
    Alcohol = db.Column(db.Integer)
    Lonely = db.Column(db.Integer)
    Smoke = db.Column(db.Integer)
    Dream = db.Column(db.Integer)
    Lie = db.Column(db.Integer)
    Life = db.Column(db.Integer)
    Death = db.Column(db.Integer)
    Sick = db.Column(db.Integer)
    City = db.Column(db.Integer)
    Home = db.Column(db.Integer)
    Time = db.Column(db.Integer)
    Lost = db.Column(db.Integer)
    Money = db.Column(db.Integer)
    Nothing = db.Column(db.Integer)
    Dance = db.Column(db.Integer)
    Memory = db.Column(db.Integer)
    Water = db.Column(db.Integer)
    Friend = db.Column(db.Integer)
    Pain = db.Column(db.Integer)
    Wait = db.Column(db.Integer)
    Link = db.Column(db.String)

# lists that will go into the drop-down options for album and year forms

with app.app_context():
    albums_query = db.session.query(Elliott.Album).distinct().order_by(Elliott.Album).all()
    albums_list = [(album.Album, album.Album) for album in albums_query]
    years_query = db.session.query(Elliott.Year).distinct().order_by(Elliott.Year).all()
    years_list = [(year.Year, year.Year) for year in years_query]

# form classes
       
class ThemeSelect(FlaskForm): # theme
    select = SelectField("Choose a keyword/theme:",
        choices=[
            ("Alcohol", "Alcohol"),
            ("City","City"),
            ("Dance", "Dance"),
            ("Death", "Death"),
            ("Dream", "Dream"),
            ("Friend", "Friend"),
            ("Home","Home"),
            ("Lie", "Lie"),
            ("Life", "Life"),
            ("Lonely","Lonely"),
            ("Lost","Lost"),
            ("Love","Love"),
            ("Memory","Memory"),
            ("Money","Money"),
            ("Nothing","Nothing"),
            ("Pain","Pain"),
            ("Sick","Sick"),
            ("Smoke","Smoke"),
            ("Time","Time"),
            ("Wait","Wait"),
            ("Water","Water")
        ]
    )
    submit = SubmitField("Submit")

class AlbumSelect(FlaskForm): # album
    select = SelectField("Choose an album:",
    choices=albums_list)
    submit = SubmitField("Submit")

class YearSelect(FlaskForm): # year
    select = SelectField("Choose a year:",
    choices=years_list)
    submit = SubmitField("Submit")

class SongSelect(FlaskForm): # song title
    title = StringField("Type a song title:")
    submit = SubmitField("Submit")

class LyricSelect(FlaskForm): # lyrics
    lyric = StringField("Type a song lyric:")
    submit = SubmitField("Submit")

#routes

@app.route('/')
def index():
    form = ThemeSelect()
    form2 = AlbumSelect()
    form3 = YearSelect()
    form4 = SongSelect()
    form5 = LyricSelect()
    return render_template('index.html',form=form,form2=form2,form3=form3,form4=form4,form5=form5)


# theme routes ----

@app.route('/theme', methods=['POST'])
def theme_detail():
    theme = request.form['select']
    return redirect(url_for('theme_results',theme=theme))

@app.route('/theme/results')
def theme_results():
    theme = request.args.get('theme')
    if not theme:
        return render_template('404.html', message="No keyword provided."), 404

    column_attr = getattr(Elliott, theme, None)
    if column_attr is None:
        return render_template('404.html', message=f"Keyword '{theme}' is not valid."), 404

    songs = db.session.query(Elliott).filter(column_attr == 1).all()
    if not songs:
        return render_template('404.html', message=f"No songs found for keyword: {theme}"), 404

    return render_template('songlist.html', theme=theme, songs=songs, origin='theme', value=theme)


# album routes ----

@app.route('/album', methods=['POST'])
def album_detail():
    album = request.form['select']
    return redirect(url_for('album_results',album = album))

@app.route('/album/results')
def album_results():
    album = request.args.get('album')
    songs = db.session.query(Elliott).filter(Elliott.Album == album).order_by(Elliott.Index).all()
    if not songs:
        return render_template('404.html')
    return render_template('songlist.html', album=album, songs=songs, origin='album', value=album)

# year routes ----

@app.route('/year', methods=['POST'])
def year_detail():
    year = request.form['select']
    return redirect(url_for('year_results',year=year))

@app.route('/year/results')
def year_results():
    year = request.args.get('year')
    songs = db.session.query(Elliott).filter(Elliott.Year == year).all()
    if not songs:
        return render_template('404.html')
    return render_template('songlist.html', year=year, songs=songs, origin='year', value=year)


# title routes ----

@app.route('/title',methods=['GET','POST'])
def song_detail():
    titles = request.form['title']

    if not titles:
        form = ThemeSelect()
        form2 = AlbumSelect()
        form3 = YearSelect()
        form4 = SongSelect()
        form5 = LyricSelect()
        message = f"Please enter a song title."
        return render_template('index.html', form=form, form2=form2, form3=form3,
                               form4=form4, form5=form5, titles=titles,
                               message=message)

    return redirect(url_for('song_results',titles=titles))

@app.route('/title/results')
def song_results():
    titles = request.args.get('titles')
    if not titles:
        return render_template('404.html')
    songs = db.session.query(Elliott).filter(Elliott.Title.ilike(f"%{titles}%")).all()

    if not songs:
        form = ThemeSelect()
        form2 = AlbumSelect()
        form3 = YearSelect()
        form4 = SongSelect()
        form5 = LyricSelect()
        message = f"No song titles found."
        return render_template('index.html', form=form, form2=form2, form3=form3,
                               form4=form4, form5=form5, titles=titles,
                               message=message)

    return render_template('songlist.html', titles=titles, songs=songs, origin='title', value=titles)

# lyric routes ----

@app.route('/lyric',methods=['GET','POST'])
def lyric_detail():
    lyrics = request.form['lyric']
        
    if not lyrics:
        form = ThemeSelect()
        form2 = AlbumSelect()
        form3 = YearSelect()
        form4 = SongSelect()
        form5 = LyricSelect()
        message2 = f"Please enter lyrics."
        return render_template('index.html', form=form, form2=form2, form3=form3,
                               form4=form4, form5=form5, message2=message2)
    return redirect(url_for('lyric_results',lyrics=lyrics))

@app.route('/lyric/results')
def lyric_results():
    lyrics = request.args.get('lyrics')
    if not lyrics:
        return render_template('404.html')
    lyrics_input = lyrics.strip().lower()

    songs = db.session.query(Elliott).filter(
        func.lower(func.replace(Elliott.Lyrics, '\n', ' ')).like(f"%{lyrics_input}%")
    ).all()

    if not songs:
        form = ThemeSelect()
        form2 = AlbumSelect()
        form3 = YearSelect()
        form4 = SongSelect()
        form5 = LyricSelect()
        message2 = f"No lyrics found."
        return render_template('index.html', form=form, form2=form2, form3=form3,
                               form4=form4, form5=form5, message2=message2)
    
    return render_template('songlist.html', lyrics=lyrics, songs=songs, origin='lyrics', value=lyrics)

# route for individual song details page

@app.route('/song/<int:song_id>')
def song_page(song_id):
    origin = request.args.get('origin')
    value = request.args.get('value')
    song = Elliott.query.get_or_404(song_id)
    return render_template('songdetail.html', song=song, origin=origin, value=value)

# route for about page

@app.route('/about')
def about():
    return render_template('about.html')

# error handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=True)