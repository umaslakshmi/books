"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Book')
        self.db = self._app.db

    def index(self):
        if 'id' in session:
            return redirect('/books/home')
        return self.load_view('/users/index.html')

    def login(self):
        print request.form
        info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        result = self.models['User'].check_user(info)
        if result:
            session['id'] = result['id']
            return redirect('/books/home')
        else:
            flash("Invalid email or password", 'login_errors')
            return redirect('/')

    def register(self):
        print request.form
        info = {
            'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_password': request.form['confirm-password']
        }
        result = self.models['User'].create_user(info)
        if result['status']:
            session['id'] = result['user']['id']
            return redirect('/books/home')
        else:
            for error in result['errors']:
                flash(error, 'regis_errors')
            return redirect('/')

    def logout(self):
        session.pop('id')
        return redirect('/')

    def show(self, id):
        result = self.models['Book'].get_reviews_count(id)
        books = self.models['Book'].get_books_for_user(id)
        return self.load_view('/users/show.html', user=result, books=books)
