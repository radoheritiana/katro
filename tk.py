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
				"close": "Close",
				"cancel": "Cancel",
				"settings_gameplay": "Gameplay",
				"settings_audio": "Audio",
				"settings_language": "Language",
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
				"close": "Fermer",
				"cancel": "Annuler",
				"settings_gameplay": "Jeu",
				"settings_audio": "Audio",
				"settings_language": "Langue",
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
				"close": "Akatona",
				"cancel": "Ajanona",
				"settings_gameplay": "Filalaovana",
				"settings_audio": "Feo",
				"settings_language": "Fiteny",
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
		self._open_text_dialog("about_title", "about_text", 620, 420)

	def show_help(self):
		self._open_text_dialog("help_title", "help_text", 620, 360)

	def _open_text_dialog(self, title_key, text_key, width, height):
		dialog = Toplevel(self.top)
		dialog.title(self._t(title_key))
		dialog.resizable(width=False, height=False)
		dialog.configure(bg="brown")
		dialog.geometry(center(dialog, width, height))
		dialog.transient(self.top)
		dialog.grab_set()

		container = ttk.Frame(dialog, padding=14)
		container.pack(fill="both", expand=True)

		title = ttk.Label(container, text=self._t(title_key), font=("Helvetica", 15, "bold"))
		title.pack(anchor="w", pady=(0, 10))

		text_wrap = ttk.Frame(container)
		text_wrap.pack(fill="both", expand=True)

		scrollbar = ttk.Scrollbar(text_wrap, orient="vertical")
		scrollbar.pack(side="right", fill="y")

		body = tk.Text(
			text_wrap,
			wrap="word",
			height=12,
			font=("Helvetica", 11),
			padx=10,
			pady=10,
			yscrollcommand=scrollbar.set,
		)
		body.pack(side="left", fill="both", expand=True)
		scrollbar.config(command=body.yview)
		body.insert("1.0", self._t(text_key))
		body.config(state="disabled")

		actions = ttk.Frame(container)
		actions.pack(fill="x", pady=(12, 0))
		ttk.Button(actions, text=self._t("close"), command=dialog.destroy).pack(side="right")

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
		settings_window.geometry(center(settings_window, 460, 500))
		settings_window.transient(self.top)
		settings_window.grab_set()

		start_var = tk.StringVar(value="player" if self.settings["start"] == 2 else "ai")
		dots_var = tk.IntVar(value=self.settings["dots"])
		sound_var = tk.BooleanVar(value=self.settings["sound_enabled"])
		speed_var = tk.StringVar(value=self.settings["speed"])
		language_var = tk.StringVar(value=self.language_reverse_map.get(self.settings["language"], "EN"))

		container = ttk.Frame(settings_window, padding=14)
		container.pack(fill="both", expand=True)
		container.columnconfigure(0, weight=1)

		gameplay_group = ttk.LabelFrame(container, text=self._t("settings_gameplay"), padding=10)
		gameplay_group.grid(row=0, column=0, sticky="ew", pady=(0, 10))
		gameplay_group.columnconfigure(1, weight=1)

		ttk.Label(gameplay_group, text=self._t("who_starts")).grid(row=0, column=0, sticky="w")
		ttk.Radiobutton(gameplay_group, text=self._t("player"), variable=start_var, value="player").grid(row=1, column=0, sticky="w", padx=(10, 0), pady=(4, 0))
		ttk.Radiobutton(gameplay_group, text=self._t("ai"), variable=start_var, value="ai").grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(4, 0))

		ttk.Label(gameplay_group, text=self._t("dots_per_case")).grid(row=2, column=0, sticky="w", pady=(10, 0))
		ttk.Radiobutton(gameplay_group, text="2", variable=dots_var, value=2).grid(row=3, column=0, sticky="w", padx=(10, 0), pady=(4, 0))
		ttk.Radiobutton(gameplay_group, text="3", variable=dots_var, value=3).grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(4, 0))

		ttk.Label(gameplay_group, text=self._t("game_speed")).grid(row=4, column=0, sticky="w", pady=(10, 0))
		speed_combo = ttk.Combobox(gameplay_group, textvariable=speed_var, state="readonly", values=["slow", "normal", "fast"], width=12)
		speed_combo.grid(row=5, column=0, sticky="w", padx=(10, 0), pady=(4, 0))

		audio_group = ttk.LabelFrame(container, text=self._t("settings_audio"), padding=10)
		audio_group.grid(row=1, column=0, sticky="ew", pady=(0, 10))
		ttk.Checkbutton(audio_group, text=self._t("enable_sound"), variable=sound_var).grid(row=0, column=0, sticky="w")

		language_group = ttk.LabelFrame(container, text=self._t("settings_language"), padding=10)
		language_group.grid(row=2, column=0, sticky="ew")
		ttk.Label(language_group, text=self._t("language")).grid(row=0, column=0, sticky="w")
		language_combo = ttk.Combobox(language_group, textvariable=language_var, state="readonly", values=self.language_options, width=12)
		language_combo.grid(row=1, column=0, sticky="w", pady=(4, 0))

		def save_settings():
			self.settings["start"] = 2 if start_var.get() == "player" else 1
			self.settings["dots"] = dots_var.get()
			self.settings["sound_enabled"] = sound_var.get()
			self.settings["speed"] = speed_var.get()
			self.settings["language"] = self.language_map.get(language_var.get(), "en")
			self.refresh_ui_texts()
			settings_window.destroy()

		actions = ttk.Frame(container)
		actions.grid(row=3, column=0, sticky="e", pady=(14, 0))
		ttk.Button(actions, text=self._t("cancel"), command=settings_window.destroy).pack(side="left", padx=(0, 8))
		ttk.Button(actions, text=self._t("save"), command=save_settings).pack(side="left")

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
