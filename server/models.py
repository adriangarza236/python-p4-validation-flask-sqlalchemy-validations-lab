from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Failed to input name")
        elif db.session.query(Author).filter(Author.name == name).first():
            raise ValueError("Name must be unique")
        return name 
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits long")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validates_title(self, key, title):
        required_titles = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError("Must input title")
        elif not any(req in title for req in required_titles):
            raise ValueError("must be one of the required titles")
        return title
    
    
    @validates('content')
    def validates_content(self, key, content):
        if len(content) < 250:
            raise ValueError("content must be at least 250 characters long")
        return content
        
    @validates('summary')
    def validates_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("summary must be max 250 characters")
        return summary
    
    @validates('category')
    def validates_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("category must be Fiction or Non-Fiction") 



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
