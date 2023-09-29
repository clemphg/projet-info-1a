"""
Importer des fichiers .json.gz

Possibilité d'importer un fichier indivuellement ou tous les fichiers d'un dossier.

Examples
--------
>>> c=ImportJsonGz('data/input/2022-01.json.gz')
"""
import gzip
import json
import os
from pipelinepackage.imports.importation import Importation
from pipelinepackage.model.dataset import Dataset


class ImportJsonGz(Importation):
    """Modélisation de l'importation

    Attributes
    ----------
    chemin : str
        Chemin vers le fichier ou le dossier de fichiers à importer

    Examples
    --------
    >>> c=ImportJsonGz('data/input/2022-01.json.gz')
    """

    def __init__(self, chemin):
        """Constructeur

        Parameters
        ----------
        chemin : str
            Chemin vers le fichier ou le dossier de fichiers à importer
        """
        super().__init__(chemin)

    def importe(self):
        """Importe un jeu de données

        Returns
        -------
        Dataset
            Jeu de données importé

        Examples
        --------
        >>> c=ImportJsonGz('data/input/2022-01.json.gz')
        """
        body = []

        lfiles = []

        if os.path.isfile(self.chemin):
            lfiles.append(self.chemin)
        else:
            for filename in os.listdir(self.chemin):
                lfiles.append(os.path.join(self.chemin, filename))

        for file in lfiles:
            if file.endswith(".json.gz"):
                with gzip.open(file, mode="rt", encoding='utf-8') as gzfile:
                    body.extend(
                        json.load(gzfile, parse_float=float, parse_int=float))

        header = []

        # récupérer toutes les clés (les noms des variables) et les valeurs
        # contenues dans les champs 'fields'
        # on doit parcourir toutes les observations car les valeurs manquantes
        # font que des clés peuvent ne pas être dans toutes les observations.
        body = [row['fields'] for row in body]
        for row in body:
            header = list(set(header) | set(list(row)))

        return Dataset(header, body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
