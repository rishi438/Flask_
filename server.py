from flask import make_response, render_template
from app_build import create_app
from api.route_handler import api_routes
from api.tasks import init_celery

app, celery = create_app()
celery_scheduler = init_celery(celery)


with app.app_context():
    app.register_blueprint(api_routes, url_prefix="/api")
    

@app.route("/test",methods=["GET"])
def home():
    data = {
        "name": "UP and Running."
    }
    return make_response(render_template("/layouts/index.html", **data), 200)


if __name__ == "__main__":
    app.debug = True
    app.run()