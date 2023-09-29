"""
module exportation

Exporter un jeu de données selon un certain format.
"""
from abc import ABC, abstractmethod

class Exportation(ABC):
    """Classe abstraite exportation

    Attributes
    ----------
    chemin : str, optional
        Dossier dans lequel sauvegarder le résultat, by default "data/output"
    filename : str, optional
        Nom du fichier résultat, by default "tableau.csv"
    """

    def __init__(self, chemin = "data/output", filename = "tableau"):
        """Constructeur

        Parameters
        ----------
        chemin : str, optional
            Dossier dans lequel sauvegarder le résultat, by default "data/output"
        filename : str, optional
            Nom du fichier résultat, by default "tableau"
        """
        self.__chemin = chemin
        self.__filename = filename

    @property
    def chemin(self):
        """Getter pour l'attribut chemin

        Returns
        -------
        str
            Dossier dans lequel sauvegarder le résultat
        """
        return self.__chemin

    @property
    def filename(self):
        """Getter pour l'attribut chemin

        Returns
        -------
        str
            Nom du fichier résultat
        """
        return self.__filename

    @abstractmethod
    def exporte(self, dataset):
        """Exportation du jeu de données

        Exporte le jeu de données au chemin passé en paramètre.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données à exporter
        """
