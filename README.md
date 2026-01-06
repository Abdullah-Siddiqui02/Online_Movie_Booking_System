# 🎬 Online Movie Booking System

A Python-based desktop application featuring a GUI for seat selection, SQLite database integration, and a discount engine. Designed with a modular architecture separating frontend logic from backend data operations.

## 🚀 Key Features
- **Visual Seat Map:** Interactive grid showing real-time availability (Green/Red/Yellow indicators).
- **Modular Architecture:** Database logic is separated (`database.py`) from the UI (`main.py`) for better maintainability.
- **Discount Engine:** Supports promo codes (e.g., `STUDENT10`, `WELCOME50`) for dynamic pricing.
- **Ticket Generation:** Automatically generates a `.txt` receipt using File I/O upon successful booking.
- **Persistent Data:** Uses SQLite3 to store bookings and movie details permanently.

## 📊 UML Class Diagram
This diagram visualizes how the User Interface (`MovieBookingApp`) communicates with the Backend (`Database Module`).

```mermaid
classDiagram
    class MovieBookingApp {
        -root : Tk
        -selected_movie_id : int
        -selected_seats : List
        +__init__(root)
        +load_movies_to_ui()
        +on_movie_select(event)
        +refresh_seats()
        +toggle_seat(seat_id)
        +confirm_booking()
        +print_ticket(name, movie, price)
    }

    class DatabaseModule {
        +setup_database()
        +get_all_movies()
        +get_movie_details(movie_id)
        +get_booked_seats(movie_id)
        +add_booking(movie_id, seat, name)
    }

    MovieBookingApp ..> DatabaseModule : Imports & Calls