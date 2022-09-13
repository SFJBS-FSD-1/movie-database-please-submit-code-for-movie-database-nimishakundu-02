from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from http import HTTPStatus
from flask_migrate import Migrate
import os

class Config:
     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/moviesdb'

class Development_Config(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/moviesdb'


class Production_Config(Config):
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith('postgres://'):
        uri=uri.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = uri


env=os.environ.get("ENV","Development")
if env == "Production":
    config_str=Production_Config
else:
    config_str=Development_Config

app=Flask(__name__)
app.config.from_object(config_str)

api=Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/moviedb1'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:1234@localhost/moviesdb'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    year=db.Column(db.Integer,nullable=False)
    genre=db.Column(db.String(80),nullable=False)

    @staticmethod
    def add_movie(title,year,genre):
        new_movie=Movie(title=title,year=year,genre=genre)
        db.session.add(new_movie)
        db.session.commit()




    @staticmethod
    def get_movie():
        data=Movie.query.all()
        return data

    @staticmethod
    def get_movie_id(id):
        return Movie.query.filter_by(id=id).first()

    @staticmethod
    def get_movie_del(id):
        new_movie=Movie.query.filter_by(id=id).delete()
        db.session.commit()
        return new_movie

    @staticmethod
    def update_movie(id,title,year,genre):
        updatemovie = Movie.query.filter_by(id=id).first()
        if updatemovie:
            updatemovie.title=title
            updatemovie.year=year
            updatemovie.genre=genre
            db.session.commit()
        return updatemovie



class AllMovies(Resource):
    def post(self):
        data=request.get_json()
        Movie.add_movie(title=data["title"], year=data["year"], genre=data["genre"])
        print(data)
        return " "


    def get(self):
        data=Movie.get_movie()
        print(data)
        movielist=[]
        for moviedata1 in data:
            dictmove={'title':moviedata1.title,'year':moviedata1.year,'genre':moviedata1.genre}
            movielist.append(dictmove)
            return movielist

class one_movie(Resource):
    def get(self,id):
        data=Movie.get_movie_id(id)
        if data:
            print(data.title)
            print(data.genre)
            print(data.year)
            return jsonify({'title':data.title,'year':data.year,'genre':data.genre})
        else:
            return jsonify({'message': 'ID not found', 'status': 404})

    def delete(self,id):
        data=Movie.get_movie_del(id)
        if data:
            return jsonify({'message':'Movie deleted','Status':HTTPStatus.OK})
        else:
            return jsonify({'message':'Movie id not found','Status':HTTPStatus.NOT_FOUND})

    def put(self,id):
        data=request.get_json()
        print(data)
        response=Movie.update_movie(id,data["title"],data["year"],data["genre"])
        print(response)
        if response:
            return jsonify({"message": 'Movie info updated', "Status": HTTPStatus.OK})
        else:
            return jsonify({'message': 'Movie id not found', 'Status': HTTPStatus.NOT_FOUND})



        # for movieone in data:
        #     dictmovie={}
        #     print(movieone)
        #     if movieone.id == id:
        #         dictmovie['title']=movieone.title
        #         dictmovie['year']=movieone.year
        #         dictmovie['genre']=movieone.genre
        #         return jsonify(dictmovie)
        # else:
        #     return jsonify({'message':'ID not found','status':404})


api.add_resource(AllMovies,"/movies")
api.add_resource(one_movie,"/movies/<int:id>")
if __name__ == "__main__":
    app.run()

