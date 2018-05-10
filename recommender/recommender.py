from collaborative_filtering import pearson_similarity
import math
import heapq

genres_dict = {
    0: 'unknown',
    1: 'Action',
    2: 'Adventure',
    3: 'Animation',
    4: 'Children',
    5: 'Comedy',
    6: 'Crime',
    7: 'Documentary',
    8: 'Drama',
    9: 'Fantasy',
    10: 'Film-Noir',
    11: 'Horror',
    12: 'Musical',
    13: 'Mystery',
    14: 'Romance',
    15: 'Sci-Fi',
    16: 'Thriller',
    17: 'War',
    18: 'Western'
}

'''Builds the movies ratings by user dictionary'''
def loadMovieRatings():
    movies = {}
    for line in open('data/ml-100k/u.item'):
        id, movie = line.split('|')[0:2]
        movies[id] = movie

    movieRatings = {}
    for line in open('data/ml-100k/u.data'):
        userID, movieID, rating = line.split('\t')[0:3]
        movieRatings.setdefault(userID, {})
        movieRatings[userID][movies[movieID]] = float(rating)

    return movieRatings

''' Finds the N most similar users to the given user '''
def __most_similar(movies_ratings, user, n_similar):
    scores = {}
    for u in movies_ratings.keys():
        if user != u:
            p_score = pearson_similarity(movies_ratings, user, u)
            scores[u] = p_score

    heap = [(value, key) for key,value in scores.items()]
    largests = heapq.nlargest(n_similar, heap)
    return largests

'''Builds a list of movie recommendations based on the user movies'''
def get_recommendations_by_user(user, n):
    movie_list = set()
    movies_ratings = loadMovieRatings()
    nlargest_ratings = __most_similar(movies_ratings, user, 10)
    print(movies_ratings[user])

    # Build a movies list to search for recommendations
    # Item is a tuple composed of (sim_score, user_id)
    for item in nlargest_ratings:
        for mv in movies_ratings[item[1]]:
            if mv not in movies_ratings[user]:
                 movie_list.add(mv)

    avg_users_score = dict()
    for user_id in nlargest_ratings:
        avg_users_score[user_id[1]] = sum(movies_ratings[user_id[1]].values()) / len(movies_ratings[user_id[1]])

    movie_recommendations = []
    for mv in movie_list:
        numerator = 0
        denominator = 0
        my_avg_score = sum(movies_ratings[user].values()) / len(movies_ratings[user])
        for user_id in nlargest_ratings:
            if mv in movies_ratings[user_id[1]].keys():
                p_score = user_id[0]
                numerator += p_score * (movies_ratings[user_id[1]][mv] - avg_users_score[user_id[1]])
                denominator += math.fabs(p_score)
        predicted_rating = 0
        if(denominator > 0):
            predicted_rating = my_avg_score + numerator/denominator
        movie_recommendations.append((predicted_rating, mv))

    highest = heapq.nlargest(n, movie_recommendations)
    return highest

'''Builds a list of movies recommendations using a matrix of genres correlation'''
def get_recommendations_by_genre(user_preference, n):
    w, h = 18, 18
    genre_matrix = [[0.0 for x in range(w)] for y in range(h)]
    titles_summary = dict()
    genres = []
    movies_ratings = loadMovieRatings()

    translator = {v: k for k, v in genres_dict.items()}

    for line in open('data/ml-100k/u.item'):
        id, title = line.split('|')[0:2]
        genres = line.split('|')[-19:-1]
        titles_summary[title] = dict()
        titles_summary[title]['id'] = id
        titles_summary[title]['sum_score'] = 0
        titles_summary[title]['num_score'] = 0

        title_genres = []
        for i in range(len(genres)):
            if(genres[i] == '1'):
                title_genres.append(genres_dict[i])
                for j in range(len(genres)):
                    if(genres[j] == '1' and i != j):
                        genre_matrix[i][j] += 1.0
        titles_summary[title]['genres'] = title_genres

    genre_matrix.pop(0)
    for i in range(w-1):
        genre_matrix[i].pop(0)
        for j in range(h-1):
            total = sum(genre_matrix[i])
            genre_matrix[i][j] = genre_matrix[i][j] / total

    for user in movies_ratings.keys():
        for movie in movies_ratings[user].keys():
            titles_summary[movie]['sum_score'] += movies_ratings[user][movie]
            titles_summary[movie]['num_score'] += 1

    movies_recommendations = []
    for title in titles_summary.keys():
        r_points = 0
        avg_score = titles_summary[title]['sum_score'] / \
            titles_summary[title]['num_score']
        for ug in user_preference:
            n_mg = len(titles_summary[title]['genres'])
            if ug in titles_summary[title]['genres']:
                n_mg -= 1
            for mg in titles_summary[title]['genres']:
                if(ug == mg):
                    r_points += 1
                else:
                    r_points += genre_matrix[translator[ug] -
                                             1][translator[mg]-1] / n_mg
        r_points = (r_points * avg_score) / len(user_preference)
        movies_recommendations.append((r_points, title))
        mv_list = heapq.nlargest(n, movies_recommendations)
    return mv_list
