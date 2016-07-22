from system.core.model import Model

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()

    def get_recent_reviews(self):
    	#get 3 latest reviews
    	query = 'SELECT books.title, reviews.rating, users.alias, reviews.review, reviews.created_at, reviews.book_id AS book_id, reviews.user_id AS user_id FROM reviews JOIN users ON reviews.user_id = users.id JOIN books ON reviews.book_id = books.id ORDER BY reviews.created_at DESC LIMIT 3'
    	reviews = self.db.query_db(query)
    	return reviews

    def get_books(self):
    	query = 'SELECT * FROM books'
    	books = self.db.query_db(query)
    	return books

    def create_book(self, info, id):
    	book_query = 'INSERT INTO books (title, author, created_at, updated_at) VALUES (:title, :author, NOW(), NOW())'
    	book_data = {
    		'title': info['title'],
    		'author': info['author']
    	}
    	self.db.query_db(book_query, book_data)
    	get_book_query = 'SELECT * FROM books ORDER BY created_at DESC LIMIT 1'
    	books = self.db.query_db(get_book_query)
    	book = books[0]

    	review_query = 'INSERT INTO reviews (review, rating, created_at, updated_at, book_id, user_id) VALUES (:review, :rating, NOW(), NOW(), :book_id, :user_id)'
    	review_data = {
    		'review': info['review'],
    		'rating': info['rating'],
    		'book_id': book['id'],
    		'user_id': id
    	}
    	self.db.query_db(review_query, review_data)
    	return book

    def get_book_by_id(self, id):
    	query = 'SELECT * FROM books WHERE id=:id'
    	data = {'id': id}
    	books = self.db.query_db(query, data)
    	return books[0]

    def get_reviews_for_book(self, id):
    	query = 'SELECT reviews.rating, users.alias, reviews.review, reviews.created_at, users.id AS user_id, reviews.id AS review_id FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.book_id = :id ORDER BY reviews.created_at DESC'
    	data = {'id': id}
    	reviews = self.db.query_db(query, data)
    	return reviews

    def destroy(self, id):
    	query = 'DELETE FROM reviews WHERE id=:id'
    	data = {'id': id}
    	return self.db.query_db(query, data)

    def create_review(self, info):
    	query = 'INSERT INTO reviews (review, rating, created_at, updated_at, book_id, user_id) VALUES (:review, :rating, NOW(), NOW(), :book_id, :user_id)'
    	data = {'review': info['review'], 'rating': info['rating'], 'book_id': info['book_id'], 'user_id': info['user_id']}
    	return self.db.query_db(query, data)

    def get_reviews_count(self, id):
    	#id refers to user id
    	query = 'SELECT users.alias, users.name, users.email, COUNT(reviews.user_id) as review_count FROM users JOIN reviews ON reviews.user_id = users.id WHERE users.id=:id GROUP BY reviews.user_id'
    	data = {'id': id}
    	reviews = self.db.query_db(query, data)
    	return reviews[0]

    def get_books_for_user(self, id):
    	#id refers to user id
    	query = 'SELECT books.title, books.id FROM books JOIN reviews ON reviews.book_id = books.id JOIN users ON reviews.user_id = users.id WHERE users.id=:id'
    	data = {'id': id}
    	return self.db.query_db(query, data)



