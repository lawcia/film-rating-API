from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return '''<h3>welcome to film rating api</h3>
    <p>GET /api/v1/filmrating/movies/all </p>
    <p>returns ids and ratings of all movies</p>
    </br>
    <p>GET /api/v1/filmrating/movies/popular</p>
    <p>returns ids and ratings of all movies and sorts by highest ratings</p>
    </br>
    <p>GET /api/v1/filmrating/movies/unpopular</p>
    <p>returns ids and ratings of all movies and sorts by lowest ratings</p></br>

    <p>POST /api/v1/filmrating/movies?id=tt6320628&rating=2</p>
    <p> adds movie with id tt6320628 and rating 2 to the data store </p>
    '''


@app.route("/api/v1/filmrating/movies/all", methods=['GET'])
def get_movies():
    df = pandas.read_csv('data.csv')
    return df.to_json(orient='records')


@app.route("/api/v1/filmrating/movies/popular", methods=['GET'])
def sort_movies_popular_votes():
    df = pandas.read_csv('data.csv')
    new = df.sort_values(by=['rating', 'imdbID'], ascending=False)
    print('GET movies by popular vote')
    return new.to_json(orient='records')


@app.route("/api/v1/filmrating/movies/unpopular", methods=['GET'])
def sort_movies_unpopular_votes():
    df = pandas.read_csv('data.csv')
    new = df.sort_values(by=['rating', 'imdbID'])
    print('GET movies by unpopular vote')
    return new.to_json(orient='records')


@app.route("/api/v1/filmrating/movies", methods=['POST'])
def api_id():
    if 'id' and 'rating' in request.args:
        id = str(request.args['id'])
        rating = float(request.args['rating'])
        df = pandas.read_csv('data.csv')
        if df.loc[df['imdbID'] == id].empty:
            movie_df = pandas.DataFrame({'imdbID':[id],'rating':[rating]})
            new_df = df.append(movie_df, ignore_index=True, sort=False)
            new_df.to_csv('data.csv', index=False)
        else:
            i = list(df.imdbID[df.imdbID == id].index)
            position = int(i[0])
            df.update({'rating': {position:rating}})
            df.to_csv('data.csv', index=False)
    else:
        return jsonify({'error':True,'message':'Please enter movie id and rating'})
    return jsonify({'error':False,'message':'Added movie {0} with rating {1}'.format(id, rating)})


if __name__ == "__main__":
    app.secret_key = 'supersecretkey'
    app.run(debug=False)


