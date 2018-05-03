from recommender import get_recommendations, get_recommendations_by_genre, loadMovieRatings

import sys
if(len(sys.argv) == 3):
    user_id = sys.argv[1]
    n_recommendations = sys.argv[2]
    if(str.isdigit(n_recommendations)):
        mv_list = get_recommendations(user_id, int(n_recommendations))
        for item in mv_list:
            print(item[1]+" - "+str(item[0]))
    else:
        print('Invalid format error. The input must consist of intergers.')
elif(len(sys.argv) == 2):
    n_recommendations = sys.argv[1]
    if(str.isdigit(n_recommendations)):
        n_recommendations = int(n_recommendations)
    else:
        print('Invalid format error. The input must consist of intergers.')
    uinput = ''
    genres_list = []
    print('Type the genres you like or 0 to start the recommender algorithm')
    uinput = input()
    while(uinput != '0'):
        genres_list.append(uinput)
        uinput = input()
    mv_list = get_recommendations_by_genre(
        user_preference=genres_list, n=n_recommendations)
    for item in mv_list:
        print(item[1]+" - "+str(item[0]))
else:
    print('Invalid arguments size input. Please try again providing the correct number of arguments e.g. \
            \npython recommender.py [userid] [num of recomentaions]')
