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
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html', 
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/registration', methods = ['POST','GET'])
def registration():
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
              except Exception as e:
                    cursor.rollback()
                    print(e.value)
                    print('transaction rolled back')
              else:
                    print('registrated successfully')
                    cursor.commit()
                    cursor.close()
              
                    return render_template('about.html',registration=user)
    else:
      return render_template('registration.html')


