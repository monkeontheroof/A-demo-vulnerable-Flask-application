from website import create_app
from dotenv import load_dotenv

load_dotenv()
# website package
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)