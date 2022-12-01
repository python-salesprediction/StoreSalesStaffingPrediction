"""
Routes and views for the flask application.
"""

import configparser
import sys
import pyodbc as odbc

from datetime import datetime
from flask import session, redirect, url_for, escape, request, render_template
from StoreSalesStaffingPrediction import app
from datetime import datetime

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

#region User Registration, login, logout
@app.route('/registration', methods = ['POST','GET'])
def registration():
    if request.method == 'POST':
      user = request.form
      user = [request.form['FirstName'], request.form['LastName'], request.form['EmailID'], request.form['Password'], request.form['ContactNo']]
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
              
                    return render_template('about.html',registration=user,title='Register',
                                                                          year=datetime.now().year)
    else:
      return render_template('registration.html',title='Register', year=datetime.now().year)

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
      user = request.form
      user = [request.form['EmailID'], request.form['Password']]
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
                get_user = "select top(1) u.UserID,u.EmailID,u.Password,ur.Role from UserMaster u inner join UserRole ur on ur.UserID = u.UserID where u.EmailID = ?"

                try:
                    cursor.execute(get_user, user[0])
                    login_user = cursor.fetchone()
                except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
                else:
                    cursor.commit()
                    cursor.close()

                    #Password verification and setting sessions for logged in user
                    if(login_user is not None and login_user[2] == user[1]):
                        session['userid'] = login_user[0]
                        session['email'] = login_user[1]
                        session['role'] = login_user[3]
                        return render_template('about.html', login_user = login_user,
                                                                     title='Login',
                                                                     year=datetime.now().year)

                    else:
                        return render_template('login.html',
                                title='Login',
                                year=datetime.now().year)

    else:
      return render_template('login.html',
                                title='Login',
                                year=datetime.now().year)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('userid', None)
   session.pop('email', None)
   session.pop('role', None)
   return redirect(url_for('login'))
#endregion 

#region Master pages and Foreign Key insertions
@app.route('/Discountdetail', methods = ['POST','GET'])
def discountdetail():
    if request.method == 'POST':
      discount = request.form
      discount = [request.form['DiscountType'], request.form['DiscountPercentage']]
      if discount:
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
                INSERT INTO DiscountDetail
                VALUES (?,?)
              """
              
              try:
                    cursor.execute(insert_statement, discount)        
              except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
              else:
                    print('Discount details inserted successfully.')
                    cursor.commit()
                    cursor.close()
              
                    return render_template('DiscountDetail.html',discountdetail=discount,title='Discount', year=datetime.now().year)
    else:
      return render_template('DiscountDetail.html',title='Discount', year=datetime.now().year)

@app.route('/season', methods = ['POST','GET'])
def seasonmaster():
    if request.method == 'POST':
      season = request.form
      season = [request.form['Season'], request.form['StartMonth'], request.form['EndMonth']]
      if season:
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
                INSERT INTO SeasonMaster
                VALUES (?, ?, ?)
              """
              
              try:
                    cursor.execute(insert_statement, season)        
              except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
              else:
                    print('Season inserted successfully.')
                    cursor.commit()
                    cursor.close()
              
                    return render_template('Seasonmaster.html',season=season,title='Season', year=datetime.now().year)
    else:
      return render_template('SeasonMaster.html',title='Season', year=datetime.now().year) 

@app.route('/category', methods=['POST', 'GET'])
def Category():
    if request.method == 'POST':
        user = request.form
        user = [request.form['Category']]
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

                    return render_template('category.html', category=user,title='Category', year=datetime.now().year)
    else:
        return render_template('Category.html',title='Category', year=datetime.now().year)

@app.route('/NewProduct', methods=['POST', 'GET'])
def Product():

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
            return render_template('NewProduct.html', categories = categories,title='Product', year=datetime.now().year)

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
              return render_template('NewProduct.html',product=product,title='Product', year=datetime.now().year)
    else:
        return render_template('NewProduct.html',title='Product', year=datetime.now().year)

@app.route('/sales', methods=['POST', 'GET'])
def Sales():

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
            cursor.execute("select * from ProductDetail")
            products = cursor.fetchall()

            cursor.execute("select * from SeasonMaster")
            seasons = cursor.fetchall()

            cursor.execute("select * from DiscountDetail")
            discounts = cursor.fetchall()
        except Exception as e:
            cursor.rollback()
            print(e.value)
            print('transaction rolled back')
        else:
            cursor.commit()
            cursor.close()
            return render_template('sales.html', products = products, seasons= seasons, discounts = discounts ,title='Sales', year=datetime.now().year)

    elif request.method == 'POST':
        sales = request.form
        sales_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        sales = [request.form['ProductID'], sales_date, request.form['SalePrice'], request.form['ClearancePrice'], request.form['Quantity'], request.form['SeasonID'], request.form['DiscountID']]
        insert_statement = """
               INSERT INTO SalesDetail
               VALUES (?, ?, ?, ?, ?, ?, ?)
            """
              
        try:
              cursor.execute(insert_statement, sales)        
        except Exception as e:
              cursor.rollback()
              print(e.value)
              print('transaction rolled back')
        else:
              print('Product sales inserted successfully.')
              cursor.commit()
              cursor.close()
              return render_template('sales.html',sales=sales,title='Sales', year=datetime.now().year)
    else:
        return render_template('sales.html',title='Sales', year=datetime.now().year)
#endregion

#region Reports

#Reports Code
@app.route('/ProductReport', methods=['POST', 'GET'])
def productreport():
    if request.method == 'GET':
        if True:
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
                storedProc = "Exec GetProductDetail"
                #params = ("And", 10)

                try:
                    cursor.execute(storedProc)
                    productreport = cursor.fetchall()
                except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
                else:
                    cursor.commit()
                    cursor.close()

                    return render_template('ProductReport.html', productreport = productreport,
                                                                title='Products',
                                                                year=datetime.now().year,
                                                                message='Product Details Report.')
    else:
        return render_template('ProductReport.html',title='Products',
                                                    year=datetime.now().year,
                                                    message='Product Details Report.')

@app.route('/staffdetail', methods=['POST', 'GET'])
def Staffdetail():

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

    if request.method == 'GET':
        try:
            cursor.execute("select * from CategoryMaster")
            categories = cursor.fetchall()

            cursor.execute("select * from UserMaster")
            users = cursor.fetchall()

        except Exception as e:
            cursor.rollback()
            print(e.value)
            print('transaction rolled back')
        else:
            cursor.commit()
            cursor.close()
            return render_template('staffdetail.html', categories = categories, users = users)

    elif request.method == 'POST':
        staffdetail = request.form
        staffdetail = [request.form['UserID'],request.form['EmploymentType'],request.form['CategoryID']]
        insert_statement = """
               INSERT INTO StaffDetail
               VALUES (?,?,?)
            """
              
        try:
              cursor.execute(insert_statement,staffdetail)        
        except Exception as e:
              cursor.rollback()
              print(e.value)
              print('transaction rolled back')
        else:
              print('Product inserted successfully.')
              cursor.commit()
              cursor.close()
              return render_template('staffdetail.html',staffdetail = staffdetail)
    else:
        return render_template('staffdetail.html')

@app.route('/Staffscheduledetail', methods=['POST', 'GET'])
def Staffscheduledetail():

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

    if request.method == 'GET':
        try:
            cursor.execute("select * from StaffDetail")
            staff = cursor.fetchall()

        except Exception as e:
            cursor.rollback()
            print(e.value)
            print('transaction rolled back')
        else:
            cursor.commit()
            cursor.close()
            return render_template('StaffScheduleDetail.html', staff = staff)

    elif request.method == 'POST':
        staff = request.form
        staff = [request.form['StaffID'],request.form['Date'],request.form['DayWeek'],request.form['ShiftStart'],request.form['ShiftEnd']]
        insert_statement = """
               INSERT INTO StaffScheduleDetail
               VALUES (?,?,?,?,?)
            """
              
        try:
              cursor.execute(insert_statement,staff)        

        except Exception as e:
              cursor.rollback()
              print(e.value)
              print('transaction rolled back')
        else:
              print('Product inserted successfully.')
              cursor.commit()
              cursor.close()
              return render_template('StaffScheduleDetail.html',staff = staff)
    else:
        return render_template('StaffScheduleDetail.html')
