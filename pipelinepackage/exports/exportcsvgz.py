"""
module exportcsvgz

Exporter un jeu de données au format .csv.gz

Examples
--------
>>> c=ExportCsvGz('data/output')
"""
import gzip
import csv
import os
from pipelinepackage.exports.exportation import Exportation


class ExportCsvGz(Exportation):
    """Classe ExportCsvGz

    Modélise une exportation de fichier

    Attributes
    ----------
    chemin : str, optional
        Dossier dans lequel sauvegarder le résultat, by default "data/output"
    filename : str, optional
        Nom du fichier résultat, by default "tableau.csv.gz"
    sep : str, optional
        Séparateur à utiliser, by default ';'

    Examples
    --------
    >>> c=ExportCsvGz('data/output', sep=';')
    """

    def __init__(self, chemin="data/output", filename="tableau.csv.gz", sep=";"):
        """Constructeur

        Parameters
        ----------
        chemin : str, optional
            Dossier dans lequel sauvegarder le résultat, by default "data/output"
        filename : str, optional
            Nom du fichier résultat, by default "tableau.csv.gz"
        sep : str, optional
            Séparateur à utiliser, by default ";"
        """
        super().__init__(chemin, filename)
        self.__sep = sep

    def exporte(self, dataset):
        """Exporte le jeu de données

        Exporte le jeu de données dataset passé en paramètre au format .csv.gz

        Parameters
        ----------
        dataset : Dataset
            Jeu de données à exporter

        Examples
        --------
        >>> c=ExportCsvGz('data/output', 'tab.csv.gz', ';')
        """
        with gzip.open(os.path.join(self.chemin, self.filename),
                       'wt', encoding='UTF8', newline='') as csvgzfile:
            writer = csv.DictWriter(
                csvgzfile, delimiter=self.__sep, fieldnames=dataset.header)
            writer.writeheader()
            writer.writerows(dataset.body)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
