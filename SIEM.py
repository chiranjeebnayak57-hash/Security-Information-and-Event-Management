# Copyright (c) 2026 Chiranjeeb Nayak.
# All rights reserved.

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import os

class SimpleSIEM:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Mini-SIEM Dashboard")
        self.root.geometry("800x500")

        # Configuration
        self.log_file = "server_logs.txt"
        self.monitoring = False
        self.keywords = ["FAILED", "ERROR", "CRITICAL", "UNAUTHORIZED"]

        # UI Setup
        self.setup_ui()

        # Create a dummy log file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("SIEM Log Monitor Initialized...\n")

    def setup_ui(self):
        # Top Control Panel
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        self.status_label = ttk.Label(control_frame, text="Status: Idle", foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.start_btn = ttk.Button(control_frame, text="Start Monitoring", command=self.start_monitor)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_monitor, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Simulate Attack", command=self.simulate_log).pack(side=tk.RIGHT)

        # Log Display Area
        display_frame = ttk.LabelFrame(self.root, text="Security Events")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_display = scrolledtext.ScrolledText(display_frame, state='disabled', bg="black", fg="lime")
        self.log_display.pack(fill=tk.BOTH, expand=True)

        # Tag configuration for coloring alerts
        self.log_display.tag_config("ALERT", foreground="red", font=('Helvetica', 10, 'bold'))

    def log_message(self, message, is_alert=False):
        self.log_display.configure(state='normal')
        tag = "ALERT" if is_alert else None
        self.log_display.insert(tk.END, f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n", tag)
        self.log_display.configure(state='disabled')
        self.log_display.yview(tk.END)

    def monitor_logic(self):
        """Background thread logic to read the file."""
        self.log_message("Monitoring started on: " + self.log_file)

        with open(self.log_file, "r") as f:
            # Move to the end of the file
            f.seek(0, os.SEEK_END)

            while self.monitoring:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                # Check for security keywords
                is_alert = any(key in line.upper() for key in self.keywords)
                self.log_message(line.strip(), is_alert)

                if is_alert:
                    # Logic for automated response could go here
                    print(f"ALERT: Security threshold triggered by: {line.strip()}")

    def start_monitor(self):
        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: ACTIVE", foreground="green")

        self.thread = threading.Thread(target=self.monitor_logic, daemon=True)
        self.thread.start()

    def stop_monitor(self):
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Idle", foreground="blue")

    def simulate_log(self):
        """Simulates an external application writing to the log file."""
        logs = [
            "INFO: User admin logged in.",
            "ERROR: FAILED password attempt for user 'root' from 192.168.1.50",
            "INFO: File system backup completed.",
            "CRITICAL: UNAUTHORIZED access detected in /etc/shadow"
        ]
        import random
        selected = random.choice(logs)
        with open(self.log_file, "a") as f:
            f.write(selected + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleSIEM(root)
    root.mainloop()
