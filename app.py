from flask import Flask
from flask_restful import Api
import resources

app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return "hello world"


# bind resources to endpoints
api.add_resource(resources.CreateUser, '/api/createuser')
api.add_resource(resources.FindUser, '/api/finduser')
api.add_resource(resources.DeleteUser, '/api/deleteuser')
api.add_resource(resources.AuthenticateUser, '/api/authenticate')

if __name__ == '__main__':
    app.run(debug=True)
