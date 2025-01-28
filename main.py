from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

@app.after_request
def add_header(response):
    # Disable caching for static files
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
