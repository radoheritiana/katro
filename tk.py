import tkinter as tk
from tkinter import Toplevel, ttk, Tk
from PIL import ImageTk, Image
from tkinter import font as tk_font
from tkinter import messagebox
from game import Game
import os


def center(win, width, height):
	win.update_idletasks()
	x = (win.winfo_screenwidth() // 2) - (width // 2)
	y = (win.winfo_screenheight() // 2) - (height // 2)
	return '{}x{}+{}+{}'.format(width, height, x, y)


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
		self.translations = {
			"en": {
				"window_title": "Katro",
				"title": "Katro",
				"play": "Play",
				"about": "About",
				"settings": "Settings",
				"help": "Help?",
				"quit": "Quit",
				"quit_title": "Quit",
				"quit_confirm": "Do you really want to quit?",
				"settings_title": "Settings",
				"who_starts": "Who starts the game?",
				"player": "Player",
				"ai": "AI",
				"dots_per_case": "Dots per case",
				"enable_sound": "Enable sound",
				"game_speed": "Game speed",
				"language": "Language",
				"save": "Save",
				"about_title": "About Katro game",
				"about_text": "What is Katro?\n\nThe Katro has been present on the Big Island for many centuries. Malagasy, especially women and children, played this game in the afternoon, after household chores or school. This entertainment, although invented by Malagasy ancestors, would derive from the African mancala, a whole range of games of pebbles and seeds. The best known being awale. In the region of Fianarantsoa, the Bestileo, tireless players of Katro, consider it the traditional mancala.\n\nWhat is katro game?\n\nThe purpose of this application is to play this Malagasy game on our computer, the game is currently for a single player who fights against the computer, but the two-player feature is coming!",
				"help_title": "Help",
				"help_text": "The Katro is played by two player. Each player has two rows of pawns. The one who starts the game chooses the hole and starts. He takes the pawns in his hole and distributes them successively in the other holes of his row.",
			},
			"fr": {
				"window_title": "Katro",
				"title": "Katro",
				"play": "Jouer",
				"about": "A propos",
				"settings": "Parametres",
				"help": "Aide ?",
				"quit": "Quitter",
				"quit_title": "Quitter",
				"quit_confirm": "Voulez-vous vraiment quitter ?",
				"settings_title": "Parametres",
				"who_starts": "Qui commence la partie ?",
				"player": "Joueur",
				"ai": "IA",
				"dots_per_case": "Graines par case",
				"enable_sound": "Activer le son",
				"game_speed": "Vitesse du jeu",
				"language": "Langue",
				"save": "Enregistrer",
				"about_title": "A propos du jeu Katro",
				"about_text": "Le Katro est un jeu traditionnel malgache pratique depuis des siecles a Madagascar. Cette application permet d'y jouer sur ordinateur contre l'IA.",
				"help_title": "Aide",
				"help_text": "Le Katro se joue a deux. Chaque joueur a deux rangees. Le joueur prend les graines d'une case et les distribue dans les cases suivantes.",
			},
			"mga": {
				"window_title": "Katro",
				"title": "Katro",
				"play": "Hilalao",
				"about": "Momba",
				"settings": "Fikirana",
				"help": "Fanampiana ?",
				"quit": "Hivoaka",
				"quit_title": "Hivoaka",
				"quit_confirm": "Tena hivoaka ve ianao?",
				"settings_title": "Fikirana",
				"who_starts": "Iza no manomboka ?",
				"player": "Mpilalao",
				"ai": "IA",
				"dots_per_case": "Isan'ny voa isaky ny lavaka",
				"enable_sound": "Alefa ny feo",
				"game_speed": "Hafainganam-pilalaovana",
				"language": "Fiteny",
				"save": "Tehirizo",
				"about_title": "Momba ny lalao Katro",
				"about_text": "Ny Katro dia lalao nentim-paharazana malagasy. Ity rindranasa ity dia ahafahanao milalao Katro amin'ny solosaina.",
				"help_title": "Fanampiana",
				"help_text": "Lalaovin'olona roa ny Katro. Maka voa amin'ny lavaka iray ny mpilalao ary mizara azy amin'ny lavaka manaraka.",
			},
		}
		self.language_options = ["EN", "FR", "MGA"]
		self.language_map = {"EN": "en", "FR": "fr", "MGA": "mga"}
		self.language_reverse_map = {"en": "EN", "fr": "FR", "mga": "MGA"}

		self.settings = {
			"start": 2,
			"dots": 2,
			"sound_enabled": True,
			"speed": "normal",
			"language": "en",
		}
		self.speed_profiles = {
			"slow": {"fps": 90, "step": 2},
			"normal": {"fps": 120, "step": 3},
			"fast": {"fps": 180, "step": 4},
		}

		# config
		self.app = Tk()
		self.app.withdraw()
		self.top = Toplevel()
		self.top.title(self._t("window_title"))
		width, height = 860, 590
		self.top.geometry(center(self.top, width, height))
		self.top.iconbitmap(os.path.join("assets", "favicon.ico"))
		self.top.resizable(width=False, height=False)
		self.top.configure(bg="brown")
		self.top.protocol("WM_DELETE_WINDOW", self.quit)
		self.frame = ttk.Frame(master=self.top)
		self.frame.grid()
		# component
		font = ("Helvetica", 26)
		helve13 = tk_font.Font(family='Helvetica', size=13, weight='bold')
		self.menu_button_width = 11
		self.title_label = tk.Label(self.top, text=self._t("title"), font=font, background="brown", foreground="white")
		self.btn_play = tk.Button(self.top, text=self._t("play"), command=self.play, padx=8, pady=3, width=self.menu_button_width)
		self.btn_about = tk.Button(self.top, text=self._t("about"), command=self.show_about, padx=8, pady=3, width=self.menu_button_width)
		self.btn_settings = tk.Button(self.top, text=self._t("settings"), command=self.open_settings, padx=8, pady=3, width=self.menu_button_width)
		self.btn_help = tk.Button(self.top, text=self._t("help"), command=self.show_help, padx=8, pady=3, width=self.menu_button_width)
		self.btn_quit = tk.Button(self.top, text=self._t("quit"), command=self.quit, padx=8, pady=3, width=self.menu_button_width)
		self.btn_play['font'] = helve13
		self.btn_about['font'] = helve13
		self.btn_settings['font'] = helve13
		self.btn_help['font'] = helve13
		self.btn_quit['font'] = helve13

		image_path = "assets/katro.jpg"
		image = Image.open(image_path)
		image = image.resize((860, 500))
		imgtk = ImageTk.PhotoImage(image)
		self.img_label = ttk.Label(self.top, image=imgtk)
		self.img_label.image = imgtk
		# render component
		self.render_component()

	def _t(self, key):
		lang = self.settings.get("language", "en")
		return self.translations.get(lang, self.translations["en"]).get(key, key)

	def refresh_ui_texts(self):
		self.top.title(self._t("window_title"))
		self.title_label.config(text=self._t("title"))
		self.btn_play.config(text=self._t("play"))
		self.btn_about.config(text=self._t("about"))
		self.btn_settings.config(text=self._t("settings"))
		self.btn_help.config(text=self._t("help"))
		self.btn_quit.config(text=self._t("quit"))

	def show_about(self):
		messagebox.showinfo(self._t("about_title"), self._t("about_text"))

	def show_help(self):
		messagebox.showinfo(self._t("help_title"), self._t("help_text"))

	def render_component(self):
		self.img_label.grid(row=0, column=0, columnspan=6)
		for i in range(6):
			self.top.grid_columnconfigure(i, minsize=140)
		self.title_label.grid(row=1, column=0, pady=20)
		self.btn_play.grid(row=1, column=1, pady=20, padx=4)
		self.btn_about.grid(row=1, column=2, pady=20, padx=4)
		self.btn_settings.grid(row=1, column=3, pady=20, padx=4)
		self.btn_help.grid(row=1, column=4, pady=20, padx=4)
		self.btn_quit.grid(row=1, column=5, pady=20, padx=4)

	def render(self):
		self.app.mainloop()

	def quit(self):
		if not messagebox.askyesno(self._t("quit_title"), self._t("quit_confirm")):
			return
		self.top.destroy()
		# self.app.deiconify()
		self.app.destroy()

	def open_settings(self):
		settings_window = Toplevel(self.top)
		settings_window.title(self._t("settings_title"))
		settings_window.resizable(width=False, height=False)
		settings_window.configure(bg="brown")
		settings_window.geometry(center(settings_window, 420, 430))

		start_var = tk.StringVar(value="player" if self.settings["start"] == 2 else "ai")
		dots_var = tk.IntVar(value=self.settings["dots"])
		sound_var = tk.BooleanVar(value=self.settings["sound_enabled"])
		speed_var = tk.StringVar(value=self.settings["speed"])
		language_var = tk.StringVar(value=self.language_reverse_map.get(self.settings["language"], "EN"))

		tk.Label(settings_window, text=self._t("who_starts")).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
		tk.Radiobutton(settings_window, text=self._t("player"), variable=start_var, value="player").grid(row=1, column=0, sticky="w", padx=30)
		tk.Radiobutton(settings_window, text=self._t("ai"), variable=start_var, value="ai").grid(row=2, column=0, sticky="w", padx=30)

		tk.Label(settings_window, text=self._t("dots_per_case")).grid(row=3, column=0, sticky="w", padx=20, pady=(15, 5))
		ttk.Radiobutton(settings_window, text="2", variable=dots_var, value=2).grid(row=4, column=0, sticky="w", padx=30)
		ttk.Radiobutton(settings_window, text="3", variable=dots_var, value=3).grid(row=5, column=0, sticky="w", padx=30)

		tk.Checkbutton(settings_window, text=self._t("enable_sound"), variable=sound_var).grid(row=6, column=0, sticky="w", padx=20, pady=(15, 5))

		tk.Label(settings_window, text=self._t("game_speed")).grid(row=7, column=0, sticky="w", padx=20, pady=(10, 5))
		speed_combo = ttk.Combobox(settings_window, textvariable=speed_var, state="readonly", values=["slow", "normal", "fast"])
		speed_combo.grid(row=8, column=0, sticky="w", padx=20)

		tk.Label(settings_window, text=self._t("language")).grid(row=9, column=0, sticky="w", padx=20, pady=(10, 5))
		language_combo = ttk.Combobox(settings_window, textvariable=language_var, state="readonly", values=self.language_options)
		language_combo.grid(row=10, column=0, sticky="w", padx=20)

		def save_settings():
			self.settings["start"] = 2 if start_var.get() == "player" else 1
			self.settings["dots"] = dots_var.get()
			self.settings["sound_enabled"] = sound_var.get()
			self.settings["speed"] = speed_var.get()
			self.settings["language"] = self.language_map.get(language_var.get(), "en")
			self.refresh_ui_texts()
			settings_window.destroy()

		tk.Button(settings_window, text=self._t("save"), command=save_settings).grid(row=11, column=0, sticky="e", padx=20, pady=(20, 12))

	def play(self):
		self.top.withdraw()
		speed = self.speed_profiles.get(self.settings["speed"], self.speed_profiles["normal"])
		game = Game(
			self.settings["start"],
			self.settings["dots"],
			sound_enabled=self.settings["sound_enabled"],
			animation_fps=speed["fps"],
			animation_step=speed["step"],
			language=self.settings["language"],
		)
		game.main()
		self.top.deiconify()
