from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User, Feedback
from form import AddUser, LoginForm, AddFeedback



app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECT'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
debug = DebugToolbarExtension(app)

connect_db(app)



@app.route('/')
def index():
    print(session)
    print(session.get('user_id', 'empty'))
    if 'user_id' in session:
        user_id =session['user_id']
        return render_template('home.html', user_id=user_id)


    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form=AddUser()
    print(dir(form))
    print(form.data)   
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        new_registered_user = User.register(username,password,email,first_name,last_name)
        db.session.add(new_registered_user)
        db.session.commit()
        session['user_id'] = new_registered_user.id
        return redirect(f'/users/{new_registered_user.id}')

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user =User.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            return redirect(f'/users/{user.id}')
        else:
            flash('you entered wrong credentials')
            return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



@app.route('/secret')
def secret():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/login')
    user =User.query.filter_by(id = session['user_id']).first()
    return render_template('secret.html', user=user)


@app.route('/users/<int:user_id>')
def user_profile(user_id):
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/login')
    user=User.query.filter_by(id=user_id).first()
    # the feedbacks relationship returns an array
    feedbacks=user.feedbacks
    print(feedbacks)
    return render_template('user-info.html', user=user, feedbacks=feedbacks)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/login')
    form=AddFeedback()
    feedbacks=Feedback.query.all()
    user=User.query.filter_by(id=session['user_id']).first()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data 
        new_feedback=Feedback(title=title, content=content, username=user.username)
        db.session.add(new_feedback)
        db.session.commit()
        print(new_feedback)
        print(new_feedback.username)
        return redirect('/feedback')


    return render_template('feedback.html', form=form, feedbacks=feedbacks, user=user)


@app.route('/feedback/delete/<int:feed_id>')
def delete_feedback(feed_id):
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/login')
    feedback=Feedback.query.get(feed_id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect('/feedback')


@app.route('/user/delete')
def delete_user():
    if 'user_id' not in session:
        flash('Please Login')
        return redirect('/login')
    user=User.query.get(session['user_id'])
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
