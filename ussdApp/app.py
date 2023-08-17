#!/usr/bin/python3
from flask import Flask, request
import mysql.connector

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_pyfile('config.py')

# Database connection
db = mysql.connector.connect(
    host=app.config['DB_HOST'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    database=app.config['DB_NAME']
)

if db.is_connected():
    print("Database connection established successfully")

print(db.database)

@app.route('/ussd', methods=['POST'])
def ussd_handler():
    session_id = request.form['sessionId']
    user_input = request.form['text']

    if user_input == '*1188*':
        # List categories
        response = 'CON Select a category:\n'
        categories = get_categories()
        for idx, category in enumerate(categories, start=1):
            response += f'{idx}. {category}\n'
        response += f'{len(categories) + 1}. Request a new category\n'
    else:
        # Handle user input
        response = handle_user_input(user_input)

    return response

def get_categories():
    cursor = db.cursor()
    query = "SELECT name FROM category"
    cursor.execute(query)
    categories = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return categories

def get_random_content(category):
    cursor = db.cursor()
    query = f"SELECT content FROM bitcontent WHERE category_name = '{category}' ORDER BY RAND() LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if result:
        return f'CON {category}:\n{result[0]}\n'
    else:
        return 'END No content available for this category.\n'

def save_new_category_request(category):
    cursor = db.cursor()
    query = f"INSERT INTO requests (category_name) VALUES ('{category}')"
    try:
        cursor.execute(query)
        db.commit()
        cursor.close()
        return 'END Category request added successfully!\n'
    except Exception as e:
        return f'END Error adding category request: {str(e)}\n'

def handle_user_input(user_input):
    if user_input.isdigit():
        categories = get_categories()
        selection = int(user_input)
        if 1 <= selection <= len(categories):
            selected_category = categories[selection - 1]
            return get_random_content(selected_category)
        elif selection == len(categories) + 1:
            return 'CON Enter the name of the category you would like to request:\n'
    elif user_input.startswith('6*'):
        new_category = user_input[2:]
        return save_new_category_request(new_category)
    
    return 'END Invalid input. Please try again.\n'

if __name__ == '__main__':
    app.run(debug=True)
