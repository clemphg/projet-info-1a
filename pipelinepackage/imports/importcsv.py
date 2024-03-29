"""
Importer des fichiers .csv

Possibilité d'importer un fichier indivuellement ou tous les fichiers d'un dossier.
"""
import csv
import os
from pipelinepackage.imports.importation import Importation
from pipelinepackage.model.dataset import Dataset


class ImportCsv(Importation):
    """Modélisation de l'importation

    Attributes
    ----------
    chemin : str
        Chemin vers le fichier ou le dossier de fichiers à importer
    sep : str
        Séparateur utilisé pour le(s) fichier(s)
    """

    def __init__(self, chemin, sep):
        """Constructeur

        Parameters
        ----------
        chemin : str
            Chemin vers le fichier ou le dossier de fichiers à importer
        sep : str
            Séparateur utilisé pour le(s) fichier(s)
        """
        super().__init__(chemin)
        self.__sep = sep

    def importe(self):
        """Importe un jeu de données

        Returns
        -------
        Dataset
            Jeu de données importé
        """
        body = []

        lfiles = []

        if os.path.isfile(self.chemin):
            lfiles.append(self.chemin)
        else:
            for filename in os.listdir(self.chemin):
                lfiles.append(os.path.join(self.chemin, filename))

        for file in lfiles:
            if file.endswith(".csv"):

                with open(file, mode='rt', encoding='utf-8') as gzfile:
                    synopreader = csv.DictReader(
                        gzfile, delimiter=self.__sep)

                    # stockage des données dans une liste de dictionnaires
                    for row in synopreader:
                        body.append(row)

        header = list(body[0])

        return Dataset(header, body)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
