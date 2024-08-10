from website import create_app

# website package
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8081)