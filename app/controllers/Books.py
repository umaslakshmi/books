from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)
        self.load_model('Book')
        self.load_model('User')
        self.db = self._app.db

    def home(self):
    	user = self.models['User'].get_user_by_id(session['id'])
    	reviews = self.models['Book'].get_recent_reviews()
    	books = self.models['Book'].get_books()
    	return self.load_view('/books/home.html', user=user, reviews=reviews, books=books)

    def add(self):
    	books = self.models['Book'].get_books()
    	return self.load_view('/books/new.html', books=books)

    def create_book(self):
    	print request.form
    	if len(request.form['author-2']) < 1:
    		author = request.form['author-1']
    	else:
    		author = request.form['author-2']
    	info = {
    		'title': request.form['title'],
    		'author': author,
    		'review': request.form['review'],
    		'rating': request.form['rating']
    	}
    	book = self.models['Book'].create_book(info, session['id'])
    	ret = '/books/{}'.format(book['id'])
    	return redirect(ret)

    def show(self, id):
    	book = self.models['Book'].get_book_by_id(id)
    	reviews = self.models['Book'].get_reviews_for_book(id)
    	return self.load_view('/books/show.html', book=book, reviews=reviews)

    def destroy(self, id):
    	self.models['Book'].destroy(id)
    	return redirect('/books/home')

    def create_review(self, id):
    	print request.form
    	info = {
    		'review': request.form['review'],
    		'rating': request.form['rating'],
    		'book_id': id,
    		'user_id': session['id']
    	}
    	self.models['Book'].create_review(info)
    	return redirect('/books/{}'.format(id))



