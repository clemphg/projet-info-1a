"""
BONUS

Obtention de la région administrative de lieux à partir de leurs coordonnées géographiques.
"""
from abc import ABC, abstractmethod
import csv
import time


class Synop(ABC):
    """Classe Synop

    Permet d'associer à un lieu dont on dispose des coordonnées géographiques
    des informations telles que son département, sa région ou son pays. Cette
    implémentation ne permet de faire cela que pour les lieux situés en France.

    Attributes
    ----------
    synopfile : str
        Fichier csv contenant les lieux avec leur latitude et longitude
    outputfile : str
        Fichier csv dans lequel le résultat est sauvegardé
    lat : str
        Nom de la variable de latitude
    lon : str
        Nom de la variable de longitude
    """

    def __init__(self, synopfile, outputfile, lat, lon):
        """Constructeur

        Parameters
        ----------
        synopfile : str
            Fichier csv contenant les lieux avec leur latitude et longitude
        outputfile : str
            Fichier csv dans lequel le résultat est sauvegardé
        lat : str
            Nom de la variable de latitude
        lon : str
            Nom de la variable de longitude
        """
        self.__synopfile = synopfile
        self.__outputfile = outputfile
        self.__lat = lat
        self.__lon = lon

    @property
    def lat(self):
        """ Getter pour l'attribut privé lat (nom de la variable de latitude) """
        return self.__lat

    @ property
    def lon(self):
        """ Getter pour l'attribut privé lon (nom de la variable de longitude) """
        return self.__lon

    @abstractmethod
    def get_address(self, lieu):
        """Adresse d'un lieu

        Obtenir un dictionnaire décrivant l'adresse d'un lieu
        à partir de ses coordonnées géographiques.

        Parameters
        ----------
        lieu : dict
            Dictionnaire contenant des informations sur un lieu
        """

    def region(self, address):
        """Region correspondant à une adresse

        Parameters
        ----------
        address : dict
            Dictionnaire décrivant l'adresse d'un lieu (obtenu avec get_address)

        Returns
        -------
        str
            Région correspondante (en toutes lettres)
        """
        if address.get('region') in ['France métropolitaine', None]:
            region = address.get('state')
        else:
            region = address.get('region')
        return region

    def departement(self, address):
        """Département correspondant à une adresse

        Parameters
        ----------
        address : dict
            Dictionnaire décrivant l'adresse d'un lieu (obtenu avec get_address)

        Returns
        -------
        str
            Département correspondant (en toutes lettres)
        """
        if address.get('region') == 'France métropolitaine':
            departement = address.get('county')
        elif not address.get('region'):
            departement = address.get('state')
        else:
            departement = address.get('municipality')
        return departement

    def pays(self, address):
        """Pays correspondant à une adresse

        Parameters
        ----------
        address : dict
            Dictionnaire décrivant l'adresse d'un lieu (obtenu avec get_address)

        Returns
        -------
        str
            Pays correspondant (en toutes lettres)
        """
        return address.get('country')

    def synchro(self, echelons):
        """Associer un lieu à plusieurs de ses caractéristiques

        Cette méthode permet d'ajouter le département, la région
        ou le pays aux informations sur lieu situé en France.

        Parameters
        ----------
        echelons : list[str]
            Echelles à ajouter, peut prendre 3 valeurs : 'departement', 'region' ou 'pays'
        """
        echelons = [echelon.capitalize() for echelon in echelons]

        # dictionnaire des correspondances échelon/méthode
        corr = {'Departement': self.departement,
                'Region': self.region,
                'Pays': self.pays}

        # ouverture de deux fichiers csv, l'un en lecture l'autre en écriture
        with open(self.__synopfile,
                  mode='r',
                  encoding='utf-8') as synopr, open(self.__outputfile,
                                                    mode='w',
                                                    newline='',
                                                    encoding='utf-8') as synopw:
            csv_reader = csv.DictReader(synopr, delimiter=";")

            # liste des variables
            names = csv_reader.fieldnames
            for echelon in echelons:
                if echelon in ['Departement', 'Region', 'Pays']:
                    names.append(echelon)

            csv_writer = csv.DictWriter(synopw, fieldnames=names)
            csv_writer.writeheader()

            for lieu in csv_reader:
                adresse = self.get_address(lieu)

                for echelon in echelons:
                    val = corr[echelon](adresse)
                    lieu[echelon] = val

                csv_writer.writerow(lieu)

                # nouvelle requête toutes les 5 secondes
                time.sleep(5)
