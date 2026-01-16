from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
#from werkzeug.utils import secure_filename
from datetime import datetime, date
#import qrcode
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tailor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)


def generate_unique_id(prefix, model, column):
    """Generate a unique ID with the given prefix."""
    last_user = model.query.order_by(column.desc()).first()
    if last_user:
        last_id = getattr(last_user, column.name)
        number = int(last_id.replace(prefix, '')) + 1
    else:
        number = 1
    return f"{prefix}{number}"


#***************************Models*******************
class User(db.Model):
    id  = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String(20), unique=True, nullable=False)
    userName = db.Column(db.String(20),nullable=False)
    phone = db.Column(db.String(20),nullable=False)
    numberOfSuit = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    date = db.Column(db.Date,nullable=False)
#***************************Shalwar*****************************
    width = db.Column(db.String(20),nullable=False)
    height = db.Column(db.String(20),nullable=False)
    arm = db.Column(db.String(20),nullable=False)
    color = db.Column(db.String(20),nullable=False)
    pocket = db.Column(db.String(20),nullable=False)
    frontPocket = db.Column(db.String(20),nullable=False)
    chestWidth = db.Column(db.String(20),nullable=False)
    daman = db.Column(db.String(20),nullable=False)
#**************************Kameeeas******************************
    height = db.Column(db.String(20),nullable=False)
    width = db.Column(db.String(20),nullable=False)
    pocket = db.Column(db.String(20),nullable=False)


# Create Database 
with app.app_context():
    db.create_all()



# ************************************Routes*****************************************************
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user')
def user():
    all_users = User.query.all()
    return render_template('user.html', users=all_users)

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        try:
            userId = generate_unique_id('ab',User,User.userId)
            userName = request.form['Customer Name']
            phone = request.form['Phone Number']
            numberOfSuit = request.form['Number Of Suit']
            address = request.form['Address']
            date = datetime.strptime(request.form['Date'],'%d-%m-%Y').date()
            width = request.form['Width']
            height = request.form['Height']
            arm = request.form['Arm']
            color = request.form['Color']
            pocket = request.form['Pocketr']
            frontPocket = request.form['Front Pocket']
            chestWidth = request.form['Chest Width']
            daman = request.form['Daman']
            ####kameeeas Data check and change accordingly 
            # height = request.form['Height kamees']
            # width = request.form['Width Kamees']
            # pocket = request.form['Pocket Kamees']


            new_user = User(
                userId = userId,
                userName = userName,
                phone = phone,
                numberOfSuit = numberOfSuit,
                date = date,
                address = address ,
                width=width,
                height=height,
                arm = arm,
                color = color,
                pocket = pocket,
                frontPocket = frontPocket,
                chestWidth = chestWidth,
                daman = daman,
                # height = height,
                # width = width ,
                # pocket = pocket
                #let us check the name and then we will change this too beacues it become two time with same name 

                
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Customer Added Successfully!','Success')
            return redirect('/user')
        except Exception as e:
            flash(f"Error:{str(e)}", 'Danger')
    return render_template('add_user.html')

@app.route('/updateCustomer', methods=['GET', 'POST'])
def update_user():
    customer = None
    error = None
    
    if request.method == 'POST':
        search_id = request.form.get('search_id', '').strip()
        if not search_id:
            error = "Please enter a Customer ID"
        else:
            customer = User.query.filter_by(userId=search_id).first()
            if not customer:
                error = f"Customer with ID '{search_id}' not found"
    
    return render_template('updateCustomer.html', customer=customer, error=error)

@app.route('/updateCustomer_submit', methods=['POST'])
def update_user_submit():
    try:
        customer_id = request.form.get('customer_id')
        customer = User.query.get(customer_id)
        
        if not customer:
            flash("Customer not found", 'Danger')
            return redirect('/updateCustomer')
        
        customer.userName = request.form['Customer Name']
        customer.phone = request.form['Phone Number']
        customer.numberOfSuit = request.form['Number Of Suit']
        customer.address = request.form['Address']
        customer.date = datetime.strptime(request.form['Date'], '%d-%m-%Y').date()
        customer.width = request.form['Width']
        customer.height = request.form['Height']
        customer.arm = request.form['Arm']
        customer.color = request.form['Color']
        customer.pocket = request.form['Pocketr']
        customer.frontPocket = request.form['Front Pocket']
        customer.chestWidth = request.form['Chest Width']
        customer.daman = request.form['Daman']
        
        db.session.commit()
        flash('Customer Updated Successfully!', 'Success')
        return redirect('/user')
    except Exception as e:
        flash(f"Error: {str(e)}", 'Danger')
        return redirect('/updateCustomer')

@app.route('/deleteCustomer', methods=['GET', 'POST'])
def delete_customer():
    customer = None
    error = None
    
    if request.method == 'POST':
        search_id = request.form.get('search_id', '').strip()
        if not search_id:
            error = "Please enter a Customer ID"
        else:
            customer = User.query.filter_by(userId=search_id).first()
            if not customer:
                error = f"Customer with ID '{search_id}' not found"
    
    return render_template('deleteCustomer.html', customer=customer, error=error)

@app.route('/deleteCustomer_submit', methods=['POST'])
def delete_customer_submit():
    try:
        customer_id = request.form.get('customer_id')
        customer_userId = request.form.get('customer_userId')
        customer = User.query.get(customer_id)
        
        if not customer:
            flash("Customer not found", 'Danger')
            return redirect('/deleteCustomer')
        
        db.session.delete(customer)
        db.session.commit()
        
        return render_template('deleteCustomer.html', success=True, customer_id=customer_userId)
    except Exception as e:
        flash(f"Error: {str(e)}", 'Danger')
        return redirect('/deleteCustomer')

if __name__ == '__main__':
    app.run(debug=True)
#The following code is about to add measurment no sure is it at all according to talior system but i haven't check and run code i have added sectio too 
# let me run the code and add fucntiolaty like upadate and delete button in this where update will work to update the user data and delete you know 