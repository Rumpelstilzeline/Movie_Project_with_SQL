import statistics
import random
import difflib  #for fuzzy matching
import matplotlib.pyplot as plt
import sys # for quit_program function
import T4W4movie_storage_sql as storage
import requests
import os

OMDB_API_KEY = "3ec8c4da"


# ANSI escape sequence for red color
RED = "\033[91m"
RESET = "\033[0m"


def fetch_movie_from_omdb(title):
    """Fetch movie data from OMDb API by title."""
    try:
        response = requests.get(
            "http://www.omdbapi.com/",
            params={"t": title, "apikey": OMDB_API_KEY}
        )
        response.raise_for_status()
        data = response.json()

        if data["Response"] == "False":
            print(f"{RED}Movie not found: {data.get('Error')}{RESET}")
            return None

        return {
            "title": data["Title"],
            "year": int(data["Year"]),
            "rating": float(data.get("imdbRating", 0.0)),
            "poster_url": data.get("Poster", "")
        }

    except requests.exceptions.RequestException as e:
        print(f"{RED}Error fetching movie data: {e}{RESET}")
        return None


def quit_program():
    """User can quit the program"""
    print("Bye!")
    sys.exit(0)


def command_list_movies():
    """List all movies in the database with release year and rating."""
    movies = storage.list_movies()  # This now refers to the imported SQL version
    print(f"{len(movies)} movies in total")

    for movie in movies:
        title = movie["title"]
        year = movie["year"]
        rating = movie["rating"]
        print(f"{title} ({year}): {rating}")

    pause()


def command_add_movie():
    """Add a new movie by fetching its info from OMDb API using only the title."""
    title_input = input("Enter the movie title to add: ").strip()

    if not title_input:
        print(f"{RED}Error: Movie title cannot be empty.{RESET}")
        pause()
        return

    movie_data = fetch_movie_from_omdb(title_input)

    if not movie_data:
        print(f"{RED}Failed to add movie. Check title or try again later.{RESET}")
    else:
        # Use the add_movie() from T4W4movie_storage_sql.py
        storage.add_movie(
            movie_data["title"],
            movie_data["year"],
            movie_data["rating"],
            movie_data["poster_url"]
        )
        print(f"Movie '{movie_data['title']}' added successfully.")

    pause()


def delete_movie():
    """User enters the name of the movie to be deleted and the movie is deleted from the database
    If the user enters an invalid movie name, an error message is displayed."""
    movies = storage.list_movies()
    titles = [movie['title'] for movie in movies]

    if user_input_deletion not in titles:
        print(f"{RED}Error: The movie is not in the database.{RESET}")
    else:
        print(f"{user_input_deletion} is being deleted.")
        storage.delete_movie(user_input_deletion)

def update_movie():
    """User enters the name of the movie to be updated and the movie is updated in the database
    If the user enters an invalid movie name, an error message is displayed."""

    movies = storage.list_movies()

    movie_titles = [movie['title'] for movie in movies]

    user_input_enter_movie = input("Please enter the name of the movie that you want to update: ")

    if user_input_enter_movie not in movie_titles:
        print(f"{RED}Error: The movie is not in the database.{RESET}")
    else:
        try:
            user_input_update_rating = float(input("Enter the new rating for the movie: "))
            user_input_update_year = int(input("Enter the new year of release for the movie: "))

            storage.update_movie(user_input_enter_movie, user_input_update_rating, user_input_update_year)
        except ValueError:
            print(f"{RED}Error: The rating must be a number.{RESET}")

    pause()


def movie_stats():
    """Calculate and display statistics about the movies in the database"""
    movies = storage.list_movies()  # Returns a dict

    if not movies:
        print(f"{RED}No movies in the database to calculate statistics.{RESET}")
        pause()
        return

    rating_list = [movie["rating"] for movie in movies]

    avg_rating = statistics.mean(rating_list)
    median_rating = statistics.median(rating_list)
    max_rating = max(rating_list)
    min_rating = min(rating_list)


    best_movies = [movie["title"] for movie in movies if movie["rating"] == max_rating]
    worst_movies = [movie["title"] for movie in movies if movie["rating"] == min_rating]

    print(f"The average rating of all movies "
          f"in the database is {avg_rating:.2f}")
    print(f"The median rating of all movies in the database is {median_rating:.2f}")
    # Join converts the output into a string, otherwise it would be a list
    print(f"The best rating is {max_rating:.2f} for movie(s):")
    print(", ".join(best_movies))

    print(f"The worst rating is {min_rating:.2f} for movie(s):")
    print(", ".join(worst_movies))

    pause()


def random_movie():
    """Picks a random movie from the database and displays its name and rating"""
    movies = storage.list_movies()

    if not movies:
        print(f"{RED}No movies in the database to choose from.{RESET}")
        pause()
        return

    chosen_movie = random.choice(movies)
    title = chosen_movie["title"]
    rating = chosen_movie["rating"]

    print(f"The chosen movie is {title} with its rating {rating}")

    pause()


def search_movie():
    """Search for a movie in the database by title.
    If the exact title is not found, it tries to find a close match."""

    movies = storage.list_movies()

    if not movies:
        print(f"{RED}No movies in the database to search.{RESET}")
        pause()
        return

    search_string = input("Which movie are you looking for: ").lower()
    found = False

    # Create mappings for case-insensitive search
    original_titles = {movie["title"].lower(): movie["title"] for movie in movies}
    lowercase_movies = {movie["title"].lower(): movie for movie in movies}

    for lowercase_title, movie_info in lowercase_movies.items():    # movie_info is the inner dictionary
        if search_string in lowercase_title:
            original_title = original_titles[lowercase_title]
            rating = movie_info["rating"]                           # Accessing the value of "rating" in the inner dict
            year = movie_info["year"]
            print(f"{original_title} ({year}), Rating: {rating}")
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
                year = lowercase_movies[match]["year"]
                print(f"{original_title} ({year}), Rating: {rating}")
        else:
            print(f"{RED}No movies matched your search.{RESET}")

    pause()


def sort_movie_rating():
    """Sort movies by rating in descending order"""
    movies = storage.list_movies()  # Returns a list of dicts

    if not movies:
        print(f"{RED}No movies in the database to sort.{RESET}")
        pause()
        return

    # reverse=True sorts in decending order
    sorted_movies = sorted(
        movies, key=lambda movie: movie["rating"], reverse=True
    )
    for movie in sorted_movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")

    pause()


def sort_movie_year():
    """Sort movies by year in descending or ascending order, depending on the user's choice.
    It displays an error message if the user enters an invalid choice."""
    movies = storage.list_movies()  # Returns a list of dicts

    if not movies:
        print(f"{RED}No movies in the database to sort.{RESET}")
        pause()
        return

    while True:
        choice_order = input("Do you want the latest movies first? (Y/N): ").strip().lower()

        if choice_order == 'y':
            sorted_movies = sorted(movies, key=lambda movie: movie["year"], reverse=True)
            for movie in sorted_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
            break

        elif choice_order == 'n':
            sorted_movies = sorted(movies, key=lambda movie: movie["year"], reverse=False)
            for movie in sorted_movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
            break

        else:
            print('Please enter "Y" or "N".')  # Custom error message

    pause()


def filter_movies():
    """User can filter movies by minimum rating, start year and end year. Not yet implemented."""
    movies = storage.list_movies()  # Returns a list of dicts
    print("Functionality will soon be added.")

    pause()


def create_rating_histogram():
    """If the database is not empty, create a histogram of the ratings and saves it to a file."""
    movies = storage.list_movies()  # Returns a list of dicts

    if not movies:
        print(f"{RED}No movies in the database to generate a histogram.{RESET}")
        pause()
        return

    # Extract ratings
    ratings = [movie["rating"] for movie in movies]

    filename = input("Enter the filename to save the histogram (e.g., ratings.png): ").strip()

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


def generate_website():
    """Generate an HTML website using movie data and template."""
    movies = storage.list_movies()
    html_cards = ''
    for movie in movies:
        title = movie["title"]
        year = movie["year"]
        rating = movie["rating"]
        poster = movie["poster_url"]

        html_cards += f"""
        <div class="movie-card">
            <h2>{title}</h2>
            <p>Year: {year}</p>
            <p>Rating: {rating}</p>
            <img src="{poster}" alt="{title} poster" class="movie-poster">
        </div>
        """

    try:
        with open("index_template.html", "r") as f:
            template = f.read()
    except FileNotFoundError:
        print("Error: index_template.html not found.")
        return

    final_html = template.replace("__TEMPLATE_MOVIE_GRID__", html_cards)

    with open("index.html", "w") as f:
        f.write(final_html)

    print("✅ Website generated as index.html.")

    pause()


def pause():
    """Pause function (return to main menu with ENTER) that is implemented in all other functions of the menu"""
    input("Press ENTER to continue: ")


def main():
    """Contains the dictionary and the menu options.
    Asks for user input and calls the corresponding function."""

    menu_options = {        #for mapping the input of the user with an action
        0: quit_program,
        1: command_list_movies,
        2: command_add_movie,
        3: delete_movie,
        4: update_movie,
        5: movie_stats,
        6: random_movie,
        7: search_movie,
        8: sort_movie_rating,
        9: sort_movie_year,
        10: filter_movies,
        11: create_rating_histogram,
        12: generate_website
    }

    while True:
        print(
            "********** My Movies Database **********\n\nMenu:\n"
            "0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n"
            "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
            "8. Movies sorted by rating\n9. Movies sorted by year\n"
            "10. Filter movies\n11. Create Rating Histogram\n12. Generate website\n"
        )
        user_menu_choice = int(input("Enter choice (0–12): "))
        print(f"Your choice is {user_menu_choice}.")

        action = menu_options.get(user_menu_choice)
        if action:
            action()
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")


if __name__ == "__main__":
    main()
