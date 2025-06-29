import statistics
import random
import difflib  #for fuzzy matching
import matplotlib.pyplot as plt
import sys # for quit_program function

# ANSI escape sequence for red color
RED = "\033[91m"
RESET = "\033[0m"


def quit_program(movies):
    """User can quit the program"""
    print("Bye!")
    sys.exit(0)


def list_movies(movies):
    """List all movies in the database with release year and rating"""
    print(f"{len(movies)} movies in total")
    for movie_name in movies:
        movie = movies[movie_name]
        year = movie["year_of_release"]
        rating = movie["rating"]
        print(f"{movie_name} ({year}): {rating}")

    pause()


def add_movie(movies):
    """Add a new movie to the database with release year and rating"""
    movie_input = input("Enter new movie name: ")
    year_input = int(input("Enter new movie year: "))
    rating_input = float(input("Enter new movie rating: "))

    movies[movie_input] = {
        "rating": rating_input,
        "year_of_release": year_input
    }

    print(f"Movie {movie_input} successfully added")

    pause()


def delete_movie(movies):
    """User enters the name of the movie to be deleted and the movie is deleted from the database
    If the user enters an invalid movie name, an error message is displayed."""
    user_input_deletion = input("Please enter the name of the movie that you want to delete: ")

    if user_input_deletion not in movies:
        print(f"{RED}Error: The movie is not in the database.{RESET}")
    else:
        print(f"{user_input_deletion} is being deleted.")
        del movies[user_input_deletion]

    pause()
#Update Movie

def update_movie(movies):
    """User enters the name of the movie to be updated and the movie is updated in the database
    If the user enters an invalid movie name, an error message is displayed."""
    user_input_enter_movie = input("Please enter the name of the movie that you want to update: ")

    if user_input_enter_movie not in movies:
        print(f"{RED}Error: The movie is not in the database.{RESET}")
    else:
        try:
            user_input_update_rating = float(input("Enter the new rating for the movie: "))
            user_input_update_year = int(input("Enter the new year of release for the movie: "))

            movies[user_input_enter_movie]["rating"] = user_input_update_rating
            movies[user_input_enter_movie]["year_of_release"] = user_input_update_year
        except ValueError:
            print(f"{RED}Error: The rating must be a number.{RESET}")

    pause()


def movie_stats(movies):
    """Calculate and display statistics about the movies in the database"""
    rating_list = []
    for movie_name in movies:
        movie = movies[movie_name]
        rating = movie["rating"]
        rating_list.append(rating)
    avg_rating = statistics.mean(rating_list)
    median_rating = statistics.median(rating_list)
    max_rating = max(rating_list)
    min_rating = min(rating_list)

    best_movies = [title for title, info in movies.items() if info["rating"] == max_rating]
    worst_movies = [title for title, info in movies.items() if info["rating"] == min_rating]

    print(f"The average rating of all movies in the database is {avg_rating:.2f}")
    print(f"The median rating of all movies in the database is {median_rating:.2f}")
    # Join converts the output into a string, otherwise it would be a list
    print(f"The best rating is {max_rating:.2f} for movie(s):")
    print(", ".join(best_movies))

    print(f"The worst rating is {min_rating:.2f} for movie(s):")
    print(", ".join(worst_movies))

    pause()


def random_movie(movies):
    """Picks a random movie from the database and displays its name and rating"""
    list_of_movies = []

    for movie in movies.keys():
        list_of_movies.append(movie)

    chosen_movie = random.choice(list_of_movies)
    rating_of_chosen_movie = movies[chosen_movie]['rating']

    print(f"The chosen movie is {chosen_movie} with its rating {rating_of_chosen_movie}")

    pause()


def search_movie(movies):
    """Search for a movie in the database by title.
    If the exact title is not found, it tries to find a close match."""
    original_titles = {key.lower(): key for key in movies}
    lowercase_movies = {key.lower(): value for key, value in movies.items()}

    search_string = input("Which movie are you looking for: ").lower()
    found = False

    for lowercase_title, movie_info in lowercase_movies.items():    # movie_info is the inner dictionary
        if search_string in lowercase_title:
            original_title = original_titles[lowercase_title]
            rating = movie_info["rating"]                           # Accessing the value of "rating" in the inner dict
            year = movie_info["year_of_release"]
            print(f"{original_title}, {rating}")
            found = True

    if not found:
        close_matches = difflib.get_close_matches(
            search_string, lowercase_movies.keys(), n=5, cutoff=0.5
        )

        if close_matches:
            print("No exact match found. Did you mean:")
            for match in close_matches:
                original_title = original_titles[match]
                rating = lowercase_movies[match]["rating"]
                year = lowercase_movies[match]["year_of_release"]
                print(f"{original_title}, {rating}")
        else:
            print(f"{RED}No movies matched your search.{RESET}")

    pause()



#Movies sorted by rating

def sort_movie_rating(movies):
    """Sort movies by rating in descending order"""
    # reverse=True sorts in decending order
    sorted_movies = sorted(
        movies.items(), key=lambda item: item[1]["rating"], reverse=True
    )
    for movie_name, info in sorted_movies:
        print(f"{movie_name} ({info['year_of_release']}): {info['rating']}")

    pause()


def sort_movie_year(movies):
    """Sort movies by year in descending or ascending order, depending on the user's choice.
    It displays an error message if the user enters an invalid choice."""

    while True:
        choice_order = input("Do you want the latest movies first? (Y/N): ").strip().lower()

        if choice_order == 'y':
            sorted_movies = sorted(
                movies.items(), key=lambda item: item[1]["year_of_release"], reverse=True
            )
            for movie_name, info in sorted_movies:
                print(f"{movie_name} ({info['year_of_release']}): {info['rating']}")
            break

        elif choice_order == 'n':
            sorted_movies = sorted(
                movies.items(), key=lambda item: item[1]["year_of_release"], reverse=False
            )
            for movie_name, info in sorted_movies:
                print(f"{movie_name} ({info['year_of_release']}): {info['rating']}")
            break

        else:
            print('Please enter "Y" or "N".')  # Custom error message

    pause()


def filter_movies(movies):
    """User can filter movies by minimum rating, start year and end year. Not yet implemented."""
    print("Functionality will soon be added.")

    pause()


def create_rating_histogram(movies):
    """If the database is not empty, create a histogram of the ratings and saves it to a file."""
    if not movies:
        print(f"{RED}No movies in the database to generate a histogram.{RESET}")
        pause()
        return

    ratings = []

    for movie_info in movies.values():
        ratings.append(movie_info["rating"])    #takes the rating from 'movies' and saves them into a list

    filename = input("Enter the filename to save the histogram (e.g., ratings.png): ")

    # Create histogram
    plt.figure(figsize=(8, 6))
    plt.hist(ratings, bins=10, edgecolor='black', color='skyblue')
    plt.title("Movie Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save plot to file
    plt.savefig(filename)
    plt.close()

    print(f"Histogram saved as '{filename}'")

    pause()


def pause():
    """Pause function (return to main menu with ENTER) that is implemented in all other functions of the menu"""
    input("Press ENTER to continue: ")


def main():
    """Contains the dictionary and the menu options.
    Asks for user input and calls the corresponding function."""

    movies = {
        "The Shawshank Redemption": {"rating": 9.5, "year_of_release": 1994},
        "Pulp Fiction": {"rating": 8.8, "year_of_release": 1994},
        "The Room": {"rating" : 3.6, "year_of_release": 2000},
        "The Godfather": {"rating" : 9.2, "year_of_release": 1972},
        "The Godfather: Part II": {"rating": 9.0, "year_of_release": 1980 },
        "The Dark Knight": {"rating": 9.0, "year_of_release": 2008},
        "12 Angry Men": {"rating": 8.9, "year_of_release": 2000},
        "Everything Everywhere All At Once": {"rating": 8.9, "year_of_release": 2014},
        "Forrest Gump": {"rating": 8.8, "year_of_release": 1994},
        "Star Wars: Episode V": {"rating": 8.7, "year_of_release": 2000}
    }

    menu_options = {        #for mapping the input of the user with an action
        0: quit_program,
        1: list_movies,
        2: add_movie,
        3: delete_movie,
        4: update_movie,
        5: movie_stats,
        6: random_movie,
        7: search_movie,
        8: sort_movie_rating,
        9: sort_movie_year,
        10: filter_movies,
        11: create_rating_histogram
    }


    while True:
        print(
            "********** My Movies Database **********\n\nMenu:\n"
            "0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n"
            "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
            "8. Movies sorted by rating\n9. Movies sorted by year\n"
            "10. Filter movies\n11. Create Rating Histogram\n"
        )
        user_menu_choice = int(input("Enter choice (0–11): "))
        print(f"Your choice is {user_menu_choice}.")

        action = menu_options.get(user_menu_choice)
        if action:
            action(movies)
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")


if __name__ == "__main__":
    main()
