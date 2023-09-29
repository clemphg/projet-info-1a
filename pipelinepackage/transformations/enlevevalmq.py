"""
Enlever les valeurs manquantes d'un jeu de données
"""

from pipelinepackage.model.dataset import Dataset
from pipelinepackage.transformations.transformation import Transformation


class EnleveValMq(Transformation):
    """"
    Modélisation d'une transformation permettant de retirer toutes les
    observations contenant une ou plusieurs valeurs manquantes d'un jeu de données.

    Attributes
    ----------
    listevalmq : list[str]
            Valeurs que les valeurs manquantes peuvent prendre.

    Examples
    --------
    >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 'NA'}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'NA', 'age': 21}])
    >>> a = EnleveValMq(['NA'])
    >>> a.transforme(data).body
    [{'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}]
    """

    def __init__(self, listevalmq):
        """Constructeur

        Parameters
        ----------
        listevalmq : list[str]
            Valeurs que les valeurs manquantes peuvent prendre
        """
        super().__init__()
        self.__listevalmq = listevalmq

    def transforme(self, dataset):
        """Transformation d'un jeu de données.

        Enleve les valeurs manquantes du jeu de données dataset passé en paramètre.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données duquel on souhaite enlever les valeurs manquantes.

        Returns
        -------
        Dataset
            Jeu de données sans aucune valeurs manquantes.

        Examples
        --------
        >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 'NA'}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'NA', 'age': 21}])
        >>> a = EnleveValMq(['NA'])
        >>> a.transforme(data).body
        [{'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}]
        """
        body = []
        data = dataset.body

        for row in data:
            check = True
            for val in dataset.header:
                if row.get(val) in self.__listevalmq:
                    check = False
            if check:
                body.append(row)

        header = []
        if len(body) > 0:
            header = list(body[0])

        return Dataset(header, body)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)