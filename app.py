from flask import Flask
from flask_restful import Api
import resources

app = Flask(__name__)
api = Api(app)
# bind resources to endpoints
api.add_resource(resources.CreateUser, '/api/createuser')
api.add_resource(resources.AuthenticateUser, '/api/authenticate')

if __name__ == '__main__':
    app.run(debug=True)
