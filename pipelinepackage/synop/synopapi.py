"""
Obtention d'un fichier synchronisation en utilisant l'API Nominatim avec requests.
"""
import requests
from pipelinepackage.synop.synop import Synop


class SynopAPI(Synop):
    """Classe SynopAPI

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
        super().__init__(synopfile, outputfile, lat, lon)

    def get_address(self, lieu):
        """Adresse d'un lieu

        Obtenir un dictionnaire décrivant l'adresse d'un lieu à partir
        de ses coordonnées géographiques. On utilise ici directement
        l'API Nominatim avec requests.

        Parameters
        ----------
        lieu : dict
            Dictionnaire contenant des informations sur un lieu
        """
        urlapi = 'https://nominatim.openstreetmap.org/reverse'
        params = {'format': 'jsonv2',
                  'lat': lieu[self.lat],
                  'lon': lieu[self.lon]}

        address = requests.get(
            url=urlapi, params=params).json()['address']

        return address
