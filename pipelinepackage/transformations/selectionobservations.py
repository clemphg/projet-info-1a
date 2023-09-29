"""
Sélectionner des variables à partir de condictions.
"""
from datetime import datetime
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset


class SelectionObservations(Transformation):
    """Sélectionner des observations

    Parameters
    ----------
    variables : list[str]
        liste de variables
    conditions : list[str]
        liste de conditions ('=', '>', '<' ou '!=')
    valeurs : list[str]
        liste de valeurs pour les conditions
    types : list[str]
        liste des types pris par les variables ('int', 'float', 'str' ou 'date')

    Examples
    --------
    Selection sur l'âge
    >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
    >>> a = SelectionObservations(['age'], ['>'], [18], ['int'])
    >>> a.transforme(data).body
    [{'nom': 'Anne', 'age': 23}, {'nom': 'Maelle', 'age': 21}]

    Selection sur l'âge et le nom
    >>> databis = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
    >>> b = SelectionObservations(['nom', 'age'], ['!=', '<'], ['Clementine', 18], ['str', 'int'])
    >>> b.transforme(databis).body
    [{'nom': 'Chloe', 'age': 7}]
    """

    def __init__(self, variables, conditions, valeurs, types=None):
        """Constructeur

        Parameters
        ----------
        variables : list[str]
            liste de variables
        conditions : list[str]
            liste de conditions ('=', '>', '<' ou '!=')
        valeurs : list[str]
            liste de valeurs pour les conditions
        types : list[str]
            liste des types pris par les variables ('int', 'float', 'str' ou 'date')
        """
        super().__init__()
        self.__variables = variables
        self.__conditions = conditions
        self.__valeurs = valeurs
        self.__types = types

    def transforme(self, dataset):
        """Sélection d'observations d'un jeu de données.

        Construit un jeu de données ne contenant que les observations
        répondant aux conditions passées au constructeur.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données à partir duquel on sélectionne les observations.

        Returns
        -------
        Dataset
            Jeu de données ne contenant que les observations répondant aux conditions.

        Examples
        --------
        Selection sur l'âge
        >>> data = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
        >>> a = SelectionObservations(['age'], ['>'], [18], ['int'])
        >>> a.transforme(data).body
        [{'nom': 'Anne', 'age': 23}, {'nom': 'Maelle', 'age': 21}]

        Selection sur l'âge et le nom
        >>> databis = Dataset(['nom', 'age'], [{'nom': 'Anne', 'age': 23}, {'nom': 'Clementine', 'age': 17}, {'nom': 'Chloe', 'age': 7}, {'nom': 'Maelle', 'age': 21}])
        >>> b = SelectionObservations(['nom', 'age'], ['!=', '<'], ['Clementine', 18], ['str', 'int'])
        >>> b.transforme(databis).body
        [{'nom': 'Chloe', 'age': 7}]
        """
        body = dataset.body
        datares = []

        # on passe sur toutes les lignes (observations)
        for row in body:
            check = True
            for var, cond, val, typ in zip(self.__variables, self.__conditions,
                                           self.__valeurs, self.__types):
                valrow = row.get(var)

                # conversion dans le bon type pour la comparaison
                if typ == 'float':
                    valrow, val = float(valrow), float(val)
                elif typ == 'int':
                    valrow, val = int(valrow), int(val)
                elif typ == 'date':
                    valrow, val = datetime.fromisoformat(
                        valrow), datetime.fromisoformat(val)

                # comparaison
                if cond == '=':
                    check = check and valrow == val
                elif cond == '>':
                    check = check and valrow > val
                elif cond == '<':
                    check = check and valrow < val
                else:
                    check = check and valrow != val

            # si toutes les conditions sont remplies on garde l'observation
            if check:
                datares.append(row)

        return Dataset(dataset.header, datares)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
