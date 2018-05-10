from recommender import get_recommendations_by_user, get_recommendations_by_genre
import sys

'''
USAGE
-Recomendation by user-
The [userid] is a user already registered in the database.
python recommender.py user [num of recommendations] [userid]
python recommender.py user 10 9

-Recomendation by genre-
python recommender.py genre [num of recommendations] [list of genres...]
python recommender.py genre 10 Horror Thriller
'''

kwargs = sys.argv
mv_list = []
if(len(kwargs) > 3):
    n_recommendations = kwargs[2]
    if(str.isdigit(n_recommendations)):
        n_recommendations = int(n_recommendations)
    else:
        n_recommendations = 10

    # if recommendation by user
    if kwargs[1]=='user':
        user_id = kwargs[3]
        mv_list = get_recommendations_by_user(user=user_id, n=n_recommendations)

    # if recommendation by genre
    elif kwargs[1]=='genre':
        genres = [genre for genre in kwargs[3:]]
        mv_list = get_recommendations_by_genre(user_preference=genres, n=n_recommendations)


for movie in mv_list:
    print("{movie} - {score}".format(movie=movie[1], score=movie[0]))
