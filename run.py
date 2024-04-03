# local imports
from Project import create_app, db

# flask imports
from flask_migrate import Migrate
from flask_minify  import Minify


app = create_app()
Migrate(app, db)

Minify(app=app, html=True, js=False, cssless=False)

if __name__ == "__main__":
    app.run()
