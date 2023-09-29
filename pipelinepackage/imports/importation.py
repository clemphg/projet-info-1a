"""module Importation

"""
from abc import ABC, abstractmethod


class Importation(ABC):
    """Classe abstraite Importation

    Sert de base pour coder les différents types d'importation.

    Attributes
    ----------
    chemin : str
        Chemin vers le fichier ou le dossier de fichiers à importer
    """

    def __init__(self, chemin):
        """Constructeur de la classe Importation

        Parameters
        ----------
        chemin : str
            Chemin vers le fichier ou le dossier de fichiers à importer
        """
        self.__chemin = chemin

    @abstractmethod
    def importe(self):
        """Importer un jeu de données

        Parameters
        ----------
        chemin : str
            Chemin vers le fichier ou le dossier de fichiers à importer
        """

    @property
    def chemin(self):
        """Getter pour l'attribut chemin

        Returns
        -------
        str
            Chemin vers le fichier ou le dossier de fichiers à importer
        """
        return self.__chemin
