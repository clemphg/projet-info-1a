"""" module estimateur

Calcule des statistiques descriptives sur une variable d'un jeu de données.
"""

class Estimateur:
    """Classe Estimateur

    Permet de calculer des statistiques descriptives sur une variable d'un jeu de données.

    Attributes
    ----------
    variable : str
        Variable su laquelle on calcule les statistiques

    Examples
    --------
    >>> from pipelinepackage.model.dataset import Dataset
    >>> data = Dataset(['nom', 'age'], [{'nom' : 'Anne', 'age' : '23'}, {'nom' : 'Clementine', 'age' : '17'}, {'nom' : 'Chloe', 'age' : '7'}, {'nom' : 'Maelle', 'age' : '21'}])
    >>> c = Estimateur('age')
    >>> c.moyenne(data)
    17.0
    """

    def __init__(self, variable):
        """" Constructeur

        Parameters
        ----------
        variable : str
            Variable sur laquelle on calcule les statistiques
        """
        self.__variable = variable

    def moyenne(self, dataset):
        """Calcul de la moyenne

        Calcule la moyenne pour la variable du jeu de données dataset

        Parameters
        ----------
        dataset : Dataset
            Jeu de données comprenant la variable (sans valeurs manquantes)

        Returns
        -------
        dataset
            Dataset

        Examples
        --------
        >>> from pipelinepackage.model.dataset import Dataset
        >>> data = Dataset(['nom', 'age'], [{'nom' : 'Anne', 'age' : '23'}, {'nom' : 'Clementine', 'age' : '17'}, {'nom' : 'Chloe', 'age' : '7'}, {'nom' : 'Maelle', 'age' : '21'}])
        >>> c = Estimateur('age')
        >>> c.moyenne(data)
        17.0
        """
        vals = [float(row.get(self.__variable)) for row in dataset.body
                if row.get(self.__variable) is not None]
        moy = sum(vals)/len(vals)
        return round(moy, 3)

    def ecarttype(self, dataset):
        """Calcul de l'écart-type

        Calcule l'écart-type pour la variable du jeu de données dataset

        Parameters
        ----------
        dataset : Dataset
            Jeu de données comprenant la variable (sans valeurs manquantes)

        Returns
        -------
        dataset
            Dataset

        Examples
        --------
        >>> from pipelinepackage.model.dataset import Dataset
        >>> data = Dataset(['nom', 'age'], [{'nom' : 'Anne', 'age' : '23'}, {'nom' : 'Clementine', 'age' : '17'}, {'nom' : 'Chloe', 'age' : '7'}, {'nom' : 'Maelle', 'age' : '21'}])
        >>> c = Estimateur('age')
        >>> c.ecarttype(data)
        7.118
        """
        moy = self.moyenne(dataset)
        ecart = [(float(row.get(self.__variable))-moy)
                 ** 2 for row in dataset.body]
        return round((sum(ecart)/(len(ecart)-1))**(1/2), 3)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
