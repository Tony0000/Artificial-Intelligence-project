# P-score interpretation (for positive ou negative P-score)
# 0.9 or above means a very strong correlation.
# 0.7 up to 0.9 means a strong correlation.
# 0.5 up to 0.7 means a moderate correlation.
# 0.3 up to 0.5 means a weak correlation.
# 0 up to 0.3 is a meaningless correlation.
from math import sqrt, pow

def pearson_similarity(movies_ratings, user1, user2):
    movies = []
    for movie in movies_ratings[user1]:
        if movie in movies_ratings[user2]:
            movies.append(movie)

    n_movies = float(len(movies))

    # no movies in common
    if(n_movies < 8):
        return 0

    sum1 = sum([movies_ratings[user1][movie] for movie in movies])
    sum2 = sum([movies_ratings[user2][movie] for movie in movies])

    sum1seq = sum([pow(movies_ratings[user1][movie], 2) for movie in movies])
    sum2seq = sum([pow(movies_ratings[user2][movie], 2) for movie in movies])

    pSum = sum([movies_ratings[user1][movie] * movies_ratings[user2][movie] for movie in movies])

    # Calculate p-score
    numerator = n_movies * pSum - (sum1 * sum2)
    denominator = sqrt(((n_movies * sum1seq) - pow(sum1, 2.0)) * (n_movies * sum2seq - pow(sum2, 2.0)))

    if(denominator == 0):
        return 0

    p_score = numerator/denominator
    return p_score