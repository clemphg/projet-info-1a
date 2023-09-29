"""
Obtention d'un fichier synchronisation en utilisant l'API Nominatim avec GeoPy.
"""
from geopy.geocoders import Nominatim
from pipelinepackage.synop.synop import Synop


class SynopGeopy(Synop):
    """Classe SynopGeopy

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
        de ses coordonnées géographiques. Utilise le package GeoPy dans
        lequel la classe Nominatim permet d'accéder à l'API éponyme.

        Parameters
        ----------
        row : dict
            Dictionnaire contenant des informations sur un lieu
        """
        localisation = Nominatim(user_agent="test", timeout=10).reverse(
            (lieu[self.lat], lieu[self.lon])).raw['address']

        return localisation
