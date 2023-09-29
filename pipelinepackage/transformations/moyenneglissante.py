"""
Calculer la moyenne glissante d'un jeu de données.

Ne peut d'appliquer qu'à une variable numérique.
"""
from math import floor
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset
from pipelinepackage.estimateurs.estimateur import Estimateur


class MoyenneGlissante(Transformation):

    def __init__(self, variable, nvals, vardate):
        """Contructeur

        Parameters
        ----------
        variable : str
            Nom de la variable sur laquelle calculer la moyenne mobile
        nvals : int
            Nombre de valeurs sur lesquelles calculer la moyenne mobile (impair)
        vardate : str
            Nom de la variable de date du jeu de données

        Examples
        --------
        >>> data = Dataset(['prix', 'date'], [{'prix': 15, 'date': '2020-01-01'}, {'prix': 17, 'date': '2020-02-01'}, {'prix': 16, 'date': '2020-03-01'}, {'prix': 16, 'date': '2020-04-01'}, {'prix': 11, 'date': '2020-05-01'}, {'prix': 10, 'date': '2020-06-01'}, {'prix': 11, 'date': '2020-07-01'}, {'prix': 14, 'date': '2020-08-01'}, {'prix': 15, 'date': '2020-09-01'}, {'prix': 18, 'date': '2020-10-01'}, {'prix': 20, 'date': '2020-11-01'}, {'prix': 19, 'date': '2020-12-01'}, {'prix': 18, 'date': '2021-01-01'}, {'prix': 16, 'date': '2021-02-01'}])
        >>> a = MoyenneGlissante('prix', 3, 'date')
        >>> a.transforme(data).body
        [{'prix': 15, 'date': '2020-01-01'}, {'prix': 17, 'date': '2020-02-01', 'moygli_prix': 16.0}, {'prix': 16, 'date': '2020-03-01', 'moygli_prix': 16.333}, {'prix': 16, 'date': '2020-04-01', 'moygli_prix': 14.333}, {'prix': 11, 'date': '2020-05-01', 'moygli_prix': 12.333}, {'prix': 10, 'date': '2020-06-01', 'moygli_prix': 10.667}, {'prix': 11, 'date': '2020-07-01', 'moygli_prix': 11.667}, {'prix': 14, 'date': '2020-08-01', 'moygli_prix': 13.333}, {'prix': 15, 'date': '2020-09-01', 'moygli_prix': 15.667}, {'prix': 18, 'date': '2020-10-01', 'moygli_prix': 17.667}, {'prix': 20, 'date': '2020-11-01', 'moygli_prix': 19.0}, {'prix': 19, 'date': '2020-12-01', 'moygli_prix': 19.0}, {'prix': 18, 'date': '2021-01-01', 'moygli_prix': 17.667}, {'prix': 16, 'date': '2021-02-01'}]
        """
        super().__init__()
        self.__variable = variable
        self.__nvals = nvals
        self.__vardate = vardate

    def transforme(self, dataset):
        """Transformation d'un jeu de données.

        Calcul de la moyenne glissante sur un jeu de données.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données sur lequel on souhaite calculer la moyenne glissante.

        Returns
        -------
        Dataset
            Jeu de données avec une nouvelle variable contenant la moyenne mobile.
        Examples
        --------
        >>> data = Dataset(['prix', 'date'], [{'prix': 15, 'date': '2020-01-01'}, {'prix': 17, 'date': '2020-02-01'}, {'prix': 16, 'date': '2020-03-01'}, {'prix': 16, 'date': '2020-04-01'}, {'prix': 11, 'date': '2020-05-01'}, {'prix': 10, 'date': '2020-06-01'}, {'prix': 11, 'date': '2020-07-01'}, {'prix': 14, 'date': '2020-08-01'}, {'prix': 15, 'date': '2020-09-01'}, {'prix': 18, 'date': '2020-10-01'}, {'prix': 20, 'date': '2020-11-01'}, {'prix': 19, 'date': '2020-12-01'}, {'prix': 18, 'date': '2021-01-01'}, {'prix': 16, 'date': '2021-02-01'}])
        >>> a = MoyenneGlissante('prix', 3, 'date')
        >>> a.transforme(data).body
        [{'prix': 15, 'date': '2020-01-01'}, {'prix': 17, 'date': '2020-02-01', 'moygli_prix': 16.0}, {'prix': 16, 'date': '2020-03-01', 'moygli_prix': 16.333}, {'prix': 16, 'date': '2020-04-01', 'moygli_prix': 14.333}, {'prix': 11, 'date': '2020-05-01', 'moygli_prix': 12.333}, {'prix': 10, 'date': '2020-06-01', 'moygli_prix': 10.667}, {'prix': 11, 'date': '2020-07-01', 'moygli_prix': 11.667}, {'prix': 14, 'date': '2020-08-01', 'moygli_prix': 13.333}, {'prix': 15, 'date': '2020-09-01', 'moygli_prix': 15.667}, {'prix': 18, 'date': '2020-10-01', 'moygli_prix': 17.667}, {'prix': 20, 'date': '2020-11-01', 'moygli_prix': 19.0}, {'prix': 19, 'date': '2020-12-01', 'moygli_prix': 19.0}, {'prix': 18, 'date': '2021-01-01', 'moygli_prix': 17.667}, {'prix': 16, 'date': '2021-02-01'}]
        """
        body = dataset.body
        header = dataset.header

        # tri du jeu de données dans l'ordre croissant selon la variable de date
        nb_row = len(body)
        for i in range(1, nb_row):
            cle = body[i]
            j = i-1
            while j >= 0 and body[j][self.__vardate] > cle[self.__vardate]:
                body[j+1] = body[j]
                j = j-1
            body[j+1] = cle

        # nom de la nouvelle variable à ajouter au jeu de données
        new_var = "moygli_"+self.__variable
        header.append(new_var)

        estim = Estimateur(self.__variable)

        # calcul du pas à gauche et à droite
        step_deb = floor(self.__nvals/2)
        step_fin = step_deb-1 if self.__nvals % 2 == 0 else step_deb

        # calcul de la moyenne glissante
        for i in range(step_deb, len(body)-step_fin):
            temp = body[i-step_deb:i+step_fin+1]
            moytemp = estim.moyenne(Dataset(dataset.header, temp))
            body[i][new_var] = moytemp

        return Dataset(header, body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
