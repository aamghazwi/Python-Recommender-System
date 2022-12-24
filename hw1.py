# Task 1: Reading Data


## Task 1.1
def read_ratings_data(f):
    movie_ratings_dict = {}
    for line in f.readlines():
        line = line.strip().split('|')
        movie, rating, user = line
        movie = movie.strip()
        rating = float(rating.strip())
        # print(line)
        if movie in movie_ratings_dict:
            movie_ratings_dict[movie].append(rating)
        else:
            movie_ratings_dict[movie] = [rating]
    f.close()
    return movie_ratings_dict


## Task 1.2
def read_movie_genre(f):
    movie_genre_dict = {}
    for line in f.readlines():
        line = line.strip().split('|')
        genre, movie_id, movie = line
        movie = movie.strip()
        genre = genre.strip()
        # print(line)
        movie_genre_dict[movie] = genre
    f.close()
    return movie_genre_dict


# Task 2: Processing Data


## Task 2.1
def create_genre_dict(movie_genre_dict):
    genre_movie_dict = {}
    for movie in movie_genre_dict:
        genre = movie_genre_dict[movie]
        if genre in genre_movie_dict:
            genre_movie_dict[genre].append(movie)
        else:
            genre_movie_dict[genre] = [movie]
    return genre_movie_dict


## Task 2.2
def calculate_average_rating(movie_ratings_dict):
    movie_avg_dict = {}
    for movie in movie_ratings_dict:
        ratings = movie_ratings_dict[movie]
        movie_avg_dict[movie] = round(sum(ratings) / len(ratings), 2)
    return movie_avg_dict


# Task 3: Recommendation


## Task 3.1: Popularity based
def get_popular_movies(movie_avg_dict, n=10):
    popular_movies = {}
    movies = list(movie_avg_dict.keys())
    movies.sort(key=lambda x: movie_avg_dict[x], reverse=True)
    movies_f = movies[:min(n, len(movies))]
    for movie in movies_f:
        popular_movies[movie] = movie_avg_dict[movie]
    return popular_movies


## Task 3.2: Threshold rating
def filter_movies(movie_avg_dict, threshold=3):
    filtered_movies = {}
    movies = list(movie_avg_dict.keys())
    movies_f = filter(
        lambda x: True if movie_avg_dict[x] >= threshold else False, movies)
    movies_f = list(movies_f)
    for movie in movies_f:
        filtered_movies[movie] = movie_avg_dict[movie]
    return filtered_movies


## Task 3.3: Popularity + Genre based
def get_popular_in_genre(genre, genre_movie_dict, movie_avg_dict, n=5):
    movie_avg_temp = {}
    movies = genre_movie_dict[genre]
    for movie in movies:
        movie_avg_temp[movie] = movie_avg_dict[movie]
    movie_avg_pop_in_genre = get_popular_movies(movie_avg_temp, n)

    return movie_avg_pop_in_genre


## Task 3.4: Genre Rating
def get_genre_rating(genre, genre_movie_dict, movie_avg_dict):
    genre_avg_temp = []
    movies = genre_movie_dict[genre]
    for movie in movies:
        genre_avg_temp.append(movie_avg_dict[movie])
    genre_avg = round(sum(genre_avg_temp) / len(genre_avg_temp), 2)

    return genre_avg


## Task 3.5: Genre Popularity
def genre_popularity(genre_movie_dict, movie_avg_dict, n=5):
    popular_genres = {}
    for genre in genre_movie_dict:
        genre_avg = get_genre_rating(genre, genre_movie_dict, movie_avg_dict)
        popular_genres[genre] = genre_avg

    popular_genres_f = {}
    genres = list(popular_genres.keys())
    genres.sort(key=lambda x: popular_genres[x], reverse=True)
    genres = genres[:min(n, len(genres))]
    for genre in genres:
        popular_genres_f[genre] = popular_genres[genre]
    return popular_genres_f


# Task 4: User Focused


## Task 4.1
def read_user_ratings(f):
    user_movie_dict = {}
    for line in f.readlines():
        line = line.strip().split('|')
        movie, rating, user = line
        movie = movie.strip()
        rating = float(rating.strip())
        user = int(user.strip())
        # print(line)
        if user in user_movie_dict:
            user_movie_dict[user].append((movie, rating))
        else:
            user_movie_dict[user] = [(movie, rating)]
    f.close()
    return user_movie_dict


## Task 4.2
### if two genre has the same rating then the max is the alphabetically lower one
def get_user_genre(user_id, user_movie_dict, movie_genre_dict):
    if user_id not in user_movie_dict:
        raise Exception('Invalid User ID')

    movie_ratings_pairs = user_movie_dict[user_id]
    genre_ratings_dict = {}
    for pair in movie_ratings_pairs:
        movie, rating = pair
        genre = movie_genre_dict[movie]
        if genre in genre_ratings_dict:
            genre_ratings_dict[genre].append(rating)
        else:
            genre_ratings_dict[genre] = [rating]
    for genre in genre_ratings_dict:
        ratings = genre_ratings_dict[genre]
        genre_ratings_dict[genre] = round(sum(ratings) / len(ratings), 2)

    # print(genre_ratings_dict)
    user_genre = max(sorted(genre_ratings_dict.keys()),
                     key=lambda x: genre_ratings_dict[x])
    # print(user_genre)

    return user_genre


## Task 4.3
def recommend_movies(user_id, user_movie_dict, movie_genre_dict,
                     movie_avg_dict):
    user_genre = get_user_genre(user_id, user_movie_dict, movie_genre_dict)
    user_rated_movies = [movie for (movie, rating) in user_movie_dict[user_id]]
    user_not_rated_movies = []
    for movie in movie_genre_dict:
        if movie_genre_dict[movie]==user_genre and movie not in user_rated_movies:
            user_not_rated_movies.append(movie)
    user_not_rated_movies.sort(key=lambda x:movie_avg_dict[x], reverse=True)
    recommended_movies =  user_not_rated_movies[:min(3,len(user_not_rated_movies))]

    # print("user genre:", user_genre)
    # print("user rated movies:",user_rated_movies)
    # print("user not rated movies",user_not_rated_movies)

    return recommended_movies

if __name__ == "__main__":
    # Task 1 demo

    # print('########')
    ratings_f_name = 'input/movieRatingSample.txt'
    ratings_f = open(ratings_f_name, 'r')
    movie_ratings_dict = read_ratings_data(ratings_f)
    # print(movie_ratings_dict)

    # print('########')
    genre_f_name = 'input/genreMovieSample.txt'
    genre_f = open(genre_f_name, 'r')
    movie_genre_dict = read_movie_genre(genre_f)
    # print(movie_genre_dict)

    # Task 2 demo

    # print('########')
    # print('Genre dictionary')
    genre_movie_dict = create_genre_dict(movie_genre_dict)
    # print(genre_movie_dict)

    # print('########')
    # print('Average movie rating')
    movie_avg_dict = calculate_average_rating(movie_ratings_dict)
    # print(movie_avg_dict)

    # Task 3 demo

    # print('########')
    # print('Popular movies')
    popular_movies = get_popular_movies(movie_avg_dict, 15)
    # print(popular_movies)

    # print('########')
    # print('Thershold ratings')
    filtered_movies = filter_movies(movie_avg_dict)
    # print(filtered_movies)

    # print('########')
    # print('Popularity + Genre based')
    genre = 'Adventure'
    movie_avg_pop_in_genre = get_popular_in_genre(genre, genre_movie_dict,
                                                  movie_avg_dict, 2)
    # print(movie_avg_pop_in_genre)

    # print('########')
    # print('Popularity + Genre based')
    genre = 'Adventure'
    genre_avg = get_genre_rating(genre, genre_movie_dict, movie_avg_dict)
    # print(genre, ':', genre_avg)

    # print('########')
    # print('Genre Popularity')
    popular_genres_f = genre_popularity(genre_movie_dict, movie_avg_dict, 7)
    # print(popular_genres_f)

    # Task 4 demo

    print('########')
    print('User ID dict')
    ratings_f_name = 'input/movieRatingSample.txt'
    ratings_f = open(ratings_f_name, 'r')
    user_movie_dict = read_user_ratings(ratings_f)
    print(user_movie_dict)

    print('########')
    print('User Genre')
    user_id = 43
    user_genre = get_user_genre(user_id, user_movie_dict, movie_genre_dict)
    print('user id:', user_id, ' genre:', user_genre)

    print('########')
    print('Recommend movies')
    user_id = 43
    recommended_movies = recommend_movies(user_id, user_movie_dict, movie_genre_dict,
                     movie_avg_dict)
    print(recommended_movies)
