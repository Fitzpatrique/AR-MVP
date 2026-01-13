# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_python_static_files]
import logging
from flask_cors import CORS
import hashlib, os, sqlite3
from werkzeug.utils import secure_filename
from flask import *
import key_config as keys
import json
import string
import random
import datetime
from datetime import timedelta
import boto3

SECRET_KEY = keys.SECRET_KEY
PUBLIC_KEY = keys.PUBLIC_KEY


UPLOAD_FOLDER = 'static/uploads'
ASSET_FOLDER = 'static/assets'
ALLOWED_EXTENSIONS = ['jpeg', 'jpg', 'png', 'gif']
ALLOWED_ASSET_EXTENSIONS = ['glb', 'usdz']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ASSET_FOLDER'] = ASSET_FOLDER

CORS(app)

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    region_name='eu-west-2')#aws_session_token=keys.AWS_SESSION_TOKEN

from boto3.dynamodb.conditions import Key, Attr

@app.route('/')
def index():
    loggedIn, username, noOfItems = getLoginDetails()
    print(session)
    collectiontable = dynamodb.Table('collections')
    
    response = collectiontable.scan()
    item = response['Items']
    print(item)
    return render_template('index.html',item=item,loggedIn=loggedIn,username=username,noOfItems=noOfItems)
   
    

@app.route('/create/user', methods=['POST','GET'])
def createUser():
    usertable = dynamodb.Table('users')
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        created_at = str(datetime.datetime.now())
        delivery_address = request.form['delivery_address']
        subscription_status = request.form['subscription_status']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country'] 
        phone = request.form['phone']

        if usertable.item_count == 0:
            usertable.put_item(
                        Item={
                'firstname': firstname,
                'lastname' : lastname,
                'email': email,
                'password': password,
                'created_at' : created_at,
                'delivery_address' : delivery_address,
                'subscription_status' : subscription_status,
                'city' : city,
                'state' : state,
                'country' : country,
                'phone' : phone
                    }
                )
            msg = 'Registration Complete. Please Login to your account !'
            
            return render_template('sign_in.html', msg=msg)
        else:
            response = usertable.query(
                    KeyConditionExpression=Key('email').eq(email)
            )
            if response['Count'] == 0:
                usertable.put_item(
                        Item={
                'firstname': firstname,
                'lastname' : lastname,
                'email': email,
                'password': password,
                'created_at' : created_at,
                'delivery_address' : delivery_address,
                'subscription_status' : subscription_status,
                'city' : city,
                'state' : state,
                'country' : country,
                'phone' : phone
                    }
                )
                msg = 'Registration Complete. Please Login to your account !'
            
                return render_template('sign_in.html', msg=msg)
            elif response['Count'] > 0: 
                if response['Items'][0]['email'] != email:
                    usertable.put_item(
                        Item={
                'firstname': firstname,
                'lastname' : lastname,
                'email': email,
                'password': password,
                'created_at' : created_at,
                'delivery_address' : delivery_address,
                'subscription_status' : subscription_status,
                'city' : city,
                'state' : state,
                'country' : country,
                'phone' : phone
                    }
                )
                    msg = 'Registration Complete. Please Login to your account !'
            
                    return render_template('sign_in.html', msg=msg)
                else:
                    msg = 'User Already Exists'
                    return render_template('registration_form.html', msg=msg)          
            
    return render_template('registration_form.html')

@app.route('/login/user', methods=['POST','GET'])
def loginUser():
    if request.method=='POST':         
        email = request.form['email']
        password = request.form['password']
        

        usertable = dynamodb.Table('users')
        response = usertable.query(
                KeyConditionExpression=Key('email').eq(email)
        )

        print(response)

        if response['Count']> 0:
            response = response['Items'][0]
        else:
            return render_template('sign_in.html', msg = 'Invalid Email / Password')
        if password == response['password']:
            session['email'] = email
            return redirect(url_for('index'))
        else:
            return render_template('sign_in.html', msg = 'Invalid Email / Password')
    return render_template('sign_in.html')

@app.route('/update/user', methods=['POST','GET'])
def updateUser():
    loggedIn, username, noOfItems = getLoginDetails()
    usertable = dynamodb.Table('users')
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        delivery_address = request.form['delivery_address']
        subscription_status = request.form['subscription_status']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country'] 
        phone = request.form['phone']

        usertable.put_item(
                    Item={
            'firstname': firstname,
            'lastname' : lastname,
            'email': email,
            'password': password,
            'delivery_address' : delivery_address,
            'subscription_status' : subscription_status,
            'city' : city,
            'state' : state,
            'country' : country,
            'phone' : phone
                }
            )
        msg = 'Your profile has been updated'
        
        return redirect(url_for('index'))
    
    response = usertable.query(
    KeyConditionExpression=Key('email').eq(session['email'])
)
    item = response['Items']
    print(item)

    return render_template('customers_profile.html',item=item,loggedIn=loggedIn,noOfItems=noOfItems)

@app.route('/delete/user')
def deleteUser():
    usertable = dynamodb.Table('users')
    usertable.delete_item(
    Key={
        'email': session['email']
    }
    )       
    session.pop('email')
    return redirect(url_for('index'))

@app.route('/logout/user')
def logoutUser():
    session.pop('email')
    return redirect(url_for('index'))    

@app.route('/admin')
def admin():
    loggedIn, username = getAdminLoginDetails()
    print(session)
    return render_template('admin_home.html',loggedIn=loggedIn,username=username)

@app.route('/create/vendor', methods=['POST','GET'])
def createVendor():
    if request.method=='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        created_at = str(datetime.datetime.now())
        city = request.form['city']
        state = request.form['state']
        country = request.form['country'] 
        phone = request.form['phone']

        usertable = dynamodb.Table('vendors')

        response = usertable.query(
                KeyConditionExpression=Key('email').eq(email)
        )

        if response['Count'] == 0:
            usertable.put_item(
                    Item={
            'firstname': firstname,
            'lastname' : lastname,
            'email': email,
            'password': password,
            'created_at' : created_at,
            'city' : city,
            'state' : state,
            'country' : country,
            'phone' : phone
                }
            )
            msg = 'Registration Complete. Please Login to your account !'
        
            return render_template('admin_login.html', msg=msg)
        elif response['Count'] > 0:
            if response['Items'][0]['email'] != email:
                usertable.put_item(
                        Item={
                'firstname': firstname,
                'lastname' : lastname,
                'email': email,
                'password': password,
                'created_at' : created_at,
                'city' : city,
                'state' : state,
                'country' : country,
                'phone' : phone
                    }
                )
                msg = 'Registration Complete. Please Login to your account !'
            
                return render_template('admin_login.html', msg=msg)
            else:
                msg = 'Vendor Already Exists'
                return render_template('vendor_registration_form.html', msg=msg)   

    return render_template('vendor_registration_form.html')

@app.route('/login/vendor', methods=['POST','GET'])
def loginVendor():
    if request.method=='POST':         
        email = request.form['email']
        password = request.form['password']
        

        usertable = dynamodb.Table('vendors')
        response = usertable.query(
                KeyConditionExpression=Key('email').eq(email)
        )

        print(response)

        if response['Count']> 0:
            response = response['Items'][0]
        else:
            return render_template('admin_login.html', msg = 'Invalid Email / Password')
        
        if password == response['password']:
            session['email'] = email
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', msg = 'Invalid Email / Password')
    return render_template('admin_login.html')

@app.route('/update/vendor', methods=['POST','GET'])
def updateVendor():
    loggedIn, username = getAdminLoginDetails()
    usertable = dynamodb.Table('vendors')
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country'] 
        phone = request.form['phone']

        usertable.put_item(
                    Item={
            'firstname': firstname,
            'lastname' : lastname,
            'email': email,
            'password': password,
            'city' : city,
            'state' : state,
            'country' : country,
            'phone' : phone
                }
            )
        msg = 'Your profile has been updated'
        
        return redirect(url_for('admin'))
    
    response = usertable.get_item(
    Key={
            'email': session['email'],
            'firstname': username
            
        }
    )
    item = response['Items']
    print(item)

    return render_template('vendor_profile.html',item=item,loggedIn=loggedIn)

@app.route('/delete/vendor')
def deleteVendor():
    usertable = dynamodb.Table('vendors')
    usertable.delete_item(
    Key={
        'email': session['email']
    }
    )
    session.pop('email')
    return redirect(url_for('index'))

@app.route('/logout/vendor')
def logoutVendor():
    session.pop('email')
    return redirect(url_for('index'))

@app.route('/<string:collectiontitle>/<string:categorytitle>/<string:producttitle>', methods=['GET'])
def productPage(collectiontitle,categorytitle,producttitle):
    loggedIn, username, noOfItems = getLoginDetails()
    producttable = dynamodb.Table('products')
    vendortable = dynamodb.Table('vendors')
    response = producttable.scan(FilterExpression=Attr('producttitle').eq(producttitle))
    
    item = response['Items'][0]
    print(item)

    vendorresponse = vendortable.scan(FilterExpression=Attr('email').eq(item['vendor']))
    vendor = vendorresponse['Items'][0]
    wishlisttable = dynamodb.Table('wishlists')
    wishlistresponse = wishlisttable.query(
        KeyConditionExpression=Key('producttitle').eq(producttitle)
    )
    wishitem = wishlistresponse['Items']
    return render_template('product.html',item=item,vendor=vendor,loggedIn=loggedIn,username=username,noOfItems=noOfItems,wishitem=wishitem,collection=collectiontitle,category=categorytitle)

@app.route('/<string:collectiontitle>')
def collectionPage(collectiontitle):
    loggedIn, username, noOfItems = getLoginDetails()
    producttable = dynamodb.Table('categories')
    response = producttable.scan(
    FilterExpression=Attr('collectiontitle').eq(collectiontitle))
    item = response['Items']
    print(item)
    return render_template('collection.html',item=item,loggedIn=loggedIn,username=username,noOfItems=noOfItems,collection=collectiontitle)

@app.route('/<string:collectiontitle>/<string:categorytitle>')
def categoryPage(collectiontitle,categorytitle):
    loggedIn, username, noOfItems = getLoginDetails()
    producttable = dynamodb.Table('products')
    response = producttable.scan(
    FilterExpression=Attr('categorytitle').eq(categorytitle))
    item = response['Items']
    print(item)
    return render_template('category.html',item=item,loggedIn=loggedIn,username=username,noOfItems=noOfItems,collection=collectiontitle,category=categorytitle)

@app.route('/display/vendor/product')
def displayProduct():
    loggedIn, username = getAdminLoginDetails()
    email = session['email']
    producttable = dynamodb.Table('products')

    response = producttable.scan(
    FilterExpression=Attr('vendor').eq(email)
    )
    items = response['Items']
    return render_template('admin_product.html',items=items,username=username)

@app.route('/create/product', methods=['POST','GET'])
def createProduct():
    loggedIn, username = getAdminLoginDetails()
    producttable = dynamodb.Table('products')
    categorytable = dynamodb.Table('categories')
    collectiontable = dynamodb.Table('collections')
    if request.method == 'POST':
        producttitle = request.form['producttitle']
        price = request.form['price']
        compared_price = request.form['compared_price']
        vendor = session['email']
        description = request.form['description']

        image = request.files['image']
        uploaded_file_extension = image.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_EXTENSIONS):
            destination_path = f'static/uploads/{image.filename}'
            image.save(destination_path)

        try:
            model_src = request.files['model_src']
            uploaded_file_extension = model_src.filename.split('.')[1]
            if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
                model_destination_path = f'static/assets/{model_src.filename}'
                model_src.save(model_destination_path)
                model_src = model_src.filename
        except:
            model_src = ''

        try:
            model_ios_src = request.files['model_ios_src']
            uploaded_file_extension = model_ios_src.filename.split('.')[1]
            if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
                ios_destination_path = f'static/assets/{model_ios_src.filename}'
                model_ios_src.save(ios_destination_path)
                model_ios_src = model_ios_src.filename
        except:
           model_ios_src = '' 

        size = request.form.getlist('size')
        stock = request.form['stock']
        categorytitle = request.form['categorytitle'] 
        

        producttable.put_item(
                    Item={
            'producttitle': producttitle,
            'price' : price,
            'compared_price': compared_price,
            'vendor': vendor,
            'description' : description,
            'image' : image.filename,
            'model_src' : model_src,
            'model_ios_src' : model_ios_src,
            'size': size,
            'stock': stock,
            'categorytitle':categorytitle
                }
            )
        msg = 'Product  has been added'
        
        return redirect(url_for('admin'))

    response = categorytable.scan()
    category_item = [[i['categorytitle'],i['collectiontitle']] for i in response['Items']]
    print(category_item)

    response = collectiontable.scan()
    collection_item = [i['collectiontitle'] for i in response['Items']]
    #print(collection_item)
    return render_template('add_product.html',loggedIn=loggedIn,username=username,category_item=category_item,collection_item=collection_item)

@app.route('/update/product/<string:producttitle>', methods=['POST','GET'])
def updateProduct(producttitle):
    loggedIn, username = getAdminLoginDetails()
    producttable = dynamodb.Table('products')
    categorytable = dynamodb.Table('categories')
    if request.method == 'POST':
        producttitle = request.form['producttitle']
        price = request.form['price']
        compared_price = request.form['compared_price']
        vendor = session['email']
        description = request.form['description']

        image = request.files['image']
        uploaded_file_extension = image.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_EXTENSIONS):
            destination_path = f'static/uploads/{image.filename}'
            image.save(destination_path)

        model_src = request.files['model_src']
        uploaded_file_extension = model_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            model_destination_path = f'static/assets/{model_src.filename}'
            model_src.save(model_destination_path)

        model_ios_src = request.files['model_ios_src']
        uploaded_file_extension = model_ios_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            ios_destination_path = f'static/assets/{model_ios_src.filename}'
            model_ios_src.save(ios_destination_path)

        size = list(request.form['size'])
        stock = request.form['stock']
        categorytitle = request.form['categorytitle'] 
        

        producttable.put_item(
                    Item={
            'producttitle': producttitle,
            'price' : price,
            'compared_price': compared_price,
            'vendor': vendor,
            'description' : description,
            'image' : image.filename,
            'model_src' : model_src.filename,
            'model_ios_src' : model_ios_src.filename,
            'size': size,
            'stock': stock,
            'categorytitle':categorytitle
                }
            )
        msg = 'Product  has been updated'
        
        return redirect(url_for('admin'))

    response = categorytable.scan()
    category_item = response['Items']
    response = producttable.get_item(
        Key={
        'producttitle': producttitle
    })
    product_item = response['Items']

    return render_template('edit_products.html',loggedIn=loggedIn,username=username,category_item=category_item,product_item=product_item)

@app.route('/delete/product/<string:producttitle>')
def deleteProduct(producttitle):
    usertable = dynamodb.Table('products')
    usertable.delete_item(
    Key={
        'producttitle': producttitle
    }
    )
    return redirect(url_for('admin'))

@app.route('/create/category', methods=['POST','GET'])
def createCategory():
    loggedIn, username = getAdminLoginDetails()
    categorytable = dynamodb.Table('categories')
    collectiontable = dynamodb.Table('collections')
    if request.method == 'POST':
        categorytitle = request.form['categorytitle']
        description = request.form['description']

        image = request.files['image']
        uploaded_file_extension = image.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_EXTENSIONS):
            destination_path = f'static/uploads/{image.filename}'
            image.save(destination_path)

        model_src = request.files['model_src']
        uploaded_file_extension = model_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            model_destination_path = f'static/assets/{model_src.filename}'
            model_src.save(model_destination_path)

        model_ios_src = request.files['model_ios_src']
        uploaded_file_extension = model_ios_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            ios_destination_path = f'static/assets/{model_ios_src.filename}'
            model_ios_src.save(ios_destination_path)

        size = list(request.form['size'])
        collectiontitle = request.form['collectiontitle'] 
        

        categorytable.put_item(
                    Item={
            'categorytitle': categorytitle,
            'description' : description,
            'image' : image.filename,
            'model_src' : model_src.filename,
            'model_ios_src' : model_ios_src.filename,
            'size': size,
            'collectiontitle':collectiontitle
                }
            )
        msg = 'Category has been added'
        
        return redirect(url_for('admin'))

    response = collectiontable.scan()
    collection_item = response['Items']

    return render_template('add_category.html',loggedIn=loggedIn,username=username,collection_item=collection_item)

@app.route('/edit/category/<string:categorytitle>', methods=['POST','GET'])
def editCategory(categorytitle):
    loggedIn, username = getAdminLoginDetails()
    categorytable = dynamodb.Table('categories')
    collectiontable = dynamodb.Table('collections')
    if request.method == 'POST':
        categorytitle = request.form['collectiontitle']
        description = request.form['description']

        image = request.files['image']
        uploaded_file_extension = image.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_EXTENSIONS):
            destination_path = f'static/uploads/{image.filename}'
            image.save(destination_path)

        model_src = request.files['model_src']
        uploaded_file_extension = model_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            model_destination_path = f'static/assets/{model_src.filename}'
            model_src.save(model_destination_path)

        model_ios_src = request.files['model_ios_src']
        uploaded_file_extension = model_ios_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            ios_destination_path = f'static/assets/{model_ios_src.filename}'
            model_ios_src.save(ios_destination_path)

        size = list(request.form['size'])
        collectiontitle = request.form['collectiontitle'] 
        

        categorytable.put_item(
                    Item={
            'categorytitle': categorytitle,
            'description' : description,
            'image' : image.filename,
            'model_src' : model_src.filename,
            'model_ios_src' : model_ios_src.filename,
            'size': size,
            'collectiontitle':collectiontitle
                }
            )
        msg = 'Category  has been updated'
        
        return redirect(url_for('admin'))

    response = categorytable.get_item(
        Key={
        'categorytitle': categorytitle
    }
    )
    category_item = response['Items']
    response = collectiontable.get_item()
    collection_item = response['Items']

    return render_template('edit_category.html',loggedIn=loggedIn,username=username,category_item=category_item,collection_item=collection_item)

@app.route('/delete/collection/<string:categorytitle>')
def deleteCategory(categorytitle):
    usertable = dynamodb.Table('categories')
    usertable.delete_item(
    Key={
        'producttitle': categorytitle
    }
    )
    return redirect(url_for('admin'))

@app.route('/create/collection', methods=['POST','GET'])
def createCollection():
    loggedIn, username = getAdminLoginDetails()
    collectiontable = dynamodb.Table('collections')
    if request.method == 'POST':
        collectiontitle = request.form['collectiontitle']
        description = request.form['description']

        image = request.files['image']
        uploaded_file_extension = image.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_EXTENSIONS):
            destination_path = f'static/uploads/{image.filename}'
            image.save(destination_path)

        model_src = request.files['model_src']
        uploaded_file_extension = model_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            model_destination_path = f'static/assets/{model_src.filename}'
            model_src.save(model_destination_path)

        model_ios_src = request.files['model_ios_src']
        uploaded_file_extension = model_ios_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            ios_destination_path = f'static/assets/{model_ios_src.filename}'
            model_ios_src.save(ios_destination_path)
        

        collectiontable.put_item(
                    Item={
            'categorytitle': collectiontitle,
            'description' : description,
            'image' : image.filename,
            'model_src' : model_src.filename,
            'model_ios_src' : model_ios_src.filename
                }
            )
        msg = 'Collection has been added'
        
        return redirect(url_for('admin'))



    return render_template('add_category.html',loggedIn=loggedIn,username=username)

@app.route('/edit/collection/<string:collectiontitle>', methods=['POST','GET'])
def editCollection(collectiontitle):
    loggedIn, username = getAdminLoginDetails()
    collectiontable = dynamodb.Table('collections')
    if request.method == 'POST':
        collectiontitle = request.form['collectiontitle']
        description = request.form['description']

        image = request.files['image']
        uploaded_file_extension = image.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_EXTENSIONS):
            destination_path = f'static/uploads/{image.filename}'
            image.save(destination_path)

        model_src = request.files['model_src']
        uploaded_file_extension = model_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            model_destination_path = f'static/assets/{model_src.filename}'
            model_src.save(model_destination_path)

        model_ios_src = request.files['model_ios_src']
        uploaded_file_extension = model_ios_src.filename.split('.')[1]
        if (uploaded_file_extension.lower() in ALLOWED_ASSET_EXTENSIONS):
            ios_destination_path = f'static/assets/{model_ios_src.filename}'
            model_ios_src.save(ios_destination_path)

      
        

        collectiontable.put_item(
                    Item={
            'categorytitle': collectiontitle,
            'description' : description,
            'image' : image.filename,
            'model_src' : model_src.filename,
            'model_ios_src' : model_ios_src.filename

                }
            )
        msg = 'Collection  has been updated'
        
        return redirect(url_for('admin'))

    response = collectiontable.get_item(
        Key={
        'categorytitle': collectiontitle
    }
    )
    collection_item = response['Items']

    return render_template('edit_collection.html',loggedIn=loggedIn,username=username,collection_item=collection_item)

@app.route('/delete/collection/<string:collectiontitle>')
def deleteCollection(collectiontitle):
    usertable = dynamodb.Table('collections')
    usertable.delete_item(
    Key={
        'producttitle': collectiontitle
    }
    )
    return redirect(url_for('admin'))

@app.route('/wishlist')
def wishlistPage():
    loggedIn, username, noOfItems = getLoginDetails()
    try:
        if 'email' in session:
            producttable = dynamodb.Table('wishlists')
            response = producttable.query(
                KeyConditionExpression=Key('email').eq(session['email'])
            )
            item = response['Items']
            print(item)
            return render_template('wishlist.html',item=item,loggedIn=loggedIn,username=username,noOfItems=noOfItems)
        elif 'email' not in session:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))

@app.route('/add/wishlist/<string:producttitle>')
def addWishlist(producttitle):
    wishlisttable = dynamodb.Table('wishlists')
    wishlisttable.put_item(
                    Item={
            'producttitle': producttitle,
                }
            )
    return redirect(url_for('index'))

@app.route('/delete/wishlist/<string:producttitle>')
def deleteWishlist(producttitle):
    wishlisttable = dynamodb.Table('wishlists')
    wishlisttable.delete_item(
                    Item={
            'producttitle': producttitle,
                }
            )
    return redirect(url_for('index'))
    
@app.route('/addToCart', methods=['POST','GET'])
def addCart():
    if 'email' in session:
        if request.method == 'POST':
            carttable = dynamodb.Table('carts')
            cartid = keys.generate()
            email = session['email']
            producttitle = request.form['producttitle']
            image = request.form['image']
            price = request.form['price']
            unit = request.form['unit']
            total = int(request.form['price'])*int(request.form['unit'])
            size = request.form['size']
            carttable.put_item(
                Item={
                'cartid': cartid,
                'email' : email,
                'producttitle' : producttitle,
                'image' : image,
                'unit' : unit,
                'total' : total,
                'size' : size

                    }
            )

            msg = 'Added item to cart'
            
            return redirect(url_for('index'))
    else:
        return redirect(url_for('loginUser'))    

@app.route('/cart')
def cartPage():
    loggedIn, username, noOfItems = getLoginDetails()
   
    if 'email' in session:
        carttable = dynamodb.Table('carts')
        response = carttable.scan(
            FilterExpression=Attr('email').eq(session['email'])
        )
        item = response['Items']
        print(item)
        totalprice = 0
        for i in item:
            totalprice += int(i['total'])
        
        return render_template('cart.html',item=item,totalprice=totalprice,loggedIn=loggedIn,username=username,noOfItems=noOfItems)
    elif 'email' not in session:
        return redirect(url_for('index'))

@app.route('/checkout')
def checkoutPage():
    loggedIn, username, noOfItems = getLoginDetails()
   
    if 'email' in session:
        usertable = dynamodb.Table('users')
        carttable = dynamodb.Table('carts')
        userresponse = usertable.scan(
            FilterExpression=Attr('email').eq(session['email'])
        )
        response = carttable.scan(
            FilterExpression=Attr('email').eq(session['email'])
        )
        user = userresponse['Items'][0]
        item = response['Items']
        print(item)
        totalprice = 0
        for i in item:
            totalprice += int(i['total'])
        
        return render_template('checkout.html',item=item,user=user,totalprice=totalprice,loggedIn=loggedIn,username=username,noOfItems=noOfItems)
    elif 'email' not in session:
        return redirect(url_for('index'))
    

@app.route('/delete/cart/<string:cartid>')
def deleteCart(cartid):
    table = dynamodb.Table('carts')
    table.delete_item(
    Key={
        'cartid': cartid,
        'email': session['email']
    }
)

    return redirect(url_for('index'))

@app.route('/payment/page')
def paymentPage():
    if 'email' in session:
        return render_template('confirmation_successful.html')
    else:
        redirect(url_for('index'))

@app.route('/confirmation/successful')
def createOrder():
    ordertable = dynamodb.Table('orders')
    carttable = dynamodb.Table('carts')
    usertable = dynamodb.Table('users')
    if 'email' in session:
        cartresponse = carttable.scan(
            FilterExpression=Attr('email').eq(session['email'])
        )
        userresponse = usertable.scan(
            FilterExpression=Attr('email').eq(session['email'])
        )
        item = cartresponse['Items']
        totalprice = 0
        for i in item:
            totalprice += int(i['total'])
        user = userresponse['Items'][0]
        reference = keys.generate()
        email = session['email']
        items = item
        username = user['firstname'] + ' ' + user['lastname']
        amount = totalprice
        created_at = str(datetime.datetime.now())
        exp_delivery_date = str(datetime.datetime.now() + timedelta(days=8))
        payment_status = 'No'
        delivery_address = user['delivery_address']
        phone = user['phone']
        ordertable.put_item(
            Item={
            'reference': reference,
            'email' : email,
            'items' : items,
            'username' : username,
            'amount' : amount,
            'created_at' : created_at,
            'exp_delivery_date' : exp_delivery_date,
            'payment_status': payment_status,
            'delivery_address':delivery_address,
            'phone':phone

                }
        )

        for i in item:
            carttable.delete_item(
            Key={
                'cartid': i['cartid'],
                'email': session['email']
            })

        msg = 'Successfully created order'
        print(msg)

        data = {'email':email,'phone':phone,'reference':reference,'code':keys.PUBLIC_KEY,'amount':amount*100,'username':username}
        
        return jsonify(data)
    else:
        return redirect(url_for('loginUser'))





















def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        username = ''
        noOfItems = 0
    else:
        email = session['email']
        usertable = dynamodb.Table('users')
        carttable = dynamodb.Table('carts')
        loggedIn = True
        userresponse = usertable.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        cartresponse = carttable.scan(
    FilterExpression=Attr('email').eq(session['email'])
)
        username = userresponse['Items'][0]['firstname']
        noOfItems = cartresponse['Count']
    print(cartresponse)
    return (loggedIn, username, noOfItems)

def getAdminLoginDetails():
    if 'email' not in session:
        loggedIn = False
        username = ''
    else:
        email = session['email']
        vendortable = dynamodb.Table('vendors')
        loggedIn = True
        userresponse = vendortable.query(
                KeyConditionExpression=Key('email').eq(email)
        )

        username = userresponse['Items'][0]['firstname']

    
    return (loggedIn, username)

@app.errorhandler(404)
def page_not_found(e):
    loggedIn, username, noOfItems = getLoginDetails()
    return render_template('404.html',loggedIn=loggedIn, username=username, noOfItems=noOfItems), 404
 
 
@app.errorhandler(500)
def internal_server_error(e):
    loggedIn, username, noOfItems = getLoginDetails()
    return render_template('500.html',loggedIn=loggedIn, username=username, noOfItems=noOfItems)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(host='127.0.0.1', port=8080, debug=True)
