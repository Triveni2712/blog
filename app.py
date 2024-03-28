from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="system",database="codegnan")
with mysql.connector.connect(host="localhost",user="root",password="system",database="codegnan"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if  not exists register(username varchar(50) primary key,mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
app=Flask(__name__)
app.secret_key="my secret is too secret"
@app.route("/")
def home(): 
    return "Homepage of Bing"
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form.get('username')
        mobile=request.form.get('mobile')
        address=request.form.get('Address')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into register values(%s,%s,%s,%s,%s)',[username,mobile,address,email,password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from register where username=%s && password =%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return "Invalid username and password"
    return render_template("login.html")
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/addposts',methods=['GET','POST'])
def addposts():
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts(title,content,slug) VALUES(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id_):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM posts WHERE id=%s',(id,))
    mydb.commit
    cursor.close()
    return redirect(url_for('viewposts'))
@app.route('/update_post/<int:id>',methods=['GET','POST'])
def update_post():
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        cursor=mydb.cursor(buffered=True)
        cursor.execute('UPDATE posts SET title=%s,content=%s,slug=%s WHERE id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone
        cursor.close()
        return render_template('update.html',post=post)
app.run