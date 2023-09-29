"""
Formater les dates
"""
from datetime import datetime
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset


class FormaterDate(Transformation):
    """Classe modélisant une transformation sur un jeu de données

    Attributes
    ----------
    variables : str ou list[str]
        Variable(s) de date sur laquelle/lesquelles effectuer la transformation
    dateformats : str ou list[str]
        Format de la date correspondant a/aux variables
        (variable et doivent avoir le même type et la même longueur si listes)

    Examples
    --------
    >>> data = Dataset(['nom', 'date', 'date2'], [{'nom': 'Clementine', 'date': '20041005230021', 'date2': '20100520'}, {'nom': 'Chloe', 'date': '20150720221515', 'date2': '20170201'}, {'nom': 'Maelle', 'date': '20010315155145', 'date2': '20190710'}])
    >>> a = FormaterDate(['date', 'date2'], ['%Y%m%d%H%M%S', '%Y%m%d'])
    >>> a.transforme(data).body
    [{'nom': 'Clementine', 'date': '2004-10-05 23:00:21', 'date2': '2010-05-20 00:00:00'}, {'nom': 'Chloe', 'date': '2015-07-20 22:15:15', 'date2': '2017-02-01 00:00:00'}, {'nom': 'Maelle', 'date': '2001-03-15 15:51:45', 'date2': '2019-07-10 00:00:00'}]
    """

    def __init__(self, variables, dateformats):
        """Constructeur

        Parameters
        ----------
        variables : str ou list[str]
           Variable(s) de date sur laquelle/lesquelles effectuer la transformation
        dateformats : str ou list[str]
            Format de la date correspondant a/aux variables
            (variable et doivent avoir le même type et la même longueur si listes)
        """
        super().__init__()
        self.__variables = variables
        self.__dateformats = dateformats

    def transforme(self, dataset):
        """Transformation de la date

        Création d'une chaine de caractères pour la date au bon format

        Parameters
        ----------
        dataset : Dataset
            Jeu de données dont on souhaite transformer une/des variable(s)

        Returns
        -------
        Dataset
            Jeu de données dont une/des variable(s) ont été mises au bon format

        Examples
        --------
        >>> data = Dataset(['nom', 'date', 'date2'], [{'nom': 'Clementine', 'date': '20041005230021', 'date2': '20100520'}, {'nom': 'Chloe', 'date': '20150720221515', 'date2': '20170201'}, {'nom': 'Maelle', 'date': '20010315155145', 'date2': '20190710'}])
        >>> a = FormaterDate(['date', 'date2'], ['%Y%m%d%H%M%S', '%Y%m%d'])
        >>> a.transforme(data).body
        [{'nom': 'Clementine', 'date': '2004-10-05 23:00:21', 'date2': '2010-05-20 00:00:00'}, {'nom': 'Chloe', 'date': '2015-07-20 22:15:15', 'date2': '2017-02-01 00:00:00'}, {'nom': 'Maelle', 'date': '2001-03-15 15:51:45', 'date2': '2019-07-10 00:00:00'}]
        """
        data = dataset.body
        body = []

        if isinstance(self.__variables, str):
            self.__variables = [self.__variables]
            self.__dateformats = [self.__dateformats]

        for row in data:
            for var, form in zip(self.__variables, self.__dateformats):
                datestr = datetime.strptime(
                    row[var], form).replace(tzinfo=None)
                row[var] = str(datestr)
            body.append(row)

        return Dataset(dataset.header, body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
