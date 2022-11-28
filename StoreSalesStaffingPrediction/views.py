"""
Routes and views for the flask application.
"""

import configparser
import sys
import pyodbc as odbc

from datetime import datetime
from flask import render_template, request
from StoreSalesStaffingPrediction import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html', 
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')

@app.route('/registration', methods = ['POST','GET'])
def registration():
    #return render_template(
    #    'registration.html',
    #    title='Register',
    #    year=datetime.now().year,
    #    message='Your application description page.'
    #)
    if request.method == 'POST':
      user = request.form
      user = [request.form['FirstName'], request.form['LastName'], request.form['EmailID'], request.form['Password'], request.form['ContactNo']]
      if user:
          DRIVER = 'SQL Server'
          SERVER_NAME = 'DESKTOP-0AV09UH'
          DATABASE_NAME = 'StoreSalesPrediction'
          cursor = ''
          
          conn_string = f"""
              Driver={{{DRIVER}}};
              Server={SERVER_NAME};
              Database={DATABASE_NAME};
              Trust_Connection=yes;
          """
          
          try:
              conn = odbc.connect(conn_string)
          except Exception as e:
              print(e)
              print('task is terminated')
              sys.exit()
          else:
              cursor = conn.cursor()

              insert_statement = """
                INSERT INTO UserMaster
                VALUES (?, ?, ?, ?, ?)
              """
              
              try:
                    cursor.execute(insert_statement, user)  
                    cursor.execute("SELECT @@IDENTITY AS ID;")
                    user_id = cursor.fetchone()[0]

                    user_role = [user_id,request.form['Role']]

                    insert_user_role = """
                        INSERT INTO UserRole
                        VALUES (?, ?)
                    """
                    cursor.execute(insert_user_role, user_role)  
              except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
              else:
                    print('Registered successfully')
                    cursor.commit()
                    cursor.close()
              
                    return render_template('about.html',registration=user)
    else:
      return render_template('registration.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    return render_template('login.html',
        title='Login',
        year=datetime.now().year,
        message='Your application description page.')
    if request.method == 'POST':
      user = request.form
      user = [request.form['EmailID'], request.form['Password']]
      if user:
          DRIVER = 'SQL Server'
          SERVER_NAME = 'KRISH'
          DATABASE_NAME = 'StoreSalesPrediction'
          cursor = ''
          
          conn_string = f"""
              Driver={{{DRIVER}}};
              Server={SERVER_NAME};
              Database={DATABASE_NAME};
              Trust_Connection=yes;
          """
          
    else:
      return render_template('login.html')

@app.route('/Discountdetail', methods = ['POST','GET'])
def discountdetail():
    if request.method == 'POST':
      user = request.form
      user = [request.form['DiscountType'], request.form['DiscountPercentage']]
      if user:
          DRIVER = 'SQL Server'
          SERVER_NAME = 'MANSIPATEL\ASQL'
          DATABASE_NAME = 'StoreSalesPrediction'
          cursor = ''
          
          conn_string = f"""
              Driver={{{DRIVER}}};
              Server={SERVER_NAME};
              Database={DATABASE_NAME};
              Trust_Connection=yes;
          """
          
          try:
              conn = odbc.connect(conn_string)
          except Exception as e:
              print(e)
              print('task is terminated')
              sys.exit()
          else:
              cursor = conn.cursor()

              insert_statement = """
                INSERT INTO DiscountDetail
                VALUES (?,?)
              """
              
              try:
                    cursor.execute(insert_statement, user)        
              except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
              else:
                    print('Discount details inserted successfully.')
                    cursor.commit()
                    cursor.close()
              
                    return render_template('DiscountDetail.html',discountdetail=user)
    else:
      return render_template('DiscountDetail.html')

@app.route('/season', methods = ['POST','GET'])
def seasonmaster():
    if request.method == 'POST':
      user = request.form
      user = [request.form['Season'], request.form['StartMonth'], request.form['EndMonth']]
      if user:
          DRIVER = 'SQL Server'
          SERVER_NAME = 'LAPTOP-IKD7TK5J\ISQL'
          DATABASE_NAME = 'StoreSalesPrediction'
          cursor = ''
          
          conn_string = f"""
              Driver={{{DRIVER}}};
              Server={SERVER_NAME};
              Database={DATABASE_NAME};
              Trust_Connection=yes;
          """
          
          try:
              conn = odbc.connect(conn_string)
          except Exception as e:
              print(e)
              print('task is terminated')
              sys.exit()
          else:
              cursor = conn.cursor()

              insert_statement = """
                INSERT INTO SeasonMaster
                VALUES (?, ?, ?)
              """
              
              try:
                    cursor.execute(insert_statement, user)        
              except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
              else:
                    print('Season inserted successfully.')
                    cursor.commit()
                    cursor.close()
              
                    return render_template('Seasonmaster.html',season=user)
    else:
      return render_template('SeasonMaster.html') 

@app.route('/category', methods=['POST', 'GET'])
def Category():
    if request.method == 'POST':
        user = request.form
        user = [request.form['Category']]
        if user:
            DRIVER = 'SQL Server'
            SERVER_NAME = 'DESKTOP-0AV09UH'
            DATABASE_NAME = 'StoreSalesPrediction'
            cursor = ''

            conn_string = f"""
              Driver={{{DRIVER}}};
              Server={SERVER_NAME};
              Database={DATABASE_NAME};
              Trust_Connection=yes;
          """

            try:
                conn = odbc.connect(conn_string)
            except Exception as e:
                print(e)
                print('task is terminated')
                sys.exit()
            else:
                cursor = conn.cursor()

                insert_statement = """
                INSERT INTO CategoryMaster
                VALUES (?)
              """

                try:
                    cursor.execute(insert_statement, user)
                except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
                else:
                    print('Category inserted successfully.')
                    cursor.commit()
                    cursor.close()

                    return render_template('category.html', category=user)
    else:
        return render_template('Category.html')

@app.route('/NewProduct', methods=['POST', 'GET'])
def Product():

    DRIVER = 'SQL Server'
    SERVER_NAME = 'DESKTOP-0AV09UH'
    DATABASE_NAME = 'StoreSalesPrediction'
    cursor = ''

    conn_string = f"""
       Driver={{{DRIVER}}};
       Server={SERVER_NAME};
       Database={DATABASE_NAME};
       Trust_Connection=yes;
  """

    try:
        conn = odbc.connect(conn_string)
    except Exception as e:
        print(e)
        print('task is terminated')
        sys.exit()
    else:
        cursor = conn.cursor()

    if request.method == 'GET':
        try:
            cursor.execute("select * from CategoryMaster")
            categories = cursor.fetchall()
        except Exception as e:
            cursor.rollback()
            print(e.value)
            print('transaction rolled back')
        else:
            cursor.commit()
            cursor.close()
            return render_template('NewProduct.html', categories = categories)

    elif request.method == 'POST':
        product = request.form
        product = [request.form['CategoryID'], request.form['ProductName'], request.form['Description'], request.form['Price'], request.form['ManufactureDate'], request.form['ExpiryDate']]
        insert_statement = """
               INSERT INTO ProductDetail
               VALUES (?, ?, ?, ?, ?, ?)
            """
              
        try:
              cursor.execute(insert_statement, product)        
        except Exception as e:
              cursor.rollback()
              print(e.value)
              print('transaction rolled back')
        else:
              print('Product inserted successfully.')
              cursor.commit()
              cursor.close()
              return render_template('NewProduct.html',product=product)
    else:
        return render_template('NewProduct.html')




