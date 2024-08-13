import time
import requests

# Create a Session object to handle cookies
session = requests.Session()

# Login credentials
login_data = {
    'email': 'xss@example.com',
    'password': 'NoWayYouCanStealMyCookies!'
}

cookies = {
    'Flag': "FLAG{s7Or3d_XsS_9On3_CR42YYy!}"
}

def login():
    login_url = 'http://localhost:8081/login'
    response = session.post(login_url, data=login_data)
    if not 'incorrect' in str(response.content.lower()):
        session.cookies.update(response.cookies)
        session.cookies.update(cookies)
        print("Logged in successfully.")
    else:
        print(f"Failed to log in: {response.status_code}")

def visit_notes():
    try:
        response = session.get('http://localhost:8081/notes')
        print(f"Visited /notes, status code: {response.status_code}")
        # Print the cookies to verify they are being handled
        print(f"Cookies after request: {session.cookies.get_dict()}")
    except requests.exceptions.RequestException as e:
        print(f"Error visiting /notes: {e}")

# Log in before starting the loop
login()

while True:
    visit_notes()
    # Wait for 5 minutes
    time.sleep(120)
