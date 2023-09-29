"""
module jointure

Joindre deux jeux de données selon un ou plusieurs pivots.

Examples
--------
Jointure interne entre data et data_bis selon les pivots 'A' et 'B'
>>> data = Dataset(['A', 'B', 'C'], [{'A': 'a', 'B': 't', 'C': 1}, {'A': 'b', 'B': 'u', 'C': 2}, {'A': 'c', 'B': 'v', 'C': 3}])
>>> data_bis = Dataset(['a', 'b', 'd'], [{'a': 'a', 'b': 't', 'd': '3'}, {'a': 'b', 'b': 'u', 'd': '2'}, {'a': 'd', 'b': 'w', 'd': '1'}])
>>> a = Jointure(data_bis, ['A', 'B'], ['a', 'b'])
>>> a.transforme(data).body
[{'A': 'a', 'B': 't', 'C': 1, 'd': '3'}, {'A': 'b', 'B': 'u', 'C': 2, 'd': '2'}]

Jointure à gauche entre data et data_bis selon les pivots 'A' et 'B'
>>> data = Dataset(['A', 'B', 'C'], [{'A': 'a', 'B': 't', 'C': 1}, {'A': 'b', 'B': 'u', 'C': 2}, {'A': 'c', 'B': 'v', 'C': 3}])
>>> data_bis = Dataset(['A', 'B', 'D'], [{'A': 'a', 'B': 't', 'D': '3'}, {'A': 'b', 'B': 'u', 'D': '2'}, {'A': 'd', 'B': 'w', 'D': '1'}])
>>> a = Jointure(data_bis, ['A', 'B'], ['A', 'B'], 'left')
>>> a.transforme(data).body
[{'A': 'a', 'B': 't', 'C': 1, 'D': '3'}, {'A': 'b', 'B': 'u', 'C': 2, 'D': '2'}, {'A': 'c', 'B': 'v', 'C': 3}]

Jointure à droite entre data et data_bis selon les pivots 'A' et 'B'
>>> data = Dataset(['A', 'B', 'C'], [{'A': 'a', 'B': 't', 'C': 1}, {'A': 'b', 'B': 'u', 'C': 2}, {'A': 'c', 'B': 'v', 'C': 3}])
>>> data_bis = Dataset(['A', 'B', 'D'], [{'A': 'a', 'B': 't', 'D': '3'}, {'A': 'b', 'B': 'u', 'D': '2'}, {'A': 'd', 'B': 'w', 'D': '1'}])
>>> a = Jointure(data_bis, ['A', 'B'], ['A', 'B'], 'right')
>>> a.transforme(data).body
[{'A': 'a', 'B': 't', 'C': 1, 'D': '3'}, {'A': 'b', 'B': 'u', 'C': 2, 'D': '2'}, {'A': 'd', 'B': 'w', 'D': '1'}]

Jointure complète entre data et data_bis selon les pivots 'A' et 'B'
>>> data = Dataset(['A', 'B', 'C'], [{'A': 'a', 'B': 't', 'C': 1}, {'A': 'b', 'B': 'u', 'C': 2}, {'A': 'c', 'B': 'v', 'C': 3}])
>>> data_bis = Dataset(['A', 'B', 'D'], [{'A': 'a', 'B': 't', 'D': '3'}, {'A': 'b', 'B': 'u', 'D': '2'}, {'A': 'd', 'B': 'w', 'D': '1'}])
>>> a = Jointure(data_bis, ['A', 'B'], ['A', 'B'], 'full')
>>> a.transforme(data).body
[{'A': 'a', 'B': 't', 'C': 1, 'D': '3'}, {'A': 'b', 'B': 'u', 'C': 2, 'D': '2'}, {'A': 'c', 'B': 'v', 'C': 3}, {'A': 'd', 'B': 'w', 'D': '1'}]
"""
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset


class Jointure(Transformation):
    """classe Jointure

    Modélise une jointure entre deux jeux de données selon un ou plusieurs pivots.

    Attributs
    ---------
    dataset_bis : Dataset
        Jeu de données avec lequel on veut faire la fusion
    pivots : list[str]
        Variables "pivots" du dataset, sur lesquelles on effectue la jointure
    pivots_bis : list[str]
        Variables "pivots" correspondant à pivots pour dataset_bis
    typej : str
        Type de jointure, by default 'inner' (peut être aussi 'full', left', 'right')

    Examples
    --------
    Jointure entre data et data_bis selon les pivots 'A' et 'B'
    >>> data = Dataset(['A', 'B', 'C'], [{'A': 'a', 'B': 't', 'C': 1}, {'A': 'b', 'B': 'u', 'C': 2}, {'A': 'c', 'B': 'v', 'C': 3}])
    >>> data_bis = Dataset(['A', 'B', 'D'], [{'A': 'a', 'B': 't', 'D': '3'}, {'A': 'b', 'B': 'u', 'D': '2'}, {'A': 'd', 'B': 'w', 'D': '1'}])
    >>> a = Jointure(data_bis, ['A', 'B'], ['A', 'B'], 'right')
    >>> a.transforme(data).body
    [{'A': 'a', 'B': 't', 'C': 1, 'D': '3'}, {'A': 'b', 'B': 'u', 'C': 2, 'D': '2'}, {'A': 'd', 'B': 'w', 'D': '1'}]
    """

    def __init__(self, dataset_bis, pivots, pivots_bis, typej='inner'):
        """Constructeur

        Attributs
        ---------
        dataset_bis : Dataset
            Jeu de données avec lequel on veut faire la fusion
        pivots : list[str]
            Variables "pivots" du dataset, sur lesquelles on effectue la jointure
        pivots_bis : list[str]
            Variables "pivots" correspondant à pivots pour dataset_bis
        typej : str
            Type de jointure, by default 'inner' (peut être aussi 'full', left', 'right')
        """
        super().__init__()
        self.__dataset_bis = dataset_bis
        self.__pivots = pivots
        self.__pivots_bis = pivots_bis
        self.__typej = typej

    def transforme(self, dataset):
        """Jointure de deux jeux de données.

        Jointure de deux jeux de données selon un ou plusieurs pivots.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données auquel on souhaite joindre le jeu de données passé en attribut.

        Returns
        -------
        Dataset
            Jeu de données résultant de la jointure.

        Examples
        --------
        Jointure à gauche entre data et data_bis selon les pivots 'A' et 'B'
        >>> data = Dataset(['A', 'B', 'C'], [{'A': 'a', 'B': 't', 'C': 1}, {'A': 'b', 'B': 'u', 'C': 2}, {'A': 'c', 'B': 'v', 'C': 3}])
        >>> data_bis = Dataset(['a', 'b', 'd'], [{'a': 'a', 'b': 't', 'd': '3'}, {'a': 'b', 'b': 'u', 'd': '2'}, {'a': 'd', 'b': 'w', 'd': '1'}])
        >>> a = Jointure(data_bis, ['A', 'B'], ['a', 'b'], 'left')
        >>> a.transforme(data).body
        [{'A': 'a', 'B': 't', 'C': 1, 'd': '3'}, {'A': 'b', 'B': 'u', 'C': 2, 'd': '2'}, {'A': 'c', 'B': 'v', 'C': 3}]
        """
        datares = []

        data_bis = {}
        for row in self.__dataset_bis.body:
            cle = ''
            for var in self.__pivots_bis:
                cle += row[var]
            data_bis[cle] = row

        for row in dataset.body:
            cle = ''
            for var in self.__pivots:
                cle += row[var]

            # si clé dans les deux tables
            if data_bis.get(cle) is not None:
                rowdata = {key: value for d in (row, data_bis[cle])
                           for key, value in d.items()}
                for pivot_a, pivot_b in zip(self.__pivots, self.__pivots_bis):
                    if pivot_a != pivot_b:
                        del rowdata[pivot_b]
                datares.append(rowdata)

                # suppression si ligne ajoutée au résultat (sert pour 'full' et 'right')
                del data_bis[cle]

            # si la clé n'est que dans dataset_bis mais on fait une jointure full ou left
            elif self.__typej in ['full', 'left']:
                datares.append(row)

        # dans le cas d'une jointure full ou right on veut récupérer les clés du second
        # jeu de données qui n'apparaissaient pas dans le premier
        if self.__typej in ['full', 'right'] and data_bis:
            for obs in data_bis.values():
                # renommage des variables pivots afin qu'elles aient le même nom que celles
                # du premier jeu de données
                for vara, varb in zip(self.__pivots, self.__pivots_bis):
                    if vara != varb:
                        obs[vara] = obs[varb]
                        del obs[varb]
                datares.append(obs)

        header = dataset.header + [elem for elem in self.__dataset_bis.header
                                   if elem not in self.__pivots_bis]

        return Dataset(header, datares)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
