# Book recommender engine

Given a dataset of book ratings, books and users, I first performed data exploration, cleansing (removing items with invalid data, outliers, irrelevant implicit ratings, duplicates, merging variations and editions of the same book, users with no ratings, double ratings, ...) and preparation (normalization, formatting, ...) using pandas and numpy libraries. This resulting dataset is then sent via MySQL database to a collaborative filtering recommender engine (supporting different kinds of similarities).

To run, enter the user id of the user you want to get recommendations for and then run

``
python3.6 main.py
``.

The dataset used can be found at http://www2.informatik.uni-freiburg.de/~cziegler/BX/
