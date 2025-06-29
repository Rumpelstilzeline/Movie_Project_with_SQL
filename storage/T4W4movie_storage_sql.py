from sqlalchemy import create_engine, text
import os

# Define the database URL

# Get the absolute path to the 'data' folder relative to this file's parent directory
data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
db_path = os.path.join(data_folder, "movies.db")

# Use the absolute path in the DB URL (note: 3 slashes for absolute path)
DB_URL = f"sqlite:///{db_path}"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist (with poster_url column)
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    connection.commit()


def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database with poster URL."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("""
                    INSERT INTO movies (title, year, rating, poster_url)
                    VALUES (:title, :year, :rating, :poster_url)
                """),
                {"title": title, "year": year, "rating": rating, "poster_url": poster_url}
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding movie '{title}': {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()
        if result.rowcount == 0:
            print(f"No movie found with title '{title}'.")
        else:
            print(f"Movie '{title}' deleted successfully.")


def update_movie(title, rating, year):
    """Update a movie's rating and year in the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                UPDATE movies
                SET rating = :rating, year = :year
                WHERE title = :title
            """),
            {"title": title, "rating": rating, "year": year}
        )
        connection.commit()
        if result.rowcount == 0:
            print(f"No movie found with title '{title}'.")
        else:
            print(f"Movie '{title}' updated successfully.")


def list_movies():
    """List all movies in the database, including poster URL."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies")
        )
        movies = result.fetchall()
        return [
            {
                "title": row[0],
                "year": row[1],
                "rating": row[2],
                "poster_url": row[3]
            }
            for row in movies
        ]