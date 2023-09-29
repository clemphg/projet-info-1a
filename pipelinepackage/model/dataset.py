""" Module dataset

Modélisation d'un jeu de données.

Examples
--------
Méthode header
>>> e = Dataset(["nom", "age"], [{"nom" : "Anne", "age" : 23}, {"nom" : "Thomas", "age" : 17}, {"nom" : "Gribouille", "age" : 7}, {"nom" : "Maelle", "age" : 21}])
>>> print(e.header)
['nom', 'age']

Méthode body
>>> d = Dataset(["nom", "age"], [{"nom" : "Anne", "age" : 23}, {"nom" : "Thomas", "age" : 17}])
>>> print(d.body)
[{'nom': 'Anne', 'age': 23}, {'nom': 'Thomas', 'age': 17}]

Méthode __str__
>>> d = Dataset(["nom", "age"], [{"nom" : "Anne", "age" : 23}, {"nom" : "Thomas", "age" : 17}, {"nom" : "Gribouille", "age" : 7}, {"nom" : "Maelle", "age" : 21}])
>>> print(d)
  Dimensions : 4 observations et 2 variables
  Variables  : ['nom', 'age']
"""


class Dataset:
    """ Classe Dataset

    Modélise un jeu de données

    Attributes
    ----------
    header : list[str]
        Variables du jeu de données
    body : list[dict]
        Observations du jeu de données(une observation est
        un élément de la liste donc un dictionnaire)

    Examples
    --------
    Méthode get_header()
    >>> d = Dataset(['nom', 'age'], [{'nom' : 'Anne', 'age' : '23'}, {'nom' : 'Clementine', 'age' : '17'}, {'nom' : 'Chloe', 'age' : '7'}, {'nom' : 'Maelle', 'age' : '21'}])
    >>> e = d.header
    >>> print(e)
    ['nom', 'age']
    """

    def __init__(self, header, body):
        """Constructeur

        Parameters
        ----------
        header : list[str]
            Variables du jeu de données
        body : list[dict]
            Observations du jeu de données (une observation est
            un élément de la liste donc un dictionnaire)
        """
        self.__header = header
        self.__body = body

    @property
    def header(self):
        """Variables du jeu de données

        Returns
        -------
        list
            Variables du jeu de données

        Examples
        --------
        >>> d = Dataset(["nom", "age"], [{"nom" : "Anne", "age" : 23}, {"nom" : "Thomas", "age" : 17}])
        >>> print(d.header)
        ['nom', 'age']
        """
        return self.__header

    @property
    def body(self):
        """Observations du jeu de données

        Returns
        -------
        list[dict]
            Observations du jeu de données

        Examples
        --------
        >>> d = Dataset(["nom", "age"], [{"nom" : "Anne", "age" : 23}, {"nom" : "Thomas", "age" : 17}])
        >>> print(d.body)
        [{'nom': 'Anne', 'age': 23}, {'nom': 'Thomas', 'age': 17}]
        """
        return self.__body

    def __str__(self):
        """Informations sur le jeu de données.

        Returns
        -------
        str
            Description du jeu de données

        Examples
        --------
        >>> d = Dataset(["nom", "age"], [{"nom" : "Anne", "age" : 23}, {"nom" : "Thomas", "age" : 17}, {"nom" : "Gribouille", "age" : 7}])
        >>> print(d)
          Dimensions : 3 observations et 2 variables
          Variables  : ['nom', 'age']
        """
        nrow, ncol = 0, 0
        if self.__body:
            nrow = len(self.__body)
            ncol = len(self.__header)
        dim = "  Dimensions : " + \
            str(nrow)+" observations et "+str(ncol)+" variables"
        var = "\n  Variables  : "+str(self.__header)
        return dim+var


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
