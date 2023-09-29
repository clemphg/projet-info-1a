"""
Normaliser des variables d'un jeu de données.
"""
from pipelinepackage.model.dataset import Dataset
from pipelinepackage.estimateurs.estimateur import Estimateur
from pipelinepackage.transformations.transformation import Transformation


class Normalisation(Transformation):
    """Classe Normalisation

    Modélise la normalisation des données.

    Attributes
    ----------
    variables : list[str]
        Liste de la ou des variables que l'on souhaite normaliser.

    Examples
    --------
    >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
    >>> a = Normalisation(['age'])
    >>> a.transforme(data).body
    [{'nom': 'Anne', 'age': 0.8429334082607474}, {'nom': 'Clementine', 'age': 0.0}, {'nom': 'Chloe', 'age': -1.4048890137679122}, {'nom': 'Maelle', 'age': 0.561955605507165}]
    """

    def __init__(self, variables):
        """Constructeur

        Parameters
        ----------
        variables : list[str]
            Liste de la ou des variables que l'on souhaite normaliser.
        """
        super().__init__()
        self.__variables = variables

    def transforme(self, dataset):
        """Normalisation d'un jeu de données.

        Normalise les données du jeu de données passé en paramètre.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données sur lequel on souhaite effectuer la normalisation.

        Returns
        -------
        Dataset
            Jeu de données normalisé.

        Examples
        --------
        >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
        >>> a = Normalisation(['age'])
        >>> a.transforme(data).body
        [{'nom': 'Anne', 'age': 0.8429334082607474}, {'nom': 'Clementine', 'age': 0.0}, {'nom': 'Chloe', 'age': -1.4048890137679122}, {'nom': 'Maelle', 'age': 0.561955605507165}]
        """
        data = dataset.body
        body = []
        for variable in self.__variables:
            # calcul de la moyenne et de l'écart-type pour chaque variable
            estim = Estimateur(variable)
            moy = estim.moyenne(dataset)
            ecart = estim.ecarttype(dataset)
            for row in data:
                row[variable] = (float(row[variable]) - moy)/ecart
                body.append(row)
        return Dataset(dataset.header, body)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)