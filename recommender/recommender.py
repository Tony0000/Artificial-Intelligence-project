from collaborative_filtering import pearson_similarity
import heapq

# Build the ratings dictionary
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

def most_similar(movies_ratings, user, n_similar):
    scores = {}
    for u, r in movies_ratings.items():
        if user != u:
            p_score = pearson_similarity(movies_ratings, user, u)
            scores[u] = p_score

    heap = [(value, key) for key,value in scores.items()]
    largest = heapq.nlargest(n_similar, heap)
    return largest

def bestRecommendations(user, n_recommendations):
    movie_list = set()
    movies_ratings = loadMovieRatings()
    nlargest_ratings = most_similar(movies_ratings, user, 10)

    # item is a tuple composed of (sim_score, user_id)
    for item in nlargest_ratings:
        for mv in movies_ratings[item[1]]:
            if mv not in movies_ratings[user]:
                 movie_list.add(mv)

    movie_recommendations = []
    for mv in movie_list:
        weighted_score = 0
        n_users = 0
        for item in nlargest_ratings:
            if mv in movies_ratings[item[1]].keys():
                n_users += 1
                weighted_score += movies_ratings[item[1]][mv] * item[0]

        n = float(n_users)/float(len(nlargest_ratings))
        movie_recommendations.append((weighted_score*n, mv))

    # heap = [(value, key) for key,value in movie_recommendations.items()]
    highest = heapq.nlargest(n_recommendations, movie_recommendations)
    for item in highest:
        print(item[1]+" - "+str(item[0]))
    # print('\n\n')

import sys
if(len(sys.argv) == 3):
    user_id = sys.argv[1]
    n_recommendations = sys.argv[2]
    if(str.isdigit(n_recommendations)):
        bestRecommendations(user_id, int(n_recommendations))
    else:
        print('Invalid format error. The input must consist of intergers.')
else:
    print('Invalid arguments size input. Please try again providing the correct number of arguments e.g.\npython recommender.py [userid] [num of recomentaions]')
