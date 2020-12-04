from flask import Flask,url_for,render_template,redirect,request,jsonify,flash,session,get_flashed_messages
from werkzeug.utils import secure_filename
import sqlite3
import json
import os

from mutagen.id3 import ID3, TIT2
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key='Nigeria\'s First Music Library'
csrf.init_app(app)

# app.WTF_CSRF_SECRET_KEY="crazy protecion"
# csrf = CSRFProtect(app)
# app.WTF_CSRF_SECRET_KEY="crazy protecion"

# Create a directory in a known location to save files to.
uploads_dir_song = os.path.join('static/songs')
uploads_dir_image = os.path.join('static/album-art')
# My Profle Details
conn=sqlite3.connect("fmuzic.db")
cursor=conn.cursor()
data=cursor.execute("SELECT * from profile")
profiles=data.fetchone()


#Index page
@app.route("/",methods=["POST","GET"])
def index():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	data=c.execute("SELECT rowid,* from music where trending='yes' LIMIT 8")
	return render_template("index.html",data=data)
#Index page
@app.route("/<artist>",methods=["POST","GET"])
def direct_link(artist):
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE artistname=? COLLATE NOCASE",(artist,))
	data=c.fetchall()
	if len(data)==0:
		return render_template("404.html")
	else:
		return render_template("artist_list.html",data=data)
#Genre page
@app.route("/genre",methods=["POST","GET"])
def genre():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	data=c.execute("SELECT rowid,* from genre")
	return render_template("genre.html",data=data)
#Genre list page
@app.route("/genre/<genre>",methods=["POST","GET"])
def genre_list(genre):
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE genrename=? COLLATE NOCASE",(genre,))
	result=c.fetchall()
	if len(result)==0:
		return render_template("404.html")
	else:
		return render_template("genre_list.html",result=result)
#Artist page
@app.route("/artist",methods=["POST","GET"])
def artist():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	data=c.execute("select rowid,* from artist")
	return render_template("playlist.html",data=data)
# Singe Artist page
@app.route("/artist/<artist>",methods=["POST","GET"])
def playlist(artist):
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE artistname=? COLLATE NOCASE",(artist,))
	data=c.fetchall()
	if len(data)==0:
		return render_template("404.html")
	else:
		return render_template("artist_list.html",data=data)
	
#Song page
@app.route("/songs",methods=["POST","GET"])
def songs():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	data=c.execute("SELECT rowid,* from music")
	return render_template("song.html",data=data)
#Song list page
@app.route("/songs/<songIds>",methods=["POST","GET"])
def single_song(songIds):
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music WHERE rowid=?",(songIds,))
	result=c.fetchall()
	if len(result)==0:
		return render_template("404.html")
	else:
		return render_template("single_song.html",result=result)
#Song list page
@app.route("/sation",methods=["POST","GET"])
def single_song_action():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music WHERE rowid=?",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Artist playlist page
@app.route("/sartist",methods=["POST","GET"])
def single_artist_action():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music WHERE artistname=? COLLATE NOCASE",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Genre playlist page
@app.route("/sgenre",methods=["POST","GET"])
def single_genre_action():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music WHERE genrename=? COLLATE NOCASE",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Artist Artist page
@app.route("/searchartist",methods=["POST","GET"])
def artist_search():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM artist(?);",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#Song Search page
@app.route("/searchsong",methods=["POST","GET"])
def song_search():
	if request.method=='POST':
		value = request.form["value"]
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music(?);",(value,))
		return jsonify(result.fetchall())
	return "You are allowed to be here"
#login page
@app.route("/admin",methods=["POST","GET"])
def admin():
	if 'username' in session:
		return redirect(url_for('dashboard'))
	else:
		if request.method=='POST':
			username = request.form["username"]
			password= request.form["pwd"]
			conn=sqlite3.connect("fmuzic.db")
			c=conn.cursor()
			c.execute("SELECT count(*) FROM profile WHERE email=? and password=?",(username,password))
			check=c.fetchone()
			if check[0]==1:
				session['username']=username
				return redirect(url_for('dashboard'))
			else:
				flash('Invalid Login credentail')
				return redirect(url_for('admin'))
		return render_template("login.html")

#login page
@app.route("/logout",methods=["POST","GET"])
def logout():
	session.pop('username',None)


	return redirect(url_for("admin"))
#Admin page
@app.route("/dashboard",methods=["POST","GET"])
def dashboard():
	if 'username' in session:
		conn=sqlite3.connect("fmuzic.db")
		# Count the data in databse
		cursor2=conn.cursor()
		cursor2.execute("SELECT count(*) from music UNION ALL SELECT count(*) from genre UNION ALL SELECT count(*) from artist")
		counts=cursor2.fetchall()
		return render_template("admin.html",profile=profiles,counts=counts)
	else:
		return redirect(url_for("admin"))
#Count
# @app.route("/count",methods=["POST","GET"])
# def count():

# 	conn=sqlite3.connect("fmuzic.db")
# 	c=conn.cursor()
# 	c.execute("SELECT count(*) from music UNION ALL SELECT count(*) from genre UNION ALL SELECT count(*) from artist")
# 	data=c.fetchall()
# 	return jsonify(data=data)

#Profile page
@app.route("/profile",methods=["POST","GET"])
def profile():
	if 'username' in session:
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT * FROM profile")
		return render_template("profile.html",result=result)
	else:
		return redirect(url_for("admin"))


# Profile Update
@app.route('/profile-update', methods=['GET', 'POST'])
def profile_update():
	if request.method=='POST':
		name=request.form["name"]
		email=request.form["mail"]
		password=request.form["pwd"]
		phone=request.form["num"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		if image.filename=='':
			c.execute("UPDATE profile SET fullname=?, email=?, password=?, phone=?", (name,email,password,phone))
			conn.commit()
			return redirect(url_for("profile"))
		else:
	# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
			c.execute("UPDATE profile SET fullname=?, email=?, password=?, phone=?, pix=?", (name,email,password,phone,image_link))
			conn.commit()
			return redirect(url_for("profile"))
	return redirect(url_for("profile"))
#Song table page
@app.route("/song-table",methods=["POST","GET"])
def songs_table():
	if 'username' in session:
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM music")
		return render_template("basic-table.html",result=result,profile=profiles)
	else:
		return redirect(url_for("admin"))
#Song table post page
@app.route("/song-post",methods=["POST","GET"])
def songs_post():
	if request.method=='POST':
		artist=request.form["artist"]
		title=request.form["title"]
		link=request.files["song"]
		duration=request.form["duration"]
		genre=request.form["genre"]
		description=request.form["description"]
		trending=request.form["trend"]
		image=request.files["image"]
# save song
		song_link=secure_filename(link.filename)
		link.save(os.path.join(uploads_dir_song, secure_filename(link.filename)))
# save image
		image_link=secure_filename(image.filename)
		image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		c.execute("INSERT INTO music(artistname,title,song,duration,genrename,description,trending,image) VALUES(?,?,?,?,?,?,?,?)",(artist,title,song_link,duration,genre,description,trending,image_link))
		c.execute("UPDATE artist set total=total+1 where name=?",(artist,))
		c.execute("UPDATE genre set total=total+1 where name=?",(genre,))
		conn.commit()
		return redirect(url_for("songs_table"))
	return"Not allowed"
#Song table update page
@app.route("/song-update/<string>",methods=["POST","GET"])
def songs_update(string):
	if request.method=='POST':
		artist=request.form["artist"]
		title=request.form["title"]
		link=request.files["song"]
		duration=request.form["duration"]
		genre=request.form["genre"]
		description=request.form["description"]
		trending=request.form["trend"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		if link.filename=='' and image.filename !='':
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Delete Previous Image
			data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			for row in data:
				os.remove(os.path.join(uploads_dir_image, secure_filename(row[8])))
			c.execute("UPDATE music SET artistname=?, title=?, duration=?, genrename=?, description=?, trending=?, image=? WHERE rowid=?", (artist,title,duration,genre,description,trending,image_link,string))
			conn.commit()
			return redirect(url_for("songs_table"))

		elif image.filename=='' and link.filename !='':
			song_link=secure_filename(link.filename)
			link.save(os.path.join(uploads_dir_song, secure_filename(link.filename)))
			data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			for row in data:
				os.remove(os.path.join(uploads_dir_song, secure_filename(row[3])))
			c.execute("UPDATE music SET artistname=?, title=?, song=?, duration=?, genrename=?, description=?, trending=? WHERE rowid=?", (artist,title,song_link,duration,genre,description,trending,string))
			conn.commit()
			return redirect(url_for("songs_table"))
		
		elif image.filename=='' and link.filename=='':
			c.execute("UPDATE music SET artistname=?, title=?, duration=?, genrename=?, description=?, trending=? WHERE rowid=?", (artist,title,duration,genre,description,trending,string))
			conn.commit()
			return redirect(url_for("songs_table"))

		else:
	# save song
			song_link=secure_filename(link.filename)
			link.save(os.path.join(uploads_dir_song, secure_filename(link.filename)))
	# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
			data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
			for row in data:
				os.remove(os.path.join(uploads_dir_image, secure_filename(row[8])))
				os.remove(os.path.join(uploads_dir_song, secure_filename(row[3])))
			c.execute("UPDATE music SET artistname=?, title=?, duration=?, genrename=?, description=?, trending=? WHERE rowid=?", (artist,title,duration,genre,description,trending,string))
			conn.commit()
			return redirect(url_for("songs_table"))
	return"Not allowed"
#Song table delete page
@app.route("/song-delete/<string>",methods=["POST","GET"])
def songs_delete(string):
	if request.method=='POST':
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		data=c.execute("SELECT rowid,* FROM music where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[8])))
			os.remove(os.path.join(uploads_dir_song, secure_filename(row[3])))
		c.execute("DELETE  FROM music where rowid=?",(string,))
		c.execute("UPDATE artist set total=total-1 where name=?",(row[1],))
		c.execute("UPDATE genre set total=total-1 where name=?",(row[5],))
		conn.commit()
		return redirect(url_for("songs_table"))
	return redirect(url_for("songs_table"))
# Artist page
@app.route("/artist-table",methods=["POST","GET"])
def artist_table():
	if 'username' in session:
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM artist")
		return render_template("artist-table.html",result=result,profile=profiles)
	else:
		return redirect(url_for("admin"))


# #artist table post page
@app.route("/artist-post",methods=["POST","GET"])
def artists_post():
	if request.method=='POST':
		artist=request.form["artist"]
		image=request.files["image"]
# save image
		image_link=secure_filename(image.filename)
		image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		c.execute("INSERT INTO artist(name,image) VALUES(?,?)",(artist,image_link))
		conn.commit()
		return redirect(url_for("artist_table"))
	return redirect(url_for("artist_table"))

# #Song table update page
@app.route("/artist-update/<string>",methods=["POST","GET"])
def artists_update(string):
	if request.method=='POST':
		artist=request.form["artist"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		if image.filename=='':
			c.execute("UPDATE artist SET name=? WHERE rowid=?", (artist,string))
			conn.commit()
			return redirect(url_for("artist_table"))
		else:
# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Delete Previous Image
			data=c.execute("SELECT rowid,* FROM artist where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))
# Update New data
			c.execute("UPDATE artist SET name=?, image=? WHERE rowid=?", (artist,image_link,string))
			conn.commit()
			return redirect(url_for("artist_table"))
	redirect(url_for("artist_table"))

# #Song table delete page
@app.route("/artist-delete/<string>",methods=["POST","GET"])
def artists_delete(string):
	if request.method=='POST':
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		data=c.execute("SELECT rowid,* FROM artist where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))
		c.execute("DELETE  FROM artist where rowid=?",(string,))
		conn.commit()
		return redirect(url_for("artist_table"))
	return redirect(url_for("artist_table"))

#Genre page
@app.route("/genre-table",methods=["POST","GET"])
def genre_table():
	if 'username' in session:
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		result=c.execute("SELECT rowid,* FROM genre")
		return render_template("genre-table.html",result=result,profile=profiles)
	else:
		return redirect(url_for("admin"))

#Song table post page
@app.route("/genre-post",methods=["POST","GET"])
def genre_post():
	if request.method=='POST':
		genre=request.form["genre"]
		image=request.files["image"]
# save image
		image_link=secure_filename(image.filename)
		image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		c.execute("INSERT INTO genre(genre,image) VALUES(?,?)",(genre,image_link))
		conn.commit()
		return redirect(url_for("genre_table"))
	return redirect(url_for("genre_table"))
# #Song table update page
@app.route("/genre-update/<string>",methods=["POST","GET"])
def genre_update(string):
	if request.method=='POST':
		genre=request.form["genre"]
		image=request.files["image"]
		# Connect to database
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		if image.filename=='':
			c.execute("UPDATE genre SET genre=? WHERE rowid=?", (genre,string))
			conn.commit()
			return redirect(url_for("genre_table"))
		else:
	# save image
			image_link=secure_filename(image.filename)
			image.save(os.path.join(uploads_dir_image, secure_filename(image.filename)))
# Delete Previous Image
			data=c.execute("SELECT rowid,* FROM genre where rowid=?",(string,))
			for row in data:
				os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))

			c.execute("UPDATE genre SET genre=?, image=? WHERE rowid=?", (genre,image_link,string))
			conn.commit()
			return redirect(url_for("genre_table"))
	redirect(url_for("genre_table"))

# #Song table delete page
@app.route("/genre-delete/<string>",methods=["POST","GET"])
def genre_delete(string):
	if request.method=='POST':
		conn=sqlite3.connect("fmuzic.db")
		c=conn.cursor()
		data=c.execute("SELECT rowid,* FROM genre where rowid=?",(string,))
		for row in data:
			os.remove(os.path.join(uploads_dir_image, secure_filename(row[3])))
		c.execute("DELETE  FROM genre where rowid=?",(string,))
		conn.commit()
		return redirect(url_for("genre_table"))
	return redirect(url_for("genre_table"))
	
# Error handler
# @app.errorhandler(404)
# def error (e):

# 	return render_template('404.html')
# @app.errorhandler(500)
# def internal_server_error(e):
# 	return "internal server error", 50
@app.route('/test')
def test():
	title = "be still hillsong worship"
	artist = " new worship"
	audio_path="static/songs/be_still_hillsong_worship_mp3_35587.mp3"
	picture_path="static/album-art/sam.jpg"
# Save song details
	audio = EasyID3(audio_path)
	audio["title"]=title
	audio["artist"]=artist
	audio["genre"]=u"worship"
	audio["lyricist"]=u"this is lyrics"
	audio["composer"]=u"Musixcloud"
	audio["copyright"]=u"Musixcloud reserve no right to copyright of songs, please refer to artist for copyright poliy"
	audio["website"]=u"musixcloud.com"
	audio.save()
# Add album art
	audio_cover =  MP3(audio_path, ID3=ID3)
	audio_cover.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(picture_path,'rb').read()))
	audio_cover.save()
	test = audio_cover.pprint()


	return jsonify(test)
# Musixcloud App apis
# Songs
@app.route('/v1/api/songs')
def songs_api():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music")
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"http://127.0.0.1:5000/static/album-art/"+row[8],
			"url": "http://127.0.0.1:5000/static/songs/"+row[3],
			"description":row[6],
			"duration":row[3],
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# Genre Songs
@app.route('/v1/api/genre/<genre>')
def genresong_api(genre):
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music where genrename=?",(genre,))
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"http://127.0.0.1:5000/static/album-art/"+row[8],
			"url": "http://127.0.0.1:5000/static/songs/"+row[3],
			"description":row[6],
			"duration":row[3],
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# Genre Songs
@app.route('/v1/api/artist/<name>')
def artistsong_api(name):
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM music where artistname=?",(name,))
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"http://127.0.0.1:5000/static/album-art/"+row[8],
			"url": "http://127.0.0.1:5000/static/songs/"+row[3],
			"description":row[6],
			"duration":row[3],
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# Genre Songs
@app.route('/v1/api/artist')
def artistlist_api():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* FROM artist")
	result=c.fetchall()
	artist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"image":"http://127.0.0.1:5000/static/album-art/"+row[3]
		}
		artist.append(mydic)
	return jsonify(artist)
# Trending Songs
@app.route('/v1/api/songs/trending')
def songstrend_api():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("select rowid,* from music ORDER by count + like + downloads DESC LIMIT 10")
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"http://127.0.0.1:5000/static/album-art/"+row[8],
			"url": "http://127.0.0.1:5000/static/songs/"+row[3],
			"description":row[6],
			"duration":row[3],
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
# New Songs
@app.route('/v1/api/songs/new')
def songsnew_api():
	conn=sqlite3.connect("fmuzic.db")
	c=conn.cursor()
	c.execute("SELECT rowid,* from music ORDER by ROWID DESC LIMIT 10")
	result=c.fetchall()
	songlist = []
	for row in result:
		mydic={
			"id":row[0],
			"artist":row[1],
			"title":row[2],
			"image":"http://127.0.0.1:5000/static/album-art/"+row[8],
			"url": "http://127.0.0.1:5000/static/songs/"+row[3],
			"description":row[6],
			"duration":row[3],
			"genre":row[5]
		}
		songlist.append(mydic)
	return jsonify(songlist)
if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug=True)