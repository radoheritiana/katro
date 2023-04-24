from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts


class KatroEnv(py_environment.PyEnvironment):

	def __init__(self):
		# Initialisation de l'environnement
		self._state = np.array([[2, 2, 2, 2], [2, 2, 2, 2]])  # Tableau des pions pour chaque joueur
		print(self._state)
		self._player = 0  # Joueur en cours
		self._game_over = False  # Indicateur de fin de partie

	def action_spec(self):
		# Espace des actions possibles
		return array_spec.BoundedArraySpec(
			shape=(), dtype=np.int32, minimum=0, maximum=7, name='action')

	def observation_spec(self):
		# Espace des observations possibles
		return array_spec.ArraySpec(
			shape=(2, 4), dtype=np.int32, name='observation')

	def _reset(self):
		# Réinitialisation de l'environnement
		self._state = np.array([[2, 2, 2, 2], [2, 2, 2, 2]])
		self._player = 0
		self._game_over = False
		return ts.restart(np.array([self._state[self._player]]))

	def _step(self, action):
		# Effectue une transition dans l'état de l'environnement en fonction de l'action spécifiée,
		# calcule la récompense pour l'action, et renvoie un nouveau time_step
		if self._game_over:
			return self.reset()

		# Distribution des pions
		num_pions = self._state[self._player, action]
		self._state[self._player, action] = 0
		col = action
		while num_pions > 0:
			col += 1
			if col == 8:  # Retour à la première colonne si on dépasse la dernière
				col = 0
			if col == action:  # On ne place pas de pion dans le trou de départ
				continue
			self._state[self._player, col] += 1
			num_pions -= 1

		# Vérification des captures
		if col < 4 and self._state[self._player, col] == 1 and self._state[1 - self._player, 3 - col] > 0:
			self._state[self._player, col] = 0
			self._state[self._player, 4] += 1 + self._state[1 - self._player, 3 - col]
			self._state[1 - self._player, 3 - col] = 0

		# Vérification de la fin de la partie
		if np.sum(self._state[self._player]) == 0:
			self._game_over = True
			return ts.termination(np.array([self._state[self._player]]), 0)

		# Passage au joueur suivant
		self._player = 1 - self._player
		return ts.transition(
			np.array([self._state[self._player]]),
			reward=0, discount=1.0)

	def render(self):
		# Affiche une représentation graphique de l'état actuel de l'environnement
		print(self._state)


if __name__ == "__main__":
	katro_env = KatroEnv()
