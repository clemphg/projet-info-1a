"""
Produire des graphiques.

Graphiques classiques (x en fonction de y)
Séries temporelles (une ou plusieurs variables selon le temps)

Note : les tests utilises les tables créées par le __main__
"""
from datetime import datetime
import matplotlib.pyplot as plt


class LinePlot:
    """
    Classe permettant la création de graphiques.

    Elle est adaptée pour les données disponible dans un objet Dataset.

    Examples
    --------
    >>> from pipelinepackage.imports.importcsv import ImportCsv
    >>> lplot = LinePlot()
    >>> table = ImportCsv('data/output/conso_temp.csv', ';').importe()
    >>> lplot.plot(table, 't', 'consommation_brute_electricite_rte', 'Region')
    >>> lplot.serie_temp(table, 'date', 'consommation_brute_electricite_rte', 'Region')
    """

    def plot(self, dataset, varx, vary, groupby=None):
        """Plot classique (y en fonction de x)

        Affichage d'un graphique classique. Il est possible de grouper selon les modalités
        d'une autre variable du jeu de données.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données
        varx : str
            Variable que l'on veut en abscisse
        vary : str
            Variable que l'on veut en ordonnée
        groupby : str, optional
            Variable par les modalités de laquelle on regroupe les observations, by default None

        Examples
        --------
        >>> from pipelinepackage.imports.importcsv import ImportCsv
        >>> lplot = LinePlot()
        >>> table = ImportCsv('data/output/conso_temp.csv', ';').importe()
        >>> lplot.plot(table, 't', 'consommation_brute_electricite_rte', 'Region')
        """
        if groupby:
            groups = list(set([row[groupby] for row in dataset.body]))
            for group in groups:
                datax = [float(row[varx])
                         for row in dataset.body if row[groupby] == group]
                datay = [float(row[vary])
                         for row in dataset.body if row[groupby] == group]
                datax, datay = zip(*sorted(zip(datax, datay)))
                plt.plot(datax, datay, label=group)
                plt.legend()
        else:
            datax = [float(row[varx])
                     for row in dataset.body if row[varx] not in [None,'']]
            datay = [float(row[vary])
                     for row in dataset.body if row[vary] not in [None,'']]
            datax, datay = zip(*sorted(zip(datax, datay)))
            plt.plot(datax, datay)

        plt.xlabel(varx)
        plt.ylabel(vary)
        plt.title(vary+" en fonction de "+varx)
        plt.show()

    def serie_temp(self, dataset, vardate, vardata, groupby=None):
        """Plot d'une série temporelle (pour une seule variable)

        Affichage d'une série temporelle. Il est possible de grouper selon les modalités
        d'une autre variable du jeu de données.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données
        vardate : str
            Variable de date que l'on veut en abscisse
        vardata : str
            Variable que l'on veut en ordonnée
        groupby : str, optional
            Variable par les modalités de laquelle on regroupe les observations, by default None

        Examples
        --------
        >>> from pipelinepackage.imports.importcsv import ImportCsv
        >>> lplot = LinePlot()
        >>> table = ImportCsv('data/output/conso_temp.csv', ';').importe()
        >>> lplot.serie_temp(table, 'date', 'consommation_brute_electricite_rte', 'Region')
        """
        if groupby:
            groups = list(set([row[groupby] for row in dataset.body]))
            for group in groups:
                dates = [datetime.fromisoformat(
                    row[vardate]) for row in dataset.body if row[groupby] == group]
                data = [float(row.get(vardata))
                        for row in dataset.body if row[groupby] == group]
                dates, data = zip(*sorted(zip(dates, data)))
                plt.plot(dates, data, label=group)
                plt.legend()
        else:
            dates = [datetime.fromisoformat(row[vardate])
                     for row in dataset.body]
            data = [float(row.get(vardata)) if row.get(vardata) not in ['', None] else None
                    for row in dataset.body]
            dates, data = zip(*sorted(zip(dates, data)))
            plt.plot(dates, data)

        plt.xlabel("Temps")
        plt.ylabel(vardata)
        plt.title("Evolution de "+vardata+" selon le temps")
        plt.show()

    def series_temps(self, dataset, vardate, varsdata):
        """Plot de séries temporelles

        Affichage de plusieurs séries temporelles.

        Parameters
        ----------
        dataset : Dataset
            Jeu de données
        vardate : str
            Variable de date que l'on veut en abscisse
        varsdata : list[str]
            Variables que l'on veut en ordonnées

        Examples
        --------
        >>> from pipelinepackage.imports.importcsv import ImportCsv
        >>> lplot = LinePlot()
        >>> table = ImportCsv('data/output/conso_temp_bretagne.csv', ';').importe()
        >>> lplot.series_temps(table, 'date', ['moygli_t','moygli_consommation_brute_electricite_rte'])
        """
        for var in varsdata:
            dates = [datetime.fromisoformat(row[vardate])
                     for row in dataset.body]
            data = [float(row.get(var)) if row.get(var) not in ['', None] else None
                    for row in dataset.body]
            dates, data = zip(*sorted(zip(dates, data)))
            plt.plot(dates, data, label=var)

        plt.xlabel("Temps")
        plt.ylabel(','.join(varsdata))
        plt.title("Evolution de "+','.join(varsdata)+" selon le temps")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
