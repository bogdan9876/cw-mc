from flask import Blueprint


def register_blueprints(app):
    from app.controllers.user_controller import user_blueprint
    from app.controllers.health_controller import health_blueprint
    from app.controllers.chat_controller import chat_blueprint
    from app.controllers.doctor_controller import doctor_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(health_blueprint)
    app.register_blueprint(chat_blueprint)
    app.register_blueprint(doctor_blueprint)
