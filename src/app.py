import tkinter as tk
import sqlite3
from tekstowo_scraper import song_scraper


class TekstowoScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("tekstowo.pl lyrics scraper")
        self.root.resizable(False, False)

        self.conn = sqlite3.connect("src/music_artists.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS artists (id INTEGER PRIMARY KEY, artist_name TEXT, url TEXT)"""
        )
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, pady=10)

        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10)
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10)

        self.search_label = tk.Label(self.top_frame, text="Search for an artist:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.top_frame)
        self.search_entry.pack()

        self.search_button = tk.Button(
            self.top_frame, text="Search", command=self.search_artists
        )
        self.search_button.pack()

        self.scrap_button = tk.Button(self.top_frame, text="Scrap", command=self.scrap)
        self.scrap_button.pack()

        self.results_label = tk.Label(self.left_frame, text="Search results:")
        self.results_label.pack()

        self.results_listbox = tk.Listbox(self.left_frame, width=40)
        self.results_listbox.pack()

        self.selected_label = tk.Label(self.right_frame, text="Selected artists:")
        self.selected_label.pack()

        self.selected_listbox = tk.Listbox(self.right_frame, width=40)
        self.selected_listbox.pack()

        self.add_button = tk.Button(
            self.left_frame, text="Add", command=self.add_artist
        )
        self.add_button.pack()

        self.remove_button = tk.Button(
            self.right_frame, text="Remove", command=self.remove_artist
        )
        self.remove_button.pack()

    def search_artists(self):
        search_term = self.search_entry.get()
        self.results_listbox.delete(0, tk.END)

        self.cursor.execute(
            "SELECT artist_name, id FROM artists WHERE artist_name LIKE ?",
            (search_term + "%",),
        )
        results = self.cursor.fetchall()

        for row in results:
            self.results_listbox.insert(tk.END, row[0] + " ID: " + str(row[1]))

    def add_artist(self):
        selected_artist = self.results_listbox.get(tk.ACTIVE)
        if selected_artist not in self.selected_listbox.get(0, tk.END):
            self.selected_listbox.insert(tk.END, selected_artist)

    def remove_artist(self):
        selected_index = self.selected_listbox.curselection()
        if selected_index:
            self.selected_listbox.delete(selected_index[0])

    def run(self):
        self.root.mainloop()

    def scrap(self):
        urls = []
        for artist in self.selected_listbox.get(0, tk.END):
            artist_id = int(artist.split()[-1])
            self.cursor.execute(
                "SELECT artist_name, url FROM artists WHERE id = ?", (artist_id,)
            )
            result = self.cursor.fetchone()
            urls.append(result)

        song_scraper(urls)


if __name__ == "__main__":
    root = tk.Tk()
    app = TekstowoScraperApp(root)
    app.run()
