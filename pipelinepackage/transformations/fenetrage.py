"""
module fenetrage

Sélectionner toutes les observations dont la date est dans une fourchette donnée.
"""
from datetime import datetime
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset


class Fenetrage(Transformation):
    """ Classe Fenetrage

    Modélise une sélection de lignes selon une variable de date.
    Les dates sont des chaines de caractères au format suivant :
    'yyyy-mm-dd hh:mm:ss' ou 'yyyy-mm-dd'

    Attributes
    ----------
    date_debut : str
        Date à partir de laquelle on souhaite obtenir les observations
    date_fin : str
        Date avant laquelle on souhaite obtenir les observations
    date : str
        Nom de la variable de date du jeu de données

    Examples
    --------
    >>> data = Dataset(['nom', 'date'], [{'nom': 'Anne', 'date': '1998-07-24'}, {'nom': 'Clementine', 'date': '2004-09-25'}, {'nom': 'Chloe', 'date': '2015-10-09'}, {'nom': 'Maelle', 'date': '2001-03-15'}])
    >>> a = Fenetrage('2003-01-01', '2005-12-31', 'date')
    >>> a.transforme(data).body
    [{'nom': 'Clementine', 'date': '2004-09-25'}]
    """

    def __init__(self, date_debut, date_fin, variable):
        """ Constructeur

        Parameters
        ----------
        date_debut : str
            Date à partir de laquelle on souhaite obtenir les observations
        date_fin : str
            Date avant laquelle on souhaite obtenir les observations
        variable : str
            Nom de la variable de date du jeu de données
        """
        super().__init__()
        self.__date_debut = date_debut
        self.__date_fin = date_fin
        self.__variable = variable

    def transforme(self, dataset):
        """ Transformation d'un jeu de données

        Sélection des observation du jeu de données dataset dont la variable de
        date des observations est comprise entre date_debut et date_fin.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données sur lequel on effectue la sélection d'observations

        Returns
        -------
        Dataset
            Jeu de données dont la variable date est comprise entre date_debut et date_fin

        Examples
        --------
        >>> data = Dataset(['nom', 'date'], [{'nom': 'Anne', 'date': '1998-07-24'}, {'nom': 'Clementine', 'date': '2004-09-25'}, {'nom': 'Chloe', 'date': '2015-10-09'}, {'nom': 'Maelle', 'date': '2001-03-15'}])
        >>> a = Fenetrage('2003-01-01', '2020-05-10', 'date')
        >>> a.transforme(data).body
        [{'nom': 'Clementine', 'date': '2004-09-25'}, {'nom': 'Chloe', 'date': '2015-10-09'}]
        """
        result = []
        data = dataset.body

        for row in data:
            if (datetime.fromisoformat(self.__date_debut) <=
                datetime.fromisoformat(row[self.__variable]) <=
                    datetime.fromisoformat(self.__date_fin)):
                result.append(row)

        return Dataset(dataset.header, result)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
