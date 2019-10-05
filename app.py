from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="blood_bank"
)

curr = db.cursor(buffered=True)


class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', type=str, help='first name address of user')
            parser.add_argument('last_name', type=str, help='last name of user')
            parser.add_argument('email', type=str, help='Email address of user')
            parser.add_argument('password', type=str, help='Password of user in SHA')
            parser.add_argument('phone_number', type=str, help='phone no. address of user')
            parser.add_argument('address', type=str, help='address of user')
            parser.add_argument('state', type=str, help='state address of user')
            parser.add_argument('city', type=str, help='city of user')
            parser.add_argument('blood_grp', type=str, help='blood group address of user')
            parser.add_argument('age', type=str, help='age of user')
            args = parser.parse_args()

            f_name = str(args['first_name'])
            l_name = str(args['last_name'])
            email = str(args['email'])
            password = str(args['password'])
            p_number = str(args['phone_number'])
            address = str(args['address'])
            state = str(args['state'])
            city = str(args['city'])
            blood_grp = str(args['blood_grp'])
            age = str(args['age'])

            sql = "INSERT INTO `user` (`first_name`, `last_name`, `email`, `password`, `phone_number`, `address`, `state`, `city`, `blood_grp`, `age`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                f_name, l_name, email, password, p_number, address, state, city, blood_grp, age)
            curr.execute(sql)
            db.commit()
            return {'status': 'user created'}
        except Exception as e:
            return {'error': str(e)}


class AuthenticateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email of user')
            parser.add_argument('password', type=str, help='password of user')
            arg = parser.parse_args()

            username = arg['email']
            password = arg['password']

            sql = "select password from user where email = '{}'".format(str(username))
            curr.execute(sql)
            db.commit()
            res = curr.fetchone()
            password_db = res[0]
            if password == password_db:
                return {'Authenticated': True}
            else:
                return {'Authenticated': False}
        except Exception as e:
            return {'error': str(e)}


api.add_resource(CreateUser, '/api/createuser')
api.add_resource(AuthenticateUser, '/api/authenticate')
if __name__ == '__main__':
    app.run(debug=True)
