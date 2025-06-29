import json

def get_movies():
    """loads the JSON file and returns the movies"""
    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)  # no need for json.loads(file.read())
    return data["movies"]


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open("data.json", "w") as fileobj:
        json.dump({"movies": movies}, fileobj, indent=2)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {"rating": rating, "year_of_release": year}
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)

def update_movie(title, rating, year):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        movies[title]["year_of_release"] = year
        save_movies(movies)


