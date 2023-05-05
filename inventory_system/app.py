from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Your models go here
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=True)
    quality = db.Column(db.String(100), nullable=True)
    item_type = db.Column(db.String(100), nullable=True)
    item_slot = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    stackable = db.Column(db.Boolean, nullable=True)
    unique_amount = db.Column(db.Integer, nullable=True)
    soulbind = db.Column(db.Boolean, nullable=True)
    sell_price = db.Column(db.Float, nullable=True)
    buy_price = db.Column(db.Float, nullable=True)
    spell_ids = db.Column(db.String(255), nullable=True)
    spell_charges = db.Column(db.String(255), nullable=True)
    spell_cooldowns = db.Column(db.String(255), nullable=True)
    spell_category_cooldowns = db.Column(db.String(255), nullable=True)
    spell_categories = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(500), nullable=True)

# Your routes go here
@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    new_item = Item(name=item_name)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
