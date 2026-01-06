import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import database  # Importing your separate file

class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CineBook - Online Movie Booking System")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        # --- UI SETUP ---
        # Header
        tk.Label(root, text="🎬 CineBook Theaters", font=("Helvetica", 24, "bold"), bg="#333", fg="white").pack(fill=tk.X, pady=(0, 20))

        # Movie Selection
        tk.Label(root, text="Select a Movie:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        
        self.movie_listbox = tk.Listbox(root, height=5, font=("Arial", 12))
        self.movie_listbox.pack(pady=5, padx=20, fill=tk.X)
        self.movie_listbox.bind('<<ListboxSelect>>', self.on_movie_select)

        # Seat Frame
        self.seat_frame = tk.Frame(root, bg="#f0f0f0")
        self.seat_frame.pack(pady=20)
        
        # Legend
        legend_frame = tk.Frame(root, bg="#f0f0f0")
        legend_frame.pack(pady=5)
        tk.Label(legend_frame, text="🟩 Available", bg="#f0f0f0", fg="green").pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟥 Booked", bg="#f0f0f0", fg="red").pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="🟨 Selected", bg="#f0f0f0", fg="#AAAA00").pack(side=tk.LEFT, padx=10)

        # Discount Section (New Feature)
        discount_frame = tk.Frame(root, bg="#f0f0f0")
        discount_frame.pack(pady=10)
        tk.Label(discount_frame, text="Promo Code:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT)
        self.promo_entry = tk.Entry(discount_frame, font=("Arial", 10))
        self.promo_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(discount_frame, text="(Try: STUDENT10 or WELCOME50)", bg="#f0f0f0", fg="gray", font=("Arial", 8)).pack(side=tk.LEFT)

        # Booking Button
        self.book_btn = tk.Button(root, text="Confirm Booking", command=self.confirm_booking, state=tk.DISABLED, bg="#007bff", fg="white", font=("Arial", 12, "bold"))
        self.book_btn.pack(pady=20)

        # --- DATA LOADING ---
        self.selected_movie_id = None
        self.selected_seats = []
        self.movies = [] # Store movie data locally for easy access
        self.load_movies_to_ui()

    def load_movies_to_ui(self):
        # Fetch from database file
        raw_movies = database.get_all_movies()
        self.movies = raw_movies # Store [(id, title, price), ...]
        
        for movie in raw_movies:
            self.movie_listbox.insert(tk.END, f"{movie[1]} - ₹{movie[2]}")

    def on_movie_select(self, event):
        self.selected_seats = []
        self.book_btn.config(state=tk.DISABLED, text="Confirm Booking")
        
        selection = self.movie_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        self.selected_movie_id = self.movies[index][0] 
        self.refresh_seats()

    def refresh_seats(self):
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        # Fetch booked seats from database file
        booked_seats = database.get_booked_seats(self.selected_movie_id)

        rows = ['A', 'B', 'C', 'D', 'E']
        for r_idx, row_char in enumerate(rows):
            for c_idx in range(1, 6):
                seat_id = f"{row_char}{c_idx}"
                
                if seat_id in booked_seats:
                    btn = tk.Button(self.seat_frame, text=seat_id, width=5, bg="red", state=tk.DISABLED)
                else:
                    cmd = lambda s=seat_id: self.toggle_seat(s)
                    btn = tk.Button(self.seat_frame, text=seat_id, width=5, bg="lightgreen", command=cmd)
                    btn.seat_id = seat_id # Tag for finding later

                btn.grid(row=r_idx, column=c_idx, padx=5, pady=5)

    def toggle_seat(self, seat_id):
        for widget in self.seat_frame.winfo_children():
            if hasattr(widget, 'seat_id') and widget.seat_id == seat_id:
                if seat_id in self.selected_seats:
                    self.selected_seats.remove(seat_id)
                    widget.config(bg="lightgreen")
                else:
                    self.selected_seats.append(seat_id)
                    widget.config(bg="yellow")
        
        if self.selected_seats:
            self.book_btn.config(state=tk.NORMAL, text=f"Book {len(self.selected_seats)} Seat(s)")
        else:
            self.book_btn.config(state=tk.DISABLED, text="Confirm Booking")

    def confirm_booking(self):
        if not self.selected_seats: return

        name = simpledialog.askstring("Input", "Enter your Name:")
        if not name: return

        # 1. Get Price Info
        movie_data = database.get_movie_details(self.selected_movie_id)
        price_per_ticket = movie_data[0]
        movie_title = movie_data[1]
        
        total_price = price_per_ticket * len(self.selected_seats)

        # 2. Calculate Discount
        promo = self.promo_entry.get().upper().strip()
        discount = 0
        if promo == "WELCOME50":
            discount = 50
        elif promo == "STUDENT10":
            discount = int(total_price * 0.10)
        
        final_price = max(0, total_price - discount)

        # 3. Confirm Dialog
        msg = (f"Movie: {movie_title}\nSeats: {self.selected_seats}\nPrice: ₹{total_price}\nDiscount: -₹{discount}\nTotal: ₹{final_price}\n\nProceed?")
        if not messagebox.askyesno("Confirm", msg): return

        # 4. Save to Database
        for seat in self.selected_seats:
            database.add_booking(self.selected_movie_id, seat, name)

        # 5. Print Ticket to File
        self.print_ticket(name, movie_title, final_price)

        # Reset UI
        messagebox.showinfo("Success", "Booking Confirmed! Ticket Saved.")
        self.selected_seats = []
        self.promo_entry.delete(0, tk.END)
        self.refresh_seats()
        self.book_btn.config(state=tk.DISABLED, text="Confirm Booking")

    def print_ticket(self, name, movie, price):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"Ticket_{name}_{self.selected_seats[0]}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("================================\n")
            f.write("       CINEBOOK TICKET          \n")
            f.write("================================\n")
            f.write(f"Time:  {timestamp}\n")
            f.write(f"Name:  {name}\n")
            f.write(f"Movie: {movie}\n")
            f.write(f"Seats: {', '.join(self.selected_seats)}\n")
            f.write("--------------------------------\n")
            f.write(f"Total: ₹{price}\n")
            f.write("================================\n")

if __name__ == "__main__":
    database.setup_database()
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()