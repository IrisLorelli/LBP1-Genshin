from app import create_app

app = create_app()

if __name__ == '__main__':
    # Redireciona pro login por padrão
    app.run(debug=True)