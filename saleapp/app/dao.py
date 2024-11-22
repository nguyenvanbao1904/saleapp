from app.models import Category, Product, User
from app import app, models, db
import hashlib


def load_categories():
    return Category.query.order_by('id').all()


def load_products(cate_id=None, kw=None, page = None):
    query = Product.query
    if page is None:
        page = 1
    page = int(page)
    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    start = (page - 1) * app.config['PAGE_SIZE'] + 1
    return query.offset(start).limit(app.config['PAGE_SIZE']).all()

def count_products():
    return Product.query.count()

def auth_user(username, password):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(data):
    data['password'] = hashlib.md5(data['password'].strip().encode('utf-8')).hexdigest()
    user = models.User(**data)
    db.session.add(user)
    db.session.commit()

