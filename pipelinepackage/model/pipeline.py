"""
Modélisation d'un pipeline de données

Examples
--------
>>> from pipelinepackage.imports.importjsongz import ImportJsonGz
>>> from pipelinepackage.exports.exportcsvgz import ExportCsvGz
>>> from pipelinepackage.transformations.selectionvariables import SelectionVariables
>>> a = Pipeline([ImportJsonGz('data/input/2022-01.json.gz'), SelectionVariables(['region','consommation_brute_electricite_rte']), ExportCsvGz(filename='conso_elec.csv.gz')])
>>> a.run()
"""

class Pipeline:
    """Modélisation d'un pipeline de données

    Attributes
    ----------
    ltransfo : list[str]
        Liste contenant l'import de la table, les transformations à effectuer sur celle-ci et l'export.

    Examples
    --------
    >>> from pipelinepackage.imports.importjsongz import ImportJsonGz
    >>> from pipelinepackage.exports.exportcsvgz import ExportCsvGz
    >>> from pipelinepackage.transformations.selectionvariables import SelectionVariables
    >>> a = Pipeline([ImportJsonGz('data/input/2022-01.json.gz'), SelectionVariables(['region','consommation_brute_electricite_rte']), ExportCsvGz(filename='conso_elec.csv.gz')])
    >>> a.run()
    """

    def __init__(self, ltransfo):
        """Constructeur

        Parameters
        ----------
        ltransfo : list[Transformation]
            Liste de transformation (commence par un import et fini par un export)
        """
        self.__ltransfo = ltransfo

    def run(self):
        """
        Execution du pipeline

        Les transformations passées en attribut sont effectuées,
        le jeu de données est disponible au chemin passé à l'export.

        Examples
        --------
        >>> from pipelinepackage.imports.importjsongz import ImportJsonGz
        >>> from pipelinepackage.exports.exportcsvgz import ExportCsvGz
        >>> from pipelinepackage.transformations.selectionvariables import SelectionVariables
        >>> a = Pipeline([ImportJsonGz('data/input/2022-01.json.gz'), SelectionVariables(['region','consommation_brute_electricite_rte']), ExportCsvGz(filename='conso_elec.csv.gz')])
        >>> a.run()
        """
        table = self.__ltransfo[0].importe()

        for transfo in self.__ltransfo[1:len(self.__ltransfo)-1]:
            table = transfo.transforme(table)

        self.__ltransfo[-1].exporte(table)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)