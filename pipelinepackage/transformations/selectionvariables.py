"""
Sélectionner des variables d'un jeu de données.

Crée un nouveau jeu de données ne contenant que les variables sélectionnées.
"""
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset


class SelectionVariables(Transformation):
    """Classe SelectionVariables

    Sélectionner toutes les observations des variables choisies dans un Dataset.

    Attributes
    ----------
    variables : list[str]
        Nom de la ou des variables à conserver.

    Examples
    --------
    >>> data = Dataset(['nom', 'region'], [{'nom': 'Anne', 'region': 'Corse'}, {'nom': 'Clementine', 'region': 'Bretagne'}, {'nom': 'Chloe', 'region': 'Hauts-de-France'}, {'nom': 'Maelle', 'region': 'Pays de la Loire'}])
    >>> a = SelectionVariables(['nom'])
    >>> a.transforme(data).header
    ['nom']
    >>> a.transforme(data).body
    [{'nom': 'Anne'}, {'nom': 'Clementine'}, {'nom': 'Chloe'}, {'nom': 'Maelle'}]
    """

    def __init__(self, variables):
        """Constructeur

        Parameters
        ----------
        variables : list[str]
            Nom de la ou des variables à conserver.
        """
        super().__init__()
        self.__variables = variables

    def transforme(self, dataset):
        """ Selection de variables dans un jeu de données.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données dans lequel on veut sélectionner des variables.

        Returns
        -------
        Dataset
            Jeu de données avec les observations des variables sélectionnées.

        Examples
        --------
        >>> data = Dataset(['nom', 'region'], [{'nom': 'Anne', 'region': 'Corse'}, {'nom': 'Clementine', 'region': 'Bretagne'}, {'nom': 'Chloe', 'region': 'Hauts-de-France'}, {'nom': 'Maelle', 'region': 'Pays de la Loire'}])
        >>> a = SelectionVariables(['region'])
        >>> a.transforme(data).header
        ['region']
        """
        body = dataset.body

        variables = list(set(self.__variables) & set(dataset.header))

        for i in range(len(body)):
            body[i] = {key: body[i][key] for key in variables}

        return Dataset(variables, body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
