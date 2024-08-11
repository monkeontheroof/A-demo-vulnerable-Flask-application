from website import create_app
from website.config import Config

# website package
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)