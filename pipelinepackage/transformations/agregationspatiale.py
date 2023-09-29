""""
Module d'aggrégation spatiale

Agréger des données à un certain échelon, en utilisant un fichier csv
associant cet échelon à l'échelon auquel sont actuellement les données.

Attention, l'agrégation ne peut être faite qu'avec des données numériques.
Les variables d'autres types (sauf pivot et cariable d'échelle) devront soit
être renseignées dans l'attribut groupby, soit être supprimées.
"""
import csv
from pipelinepackage.transformations.selectionvariables import SelectionVariables
from pipelinepackage.transformations.transformation import Transformation
from pipelinepackage.model.dataset import Dataset


class AgregationSpatiale(Transformation):
    """Classe AgregationSpatiale

    Attributes
    ----------
    filesynop : str
        Fichier csv de synchronisation (fait le lien entre echelle et
        pivotdata, par exemple la région et l'id de la station météo)
    pivotsynop : str
        Nom de la variable de filesynop qui est commune avec le jeu de données
    pivotdata : str
        Nom de la variable du jeu de données qui est commune avec filesynop
    echelle : str
        Nom de l'échelle à laquelle agréger (nom de la variable dans filesynop)
    groupby : list, optional
        Variables par lesquelles grouper les données (par exemple la date), by default None
    fonction : function, optional
        Fonction d'agrégation, by default lambdax:sum(x)/len(x)
    """

    def __init__(self, filesynop, pivotsynop, pivotdata, echelle,
                 groupby=None, fonction=lambda x: sum(x)/len(x)):
        """Constructeur

        Parameters
        ----------
        filesynop : str
            Fichier csv de synchronisation (fait le lien entre echelle et
            pivotdata, par exemple la région et l'id de la station météo)
        pivotsynop : str
            Nom de la variable de filesynop qui est commune avec le jeu de données
        pivotdata : str
            Nom de la variable du jeu de données qui est commune avec filesynop
        echelle : str
            Nom de l'échelle à laquelle agréger (nom de la variable dans filesynop)
        groupby : list, optional
            Variables par lesquelles grouper les données (par exemple la date), by default None
        fonction : function, optional
            Fonction d'agrégation, by default lambdax:sum(x)/len(x)
        """
        super().__init__()
        self.__filesynop = filesynop
        self.__echelle = echelle
        self.__pivotsynop = pivotsynop
        self.__pivotdata = pivotdata
        self.__groupby = groupby
        self.__fonction = fonction

    def fusion_synop(self, dataset):
        """Fusion du fichier synop avec le jeu de données

        Ajoute l'échelle sélectionnée comme nouvelle variable du jeu de données

        Parameters
        ----------
        dataset : Dataset
            Jeu de données
        """

        header = dataset.header
        data = dataset.body
        header.append(self.__echelle)

        body = []
        synop = []

        # ouverture du fichier de synchronisation
        with open(self.__filesynop, mode='r', encoding='utf-8') as csvr:
            csv_reader = csv.DictReader(csvr, delimiter=",")
            for row in csv_reader:
                synop.append(row)

        # ajout de la nouvelle variable echelle au jeu de données
        for row_a in data:
            for row_b in synop:
                if row_a[self.__pivotdata] == row_b[self.__pivotsynop]:
                    row_a[self.__echelle] = row_b[self.__echelle]
                    body.append(row_a)

        header.remove(self.__pivotdata)

        # suppression de la variable pivot dans le jeu de données
        sel = SelectionVariables(header)
        result = sel.transforme(Dataset(header, body))
        return result

    def transforme(self, dataset):

        table = self.fusion_synop(dataset)

        body = table.body
        header = table.header

        # table dans laquelle on groupe les obs
        groups = {}

        # agrégation des lignes selon les groupes
        for row in body:
            cle = row[self.__echelle]

            # concaténation des valeurs des variables par lesquelles on groupe
            if self.__groupby:
                for var in self.__groupby:
                    cle = cle + row[var]

            # ajout au dictionnaire groups
            if cle in groups:
                groups[cle].append(row)
            else:
                groups[cle] = [row]

        datares = []
        if self.__groupby:
            vargroup = [self.__echelle] + self.__groupby
        else:
            vargroup = [self.__echelle]

        # calcul des valeurs agrégées sur chaque groupe
        for data in groups.values():

            obsag = {}

            for var in header:
                if var not in vargroup:
                    vals = [float(row.get(var))
                            for row in data if row.get(var) is not None]
                    obsag[var] = self.__fonction(vals)
                else:
                    obsag[var] = data[0][var]

            datares.append(obsag)

        return Dataset(header, datares)
