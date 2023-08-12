from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="techtutors"
)

@app.route('/ussd', methods=['POST'])
def ussd_handler():
    """
    Handles incoming USSD requests and generates appropriate responses.

    Returns:
        str: USSD response text
    """
    session_id = request.form['sessionId']
    user_input = request.form['text']

    if user_input == '*1188#':
        # Initial menu for authentication
        response = 'CON Welcome to TechTutors USSD!\n'
        response += '1. Culture\n'
        response += '2. Entertainment\n'
        response += '3. Fashion\n'
        response += '4. Sports\n'
        response += '5. Technology\n'
        response += '6. Add a Category for the Future\n'
    else:
        # Handle user input using recursive function
        response = handle_user_input(user_input)

    return response

def handle_user_input(user_input):
    """
    Handles user input and generates USSD responses.

    Args:
        user_input (str): User's input

    Returns:
        str: USSD response text
    """
    if user_input == '1':
        return get_random_content('Culture')
    elif user_input == '2':
        return get_random_content('Entertainment')
    elif user_input == '3':
        return get_random_content('Fashion')
    elif user_input == '4':
        return get_random_content('Sports')
    elif user_input == '5':
        return get_random_content('Technology')
    elif user_input == '6':
        return 'CON Enter the name of the category you would like to see in the future:\n'
    elif user_input.startswith('6*'):
        new_category = user_input[2:]
        return save_new_category_recursive(new_category)
    else:
        return 'END Invalid input. Please try again.'

def get_random_content(category):
    """
    Retrieves random content from the specified category.

    Args:
        category (str): Category name

    Returns:
        str: USSD response text
    """
    cursor = db.cursor(dictionary=True)
    query = f"SELECT description FROM content WHERE category = '{category}' ORDER BY RAND() LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if result:
        return f'CON {category}:\n{result["description"]}\n'
    else:
        return 'END No content available for this category.\n'

def save_new_category_recursive(category):
    """
    Adds a new category to the database.

    Args:
        category (str): Category name

    Returns:
        str: USSD response text
    """
    cursor = db.cursor()
    query = f"INSERT INTO categories (name) VALUES ('{category}')"
    try:
        cursor.execute(query)
        db.commit()
        cursor.close()
        return 'END Category added successfully!\n'
    except Exception as e:
        return f'END Error adding category: {str(e)}\n'

if __name__ == '__main__':
    app.run(debug=True)
