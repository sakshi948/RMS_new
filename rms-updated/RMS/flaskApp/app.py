from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)

app.secret_key = "super key"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "RMS"


mysql = MySQL(app)


# @app.route('/login')
# def hello():
#     return render_template('AuthorDetails.htm')
@app.route('/')
@app.route('/static/project.html')
def project():
    return render_template('project.html')

# login


@app.route('/static/login.htm', methods=['Get', 'POST'])
def login():
    # print("hiiiiiiiiiiiiiiiii")
    msg = ""
    if request.method == 'POST':
        autor_id = request.form['ID']
        password = request.form['code']
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM login WHERE AUTHOR_ID=%s AND PASSWORD=%s', (autor_id, password))
        rec = cur.fetchone()
        if rec:
            session["loggedin"] = True
            session['author_id'] = rec[0]
            session['password'] = rec[1]
            session['author_name'] = rec[2]
            return redirect(url_for('static', filename='loginClick.html'))
        else:
            msg = "Incorrect username/password...TryAgain!!"
            print(msg)

    return render_template('login.htm')


# signUP
@app.route('/static/SignUP.html', methods=['GET', 'POST'])
def SignUP():
    if request.method == 'POST':
        # print("piiiiiiiiiiiiiiiiiiiiiiiiii")
        userDetails = request.form
        # print(userDetails)
        AUTHOR_ID = userDetails["AUTHOR_ID"]

        AUTHOR_NAME = userDetails["AUTHOR_NAME"]
        PASSWORD = userDetails["PASSWORD"]
        print(AUTHOR_ID)

        # print(name)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO LOGIN (AUTHOR_ID,AUTHOR_NAME,PASSWORD) VALUES(%s,%s,%s)",
                    (AUTHOR_ID,  AUTHOR_NAME, PASSWORD))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('static', filename='AuthorDetails.htm'))
        # return redirect ('{{url_for('static',filename = 'project.html')}}')

    print("hiiiiiiiiiiiiiiii")
    return render_template('SignUP.html')

# authordetails


@app.route('/static/AuthorDetails.htm', methods=['GET', 'POST'])
def hell():
    if request.method == 'POST':
        print("piiiiiiiiiiiiiiiiiiiiiiiiii")
        userDetails = request.form
        # print(userDetails)
        AUTHOR_ID = userDetails["AUTHOR_ID"]
        AUTHOR_NAME = userDetails["AUTHOR_NAME"]
        DEPARTMENT = userDetails["DEPARTMENT"]
        ROLE = userDetails["ROLE"]
        ID = userDetails["ID"]
        PHONE = userDetails["PHONE"]

        # print(name)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO AUTHORDETAILS (AUTHOR_ID,AUTHOR_NAME,DEPARTMENT,ROLE,ID,PHONE) VALUES(%s,%s,%s,%s,%s,%s)",
                    (AUTHOR_ID, AUTHOR_NAME, DEPARTMENT, ROLE, ID, PHONE))
        mysql.connection.commit()
        cur.close()
        return redirect('/')

    print("hiiiiiiiiiiiiiiii")
    return render_template('AuthorDetails.htm')


# dummy author details for deletion purpose
@app.route('/static/AuthorDetails1.html', methods=['GET', 'POST'])
def dummy():
    if request.method == 'POST':
        print("piiiiiiiiiiiiiiiiiiiiiiiiii")
        userDetails = request.form
        # print(userDetails)
        AUTHOR_ID = userDetails["AUTHOR_ID"]
        AUTHOR_NAME = userDetails["AUTHOR_NAME"]
        DEPARTMENT = userDetails["DEPARTMENT"]
        ROLE = userDetails["ROLE"]
        ID = userDetails["ID"]
        PHONE = userDetails["PHONE"]

        print(session['author_id'])

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM AUTHORDETAILS where Author_ID = %s",
                    (session['author_id'],))
        cur.execute("DELETE FROM login where Author_ID = %s",
                    (session['author_id'],))

        cur.execute("INSERT INTO AUTHORDETAILS (AUTHOR_ID,AUTHOR_NAME,DEPARTMENT,ROLE,ID,PHONE) VALUES(%s,%s,%s,%s,%s,%s)",
                    (AUTHOR_ID, AUTHOR_NAME, DEPARTMENT, ROLE, ID, PHONE))

        cur.execute("INSERT INTO LOGIN (AUTHOR_ID,AUTHOR_NAME,PASSWORD) VALUES(%s,%s,%s)",
                    (AUTHOR_ID,  AUTHOR_NAME, session['password']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('static', filename='profile.html'))

    return render_template('AuthorDetails1.html')

# Conference


@app.route('/static/conferences.html', methods=['GET', 'POST'])
def con():
    if request.method == 'POST':
        conDetails = request.form
        Citation = conDetails["Citation"]
        Author_ID = conDetails["Author_ID"]
        Conference_Title = conDetails["Conference_Title"]
        Name_of_Journal = conDetails["Name_of_Journal"]
        Date = conDetails["Date"]
        Publisher = conDetails["Publisher"]
        Page_No = conDetails["Page_No"]
        Year = conDetails["Year"]
        print("hayu")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO CONFERENCE (Citation,Author_ID,Conference_Title,Name_of_Journal,Date,Publisher,Page_No,Year) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (Citation, Author_ID, Conference_Title, Name_of_Journal, Date, Publisher, Page_No, Year))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('static', filename='profile.html'))
        # return redirect ('{{url_for('static',filename = 'project.html')}}')

    print("hiiiiiiiiiiiiiiii")
    return render_template('conferences.html')

# view conference


@app.route('/static/viewCon.html', methods=['Get', 'POST'])
def viewCon():
    cur = mysql.connection.cursor()
    value = cur.execute(
        'SELECT * FROM conference')
    if value > 0:
        details1 = cur.fetchall()
    return render_template('viewCon.html', userdata1=details1)

# view Journal


@app.route('/static/viewJou.html', methods=['Get', 'POST'])
def viewJou():
    cur = mysql.connection.cursor()
    value = cur.execute(
        'Select * FROM journal'
    )
    if value > 0:
        details2 = cur.fetchall()
    return render_template('viewJou.html', userdata2=details2)


# Journal
@app.route('/static/journal.html', methods=['GET', 'POST'])
def jou():
    if request.method == 'POST':
        jouDetails = request.form
        Citation = jouDetails["Citation"]
        Author_ID = jouDetails["Author_ID"]
        Name_of_Journal = jouDetails["Name_of_Journal"]
        Date = jouDetails["Date"]
        Publisher = jouDetails["Publisher"]
        Volume = jouDetails["Volume"]
        Year = jouDetails["Year"]
        # print("hayu")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO journal (Citation,Author_ID,Name_of_Journal,Date,Publisher,Volume,Year) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (Citation, Author_ID, Name_of_Journal, Date, Publisher, Volume, Year))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('static', filename='project.html'))
        # return redirect ('{{url_for('static',filename = 'project.html')}}')

    # print("hiiiiiiiiiiiiiiii")
    return render_template('journal.html')

# link login button with loginClick page


@app.route('/static/loginClick.html')
def loginClick():
    return render_template('loginClick.html', username=session['author_name'])

# link profile button with profile.html


@app.route('/static/profile.html', methods=['Get', 'POST'])
def profilebutton():
    id = session['author_id']
    print(id)
    cur = mysql.connection.cursor()
    value = cur.execute(
        'SELECT * FROM authordetails WHERE Author_ID=%s', (id,))
    if value > 0:
        details = cur.fetchall()
    return render_template('profile.html', userdata=details)
    # return render_template('profile.html', use=session['author_id'])


# for passing parameters from the url


@ app.route('/users')
def users():
    cur = mysql.connection.cursor()
    value = cur.execute("select * from authordetails")
    if value > 0:
        deatails = cur.fetchall()
        return render_template('user.html', userDetails=deatails)


if(__name__ == "__main__"):
    app.run(debug=True)
