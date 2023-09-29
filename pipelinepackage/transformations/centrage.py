"""
Centrer des variables d'un jeu de données.

Examples
--------
>>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
>>> a = Centrage(['age'])
>>> a.transforme(data).body
[{'nom': 'Anne', 'age': 6.0}, {'nom': 'Clementine', 'age': 0.0}, {'nom': 'Chloe', 'age': -10.0}, {'nom': 'Maelle', 'age': 4.0}]

"""
from pipelinepackage.model.dataset import Dataset
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.estimateurs.estimateur import Estimateur


class Centrage(Transformation):
    """
    Modélisation d'une transformation permettant de centrer les données d'une
    ou de plusieurs variables à l'aide de la moyenne des variables considérées.

    Attributes
    ----------
    variables : list[str]
        Liste des noms de la ou des variables à centrer.

    Examples
    --------
    >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
    >>> a = Centrage(['age'])
    >>> a.transforme(data).body
    [{'nom': 'Anne', 'age': 6.0}, {'nom': 'Clementine', 'age': 0.0}, {'nom': 'Chloe', 'age': -10.0}, {'nom': 'Maelle', 'age': 4.0}]
    """

    def __init__(self, variables):
        """ Constructeur

        Parameters
        ----------
        variables : list[str]
            Liste des noms de la ou des variables à centrer.
        """
        super().__init__()
        self.__variables = variables

    def transforme(self, dataset):
        """ Transformation d'un jeu de données

        Centre les données du jeu de données dataset passé en paramètre.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données à centrer.

        Returns
        -------
        Dataset
            Jeu de données avec des données centrées.

        Examples
        --------
        >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
        >>> a = Centrage(['age'])
        >>> a.transforme(data).body
        [{'nom': 'Anne', 'age': 6.0}, {'nom': 'Clementine', 'age': 0.0}, {'nom': 'Chloe', 'age': -10.0}, {'nom': 'Maelle', 'age': 4.0}]
        """
        body = dataset.body
        variables = list(set(dataset.header) & set(self.__variables))
        moys = {}

        for var in variables:
            estim = Estimateur(var)
            moys[var] = estim.moyenne(dataset)

        for i in range(len(body)):
            for var in variables:
                body[i][var] = float(body[i][var])-moys[var]

        return Dataset(dataset.header, body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
