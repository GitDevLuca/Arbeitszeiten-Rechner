import tkinter as tk
import time
from datetime import datetime, timedelta

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arbeitszeit")
        self.root.geometry("300x200+0+900")  # Positioniert das Fenster unten links

        # Label und Eingabefeld für die verbleibende Arbeitszeit
        self.entry_label = tk.Label(root, text="Verbleibende Zeit (HH:MM):")
        self.entry_label.pack()

        self.time_entry = tk.Entry(root)
        self.time_entry.pack()
        self.time_entry.insert(0, "08:24")  # Voreinstellung 8 Stunden und 24 Minuten

        self.set_button = tk.Button(root, text="Setzen", command=self.set_time)
        self.set_button.pack()

        # Zeit-Label
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 24))
        self.time_label.pack()

        # Voraussichtliche Endzeit
        self.end_time_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.end_time_label.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(root, text="Stopp", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT)

        self.running = False
        self.remaining_time = 0
        self.last_time = 0

    def set_time(self):
        # Eingabe der verbleibenden Zeit lesen
        time_str = self.time_entry.get()
        hours, minutes = map(int, time_str.split(':'))

        # Berechnung der verbleibenden Zeit in Sekunden
        self.initial_time = hours * 3600 + minutes * 60 - 30 * 60  # Abzug von 30 Minuten Mittagspause
        self.remaining_time = self.initial_time

        # Aktualisierung der Zeit- und Endzeitanzeige
        self.time_label.config(text=self.format_time(self.remaining_time))
        self.update_end_time()

    def update_time(self):
        if self.running and self.remaining_time > 0:
            current_time = time.time()
            elapsed = current_time - self.last_time
            self.last_time = current_time
            self.remaining_time -= elapsed

            if self.remaining_time <= 0:
                self.remaining_time = 0

            self.time_label.config(text=self.format_time(self.remaining_time))
            self.update_end_time()
        
        if self.remaining_time > 0:
            self.root.after(1000, self.update_time)

    def update_end_time(self):
        now = datetime.now()
        end_time = now + timedelta(seconds=self.remaining_time)
        self.end_time_label.config(text="Voraussichtliche Endzeit: " + end_time.strftime('%H:%M:%S'))

    def start_timer(self):
        if not self.running:
            self.running = True
            self.last_time = time.time()
            self.update_time()

    def stop_timer(self):
        if self.running:
            self.running = False

    def reset_timer(self):
        self.remaining_time = self.initial_time
        self.time_label.config(text=self.format_time(self.remaining_time))
        self.update_end_time()

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
