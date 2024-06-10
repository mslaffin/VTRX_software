# utils.py
import sys
import subprocess
import os
import tkinter as tk
from tkinter import messagebox, ttk
import datetime

class MessagesFrame:
    MAX_LINES = 100  # Maximum number of lines to keep in the widget at a time

    def __init__(self, parent):
        self.frame = tk.Frame(parent, borderwidth=2, relief="solid")
        self.frame.pack(fill=tk.BOTH, expand=True)  # Make sure it expands and fills space

        # Add a title to the Messages & Errors frame
        label = tk.Label(self.frame, text="Messages & Errors", font=("Helvetica", 10, "bold"))
        label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Configure the grid layout to allow the text widget to expand
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        # Create a Text widget for logs
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, font=("Helvetica", 8))
        self.text_widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)

        # Create a button to clear the text widget
        self.clear_button = tk.Button(self.frame, text="Clear Messages", command=self.confirm_clear)
        self.clear_button.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Redirect stdout to the text widget
        sys.stdout = TextRedirector(self.text_widget, "stdout")

    def write(self, msg):
        """ Write message to the text widget and trim if necessary. """
        self.text_widget.insert(tk.END, msg)
        self.trim_text()

    def log_message(self, msg):
        """ Log a message with a timestamp to the text widget """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] - {msg}\n"
        self.text_widget.insert(tk.END, formatted_message)
        self.text_widget.see(tk.END)

    def flush(self):
        """ Flush method needed for stdout redirection compatibility. """
        pass

    def trim_text(self):
        ''' Remove the oldest lines to maintain a maximum number of lines in the text widget. '''
        line_count = int(self.text_widget.index('end-1c').split('.')[0])
        if line_count > self.MAX_LINES:
            line_diff = line_count - self.MAX_LINES
            self.text_widget.delete('1.0', f'{line_diff}.0')

    def confirm_clear(self):
        ''' Show a confirmation dialog before clearing the text widget '''
        if messagebox.askokcancel("Clear Messages", "Do you really want to clear all messages?"):
            self.text_widget.delete('1.0', tk.END)


class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, msg):
        self.widget.insert(tk.END, msg, (self.tag,))
        self.widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # Needed for compatibility

class SetupScripts:
    def __init__(self, parent):
        self.parent = parent
        self.setup_gui()

    def setup_gui(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(pady=10, fill=tk.X)

        # Label
        tk.Label(self.frame, text="Select Config Script:").pack(side=tk.LEFT)

        # Dropdown Menu for selecting a script
        self.script_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self.frame, textvariable=self.script_var)
        self.dropdown.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.populate_dropdown()

        # Execute Button
        self.execute_button = tk.Button(self.frame, text="Execute", command=self.execute_script)
        self.execute_button.pack(side=tk.RIGHT, padx=5)

    def populate_dropdown(self):
        script_dir = os.path.join(os.path.dirname(sys.executable), 'scripts')
        if os.path.exists(script_dir):
            script_dir = 'scripts/'
            # List all .py files in the 'scripts/' directory
            scripts = [file for file in os.listdir(script_dir) if file.endswith('.py')]
            self.dropdown['values'] = scripts
            if scripts:
                self.script_var.set(scripts[0])  # Set default selection

    def execute_script(self):
        script_name = self.script_var.get()
        if script_name:
            script_path = os.path.join('scripts', script_name)
            try:
                # Execute the script
                subprocess.run(['python', script_path], check=True)
                print(f"Script {script_name} executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while executing {script_name}: {e}")

class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.tip_window = None

    def enter(self, event=None):
        self.show_tip()

    def leave(self, event=None):
        self.hide_tip()

    def show_tip(self):
        x, y, _cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
