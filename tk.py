import tkinter as tk
from tkinter import Toplevel, ttk, Tk
from PIL import ImageTk, Image
from tkinter import font as tk_font
from tkinter import messagebox
from game import Game


def about():
	messagebox.showinfo(
		"About Katro game",
		"What is Katro?\n\n"
		"The Katro has been present on the Big Island for many centuries. "
		"Malagasy, especially women and children, played this game in the afternoon, "
		"after household chores or school. "
		" This entertainment, although invented by Malagasy ancestors, would derive from the African mancala,"
		" a whole range of games of pebbles and seeds. The best known being awale. In the region of Fianarantsoa,"
		" the Bestileo, tireless players of Katro, consider it the traditional mancala.\n\n"
		"What is katro game? \n\n"
		"The purpose of this application is to play this Malagasy game on our computer, "
		"the game is currently for a single player who fights against the computer, "
		"but the two-player feature is coming!"
	)


def my_help():
	messagebox.showinfo(
		"Help?",
		"The Katro is played by two player. Each player has two rows of pawns. "
		"The one who starts the game chooses the hole as well as the direction he will want to start. "
		"He takes the pawns in his hole, distributes them successively in the other holes of his row. "
		"The Katro is played by two. Each player has two rows of pawns. "
		"The one who starts the game chooses the hole as well as the direction he will want to start. "
		"He takes the pawns in his hole, distributes them successively in the other holes of his row. "
	)


class Ui:
	def __init__(self):
		# config
		self.app = Tk()
		self.app.withdraw()
		self.top = Toplevel()
		self.top.title("Katro game")
		self.top.geometry("800x590")
		self.top.resizable(width=False, height=False)
		self.top.configure(bg="brown")
		self.frame = ttk.Frame(master=self.top)
		self.frame.grid()
		# component
		font = ("Helvetica", 26)
		helve14 = tk_font.Font(family='Helvetica', size=14, weight='bold')
		self.title_label = tk.Label(self.top, text="Katro game", font=font, background="brown", foreground="white")
		self.btn_play = tk.Button(self.top, text="Play", command=self.play, padx=15, pady=3)
		self.btn_about = tk.Button(self.top, text="About", command=about, padx=15, pady=3)
		self.btn_help = tk.Button(self.top, text="Help?", command=my_help, padx=15, pady=3)
		self.btn_quit = tk.Button(self.top, text="Quit", command=self.quit, padx=15, pady=3)
		self.btn_play['font'] = helve14
		self.btn_about['font'] = helve14
		self.btn_help['font'] = helve14
		self.btn_quit['font'] = helve14

		image_path = "assets/katro.jpg"
		image = Image.open(image_path)
		image = image.resize((800, 500))
		imgtk = ImageTk.PhotoImage(image)
		self.img_label = ttk.Label(self.top, image=imgtk)
		self.img_label.image = imgtk
		# render component
		self.render_component()

	def render_component(self):
		self.img_label.grid(row=0, column=0, columnspan=5)
		self.title_label.grid(row=1, column=0, pady=20)
		self.btn_play.grid(row=1, column=1, pady=20)
		self.btn_about.grid(row=1, column=2, pady=20)
		self.btn_help.grid(row=1, column=3, pady=20)
		self.btn_quit.grid(row=1, column=4, pady=20)

	def render(self):
		self.app.mainloop()

	def quit(self):
		self.top.destroy()
		self.app.deiconify()
		self.app.destroy()

	def play(self):
		choice = messagebox.askquestion(
			"Do you want to start?",
			"Do you want to start the game or do you prefer the AI to start?"
		)
		_start = None
		if choice == "yes":
			_start = 2
		else:
			_start = 1
		self.top.withdraw()
		game = Game(_start)
		game.main()
		self.top.deiconify()
