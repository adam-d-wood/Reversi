import ReversiEngine as engine
import tkinter as tk
import math

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.title("Reversi")
		self.pack(fill="both", expand=True, pady=10)
		self.create_widgets()
		self.create_game_settings()
		self.create_login()
		print(self.pack_slaves())

	def create_login(self):
		login_frame = tk.Frame(self.top_frame)
		login_frame.pack(side="left", padx=30, pady=10)
		self.name_frame = tk.Frame(login_frame)
		self.name_frame.pack(expand=True, fill="x", pady=2.5)
		self.username_label = tk.Label(self.name_frame, text="Username:", width=10, anchor="w")
		self.username_label.pack(side="left")
		self.username_field = tk.Entry(self.name_frame)
		self.username_field.pack(side="left", padx=10)
		self.pass_frame = tk.Frame(login_frame)
		self.pass_frame.pack(expand=True, fill="x", pady=2.5)
		self.password_label = tk.Label(self.pass_frame, text="Password:", width=10, anchor="w")
		self.password_label.pack(side="left")
		self.password_field = tk.Entry(self.pass_frame)
		self.password_field.pack(side="left", padx=10)
		self.submit_frame = tk.Frame(login_frame)
		self.submit_frame.pack(anchor="s", expand=True, pady=10)
		self.login_btn = tk.Button(self.submit_frame, text="Login")
		self.login_btn.pack(side="left", padx=10)
		self.signup_btn = tk.Button(self.submit_frame, text="Sign Up")
		self.signup_btn.pack(side ="left", padx=10)

	def create_game_settings(self):
		self.settings_frame = tk.Frame(self.top_frame)
		self.settings_frame.pack(side="right", padx=60, pady=10)
		self.strength_frame = tk.Frame(self.settings_frame)
		self.strength_frame.pack(fill="both", expand=True)
		self.strength_label = tk.Label(self.strength_frame, text="Normal Search Depth")
		self.strength_label.pack()
		self.strength_slider = tk.Scale(self.strength_frame, orient="horizontal", from_=1, to=10)
		self.strength_slider["command"] = self.display_time
		self.strength_slider.pack()
		self.time_label=tk.Label(self.strength_frame)
		self.display_time(None)
		self.time_label.pack()

	def display_time(self, a):
		depth = self.strength_slider.get()
		time = (3.7*math.e**(1.3*depth))/1000
		self.time_label["text"] = "Average thinking time: {}s".format(round(time, 2))

	def create_widgets(self):
		self.top_frame = tk.Frame(self)
		self.top_frame.pack(expand=True, fill="x", anchor="n")
		self.btn = Nice_Button(self, "Play")
		self.btn["command"] = self.run_game
		self.btn.pack(side="bottom")

	def run_game(self):
		print("yuh")
		root.destroy()
		reversi = engine.Reversi()
		reversi.main_loop()

class Nice_Button(tk.Button):
	def __init__(self, master, text):
		super().__init__(master)
		self["width"] = 0
		self["text"] = text
		self["padx"] = 30
		self["pady"] = 5
		self["relief"] = "groove"
		self["bg"] = "#3A506B"
		self["font"] = "Roboto 10"
		self["fg"] = "#ffffff"

 

root = tk.Tk()
root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
app = App(master=root)
app.mainloop()