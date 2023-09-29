"""
module exportcsv

Exporter un jeu de données au format .csv

Examples
--------
>>> c=ExportCsv('data/output')
"""
import csv
import os
from pipelinepackage.exports.exportation import Exportation


class ExportCsv(Exportation):
    """Classe ExportCsv

    Modélise une exportation de fichier au format .csv

    Attributes
    ----------
    chemin : str, optional
        Dossier dans lequel sauvegarder le résultat, by default "data/output"
    filename : str, optional
        Nom du fichier résultat, by default "tableau.csv"
    sep : str, optional
        Séparateur à utiliser, by default ';'

    Examples
    --------
    >>> c=ExportCsv('data/output',sep=',')
    """

    def __init__(self, chemin="data/output", filename="tableau.csv", sep=";"):
        """Constructeur

        Parameters
        ----------
        chemin : str, optional
            Dossier dans lequel sauvegarder le résultat, by default "data/output"
        filename : str, optional
            Nom du fichier résultat, by default "tableau.csv"
        sep : str, optional
            Séparateur à utiliser, by default ";"
        """
        super().__init__(chemin, filename)
        self.__sep = sep

    def exporte(self, dataset):
        """Exporte le jeu de données

        Exporte le jeu de données dataset passé en paramètre au format .csv

        Parameters
        ----------
        dataset : Dataset
            Jeu de données à exporter

        Examples
        --------
        >>> c=ExportCsv('data/output', 'tab.csv', ',')
        """
        with open(os.path.join(self.chemin, self.filename),
                  'wt', encoding='UTF8', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, delimiter=self.__sep, fieldnames=dataset.header)
            writer.writeheader()
            writer.writerows(dataset.body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
