# Recommender System

## Getting Started

### Prerequisites

You should have the basic installation of Python-3 installed, no third-party library is required.

Although it has not been tested under Python-2, it might run without a hitch.


#### Execute
The following arguments are required to run each algorithm:
- Item Correlation
```
python recommender.py user [# recommendations] [userid]
```
- Genre Correlation
```
python recommender.py genre [num of recommendations] [list of genres...]
```

### Method

Item-based collaborative filtering is a form of collaborative filtering for recommender systems based on the similarity between items calculated using people's ratings of those items.

|![Item-based filter](/imgs/item_based.JPG)|
|:--:|
|*Figure 1: Item-based Recommender System*|

#### Item-by-item similarity

A collaborative filtering approach based on user preferences involves
the following three steps:

1. Calculate the correlation coefficient using user preferences;
2. Choose neighbors of user A who wants recommendations (neighbors are a group of users who have similar preferences to user A)
3. Estimate the preference for a specific item based on the neighbors ratings.

##### Step 1: Calculate the correlation coefficient using user preferences

First, the system executes a model-building stage by finding the similarity between all pairs of items for all users to the one given by input. This similarity function can take many forms, such as correlation between ratings or cosine of those rating vectors.

|![Pearson](/imgs/pearson_correlation.png)|
|:--:|
|*Equation 1: Pearson Correlation algorithm*|

In equation 1 and 2, X is a given user to find recommendations and X̅ is the mean ratings of that user X times the same operation for each other user in the database. Then we have the standard deviation from the users in the denominator. The Pearson correlation coefficient returns a value between -1 and 1.

|![Pearson](/imgs/pearsonv2.svg)|
|:--:|
|*Equation 2: Rearranged algorithm*|

###### P-score interpretation (for positive ou negative P-score)
- 0.9 or above means a very strong correlation.
- 0.7 up to 0.9 means a strong correlation.
- 0.5 up to 0.7 means a moderate correlation.
- 0.3 up to 0.5 means a weak correlation.
- 0 up to 0.3 is a meaningless correlation.

##### Step 2: Choose neighbors of user A who wants recommendations

In the next step, neighbors are chosen using the results of step 1. In this step, a number of the highest correlation coefficient valued neighbors is selected.

##### Step 3: Estimate the preference for a specific item based on the neighbors ratings

The final step is to predict preferences based on the ratings of neighbors. This step uses Eq. (3):

|![Preditec Preference](/imgs/predicted_pref.jpg)|
|:--:|
|*Equation 3: Predicted Preference for a given movie*|

Where X is the average rating of user X and Yn is the rating by each other user for the nth item. Y is the average rating by the neighbors of X of the current item. Finally, Pxy is the Pearson correlation coefficient between X and another user Y. The result P in Eq. (3) is the predicted value of an item for user X.

#### Genre-by-genre similarity

Genre correlations are initially calculated based on genre combinations of each movie in a database. All movies in the movie database have at least one genre. In other words, each movie has a genre combination composed of at least one genre. We repeat this procedure for all movies in the database and calculate the genre correlations by percentages. This way we will build a genre correlation percentage matrix.

The system selects a genre and counts the number of the other genres for each movie. For example, in figure 2 if movie A has the genre combination of G1, G2, and G5, then G1 is selected as a criterion genre and we increase the combination counting with G2 and G5 by 1. Next, G2 is selected as a criterion genre and we increase
the combination counting with only G5 by 1 again.

|![Genre Correlation](/imgs/genre_points.jpg)|
|:--:|
|*Figure 2: Genre correlation for each movie*|

If the selected criterion genre of the movie is one of the
user’s preferred genres, Eq. (4) is used, Eq (5) otherwise. In Eqs. (4) and (5), up refers to the set of the user’s preferred genres while mg indicates the genre list of a specific movie. When ri=j the genre correlation is equal to 1. When ri!=j is the genre correlation of genre i and genre j which are  already calculed in the genres matrix.

|![Genre Correlation](/imgs/recommendation_points.jpg)|
|:--:|
|*Equation 4 and 5: Recommendations points equation*|



#### References

The implementation is based on:

Sang-Min Choi, Sang-Ki Ko, Yo-Sub Han(2012). A movie recommendation algorithm based on genre correlations. Expert Systems with Applications, Volume 39, Issue 9, ISSN 0957-4174.
