"""
This script runs the StoreSalesStaffingPrediction application using a development server.
"""

from os import environ
from StoreSalesStaffingPrediction import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    app.secret_key = 'salesprediction'
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
