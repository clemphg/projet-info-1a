"""
module transformation

Base pour l'implémentation de diverses transformations.
"""
from abc import ABC, abstractmethod


class Transformation(ABC):
    """Classe abstraite Transformation

    Base pour des classes effectuant des transformations sur des jeux de données
    """

    @abstractmethod
    def __init__(self):
        """Constructeur
        """

    @abstractmethod
    def transforme(self, dataset):
        """Transformer le jeu de données

        Parameters
        ----------
        dataset : Dataset
            Jeu de données sur lequel la transformation est effectuée
        """
