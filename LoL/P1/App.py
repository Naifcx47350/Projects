from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
DB = SQLAlchemy()
DB_NAME = 'database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

DB.init_app(app)


class Todo(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(200), nullable=False)
    data_created = DB.Column(DB.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def hello_world():
    print("Hello World")
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
