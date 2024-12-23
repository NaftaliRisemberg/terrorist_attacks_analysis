from flask import Flask
from blueprints import *
app = Flask(__name__)

app.register_blueprint(attack_type_bp, url_prefix='/api')
app.register_blueprint(region_bp, url_prefix='/api')
app.register_blueprint(terror_groups_bp, url_prefix='/api')
app.register_blueprint(target_type_bp, url_prefix='/api')

@app.route('/')
def index():
    return jsonify('helo world')

if __name__ == '__main__':
    app.run(debug=True)

