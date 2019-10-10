from flask_restful import Resource, reqparse
import psycopg2
from flask import jsonify
import json

# create db instance
with psycopg2.connect(host="ec2-174-129-241-114.compute-1.amazonaws.com",
                      database="de3svla4ul5cod",
                      user="tbnidoxxgmmhoq",
                      password="cbc6e81fbe5593300fa93386ae6e47497595a23f0b60726ff55c47c54b306f97"
                      ) as db:
    curr = db.cursor()


    # === resources for the api ===
    class CreateUser(Resource):
        def post(self):
            __doc__ = '''
            create user:
            required parameters -
             1. name 
             2.last name 
             3.email
             4.password(sha1 hashed) 
             5.phone number 
             6.address 
             7.state
             8.city 
             9.blood group
             10.age
            '''
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('first_name', type=str, help='first name address of user')
                parser.add_argument('last_name', type=str, help='last name of user')
                parser.add_argument('email', type=str, help='Email address of user')
                parser.add_argument('password', type=str, help='Password of user in SHA')
                parser.add_argument('phone_number', type=str, help='phone no. of user')
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

                sql = "INSERT INTO public.user (first_name, last_name, email, password," \
                      " phone_number, address, state, city, blood_grp, age) " \
                      "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                    f_name, l_name, email, password, p_number, address, state, city, blood_grp, age)
                curr.execute(sql)
                db.commit()
                return {'status': 'user created',
                        'created': True}
            except Exception as e:
                return {'error': str(e),
                        'created': False}


    class AuthenticateUser(Resource):
        def post(self):
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('email', type=str, help='Email of user')
                parser.add_argument('password', type=str, help='password of user')
                arg = parser.parse_args()

                username = arg['email']
                password = arg['password']

                sql = "select password from public.user where email ='{}'".format(str(username))
                curr.execute(sql)
                db.commit()
                res = curr.fetchone()
                if res is None:
                    return {'error': 'User does not exist',
                            'Authenticated': False}
                else:
                    password_db = res[0]
                    if password == password_db:
                        return {'Authenticated': True}
                    else:
                        return {'Authenticated': False}
            except Exception as e:
                return {'error': str(e),
                        'Authenticated': False}


    class FindUser(Resource):
        def get(self):
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('city', type=str, help='City')
                arg = parser.parse_args()
                city = arg['city']

                sql = "Select first_name,last_name,blood_grp,email from public.user where city ='{}'".format(str(city))
                curr.execute(sql)
                db.commit()
                res = curr.fetchall()

                return_list = []
                for result in res:
                    dic = {}
                    dic['first_name'] = result[0]
                    dic['last_name'] = result[1]
                    dic['blood_grp'] = result[2]
                    dic['email'] = result[3]
                    return_list.append(dic)

                return jsonify(return_list)
            except Exception as e:
                return {'error': str(e)}


    class DeleteUser(Resource):
        def get(self):
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('email', type=str, help='Email of user')
                arg = parser.parse_args()
                email = arg['email']

                sql = "DELETE FROM public.user WHERE email = '{}'".format(str(email))
                curr.execute(sql)
                db.commit()
                return {'status': 'user deleted',
                        'deleted': True}
            except Exception as e:
                return {'error': str(e),
                        'deleted': False}


    class CreateRequest(Resource):
        def post(self):
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('from', type=str, help='Email of user')
                parser.add_argument('to', type=str, help='email of requested user')
                arg = parser.parse_args()

                from_id = arg['from']
                to_id = arg['to']

                sql = "insert into public.request(from_id, to_id) values ('{}','{}')".format(from_id, to_id)
                curr.execute(sql)
                db.commit()
                return {'status': 'request created',
                        'created': True}
            except Exception as e:
                return {'error': str(e),
                        'created': False}


    class UpdateRequest(Resource):
        def post(self):
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('from', type=str, help='Email of user')
                parser.add_argument('to', type=str, help='email of requested user')
                parser.add_argument('accepted', type=str, help='Email of user')
                arg = parser.parse_args()

                from_id = arg['from']
                to_id = arg['to']
                accepted = arg['accepted']

                sql = "update public.request set accepted='{}' where from_id='{}' and to_id='{}'".format(accepted,
                                                                                                         from_id, to_id)
                curr.execute(sql)
                db.commit()
                return {'status': 'request updated',
                        'updated': True}
            except Exception as e:
                return {'error': str(e),
                        'updated': False}
