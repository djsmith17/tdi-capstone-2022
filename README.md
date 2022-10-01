# About this project
This project is the culmination of the work that I have performed for the completion of my data science certificate for [The Data Incubator](https://www.thedataincubator.com/) bootcamp. Specifically, this data science exploration is a Video Game Recommendation Engine. Harnessing data from the International Games Database ([IGDB](https://www.igdb.com/)), my recommendation engine provides suggestions for games you should try based on previous titles that you have enjoyed playing.

# Deployed Application
I have deployed the application on StreamLit's cloud services platform. Please give it a try and let me know what you think! [Video Game Recommendation Engine](https://djsmith17-tdi-capstone--video-game-recommendation-engine-qj8w1q.streamlitapp.com/)

# Motivation
These days, time is short and money is tight. It is vital that your next video game purchase gives you the most bang for your buck. I want your next game purchase to be one that creates life-long memories and will not be another $60 regret.

# IGDB
The Internal Games Database is a collaborative, user-generated database of the video games from years past, hot titles from today, and future games yet to be released. In total this database comprises over 200k game entries ranging from original titles, DLCS, remasters, and mods. Each game entry includes features such as title, platform, developer, genre, themes, ratings (both user and reviewer), and much more. From these features, I am specifically focused on the themes and genre categories and used machine learning models to identify clusters of games of similar features. 

# Recommendation Engine
The supervised machine learning tool that I have employed here is k-Nearest Neighbors (kNN) to identify features of each of these games and create relationships between each of the game entries. The model fits the dataset to a kNN using Genre and Themes as the features to cluster the data around.  

My application starts by asking you to select three video games that you have previously enjoyed playing, and from those inputs the Recommendation engine will identify other games that are in closest proximity to the combination of features for these games.  

At present this recommendation engine does not take any feedback to identify whether or not the recommendations were approrpiate, or if the games were enjoyed by the user. 

# Visualizations
To provide accessability to the outcomes of the process here are some visualizations representing summary data of the dataset.

## Game Themes
![Game Themes](images/visualization_theme.png?raw=true "Bar Plot of the Game Themes")

## Game Genres
![Game Genres](images/visualization_genre.png?raw=true "Bar Plot of the Game Genre")

## Scatter plot of 'User Rating' vs 'Critic Rating' for Action Adventure Games
![scatterplot](images/visualization_ratings.png?raw=true "Scatterplot")

* Note, not all games have received both a User Score and Critic Score. This scatterplot shows the game entries that have a value recorded for each feature