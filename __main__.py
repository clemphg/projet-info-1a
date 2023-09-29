"""
Environnement d'exécution principal

Dans ce fichier se trouve un exemple d'utilisation de ce pipeline.
Veuillez veiller à ce que les chemins vers les fichiers soient bien renseignés.
Une documentation de chacune des classes utilisées est disponible et devrait être
consultée pour une utilisation facilitée de l'application.
"""
from pipelinepackage.imports.importcsvgz import ImportCsvGz
from pipelinepackage.imports.importjsongz import ImportJsonGz
from pipelinepackage.imports.importcsv import ImportCsv

from pipelinepackage.transformations.agregationspatiale import AgregationSpatiale
#from pipelinepackage.transformations.centrage import Centrage
from pipelinepackage.transformations.enlevevalmq import EnleveValMq
#from pipelinepackage.transformations.fenetrage import Fenetrage
from pipelinepackage.transformations.formaterdate import FormaterDate
from pipelinepackage.transformations.jointure import Jointure
from pipelinepackage.transformations.moyenneglissante import MoyenneGlissante
from pipelinepackage.transformations.normalisation import Normalisation
from pipelinepackage.transformations.selectionvariables import SelectionVariables
from pipelinepackage.transformations.selectionobservations import SelectionObservations

from pipelinepackage.exports.exportcsv import ExportCsv
from pipelinepackage.exports.exportcsvgz import ExportCsvGz

from pipelinepackage.model.pipeline import Pipeline
from pipelinepackage.plots.lineplot import LinePlot


#### SYNCHRONISATION DEP/REGION/PAYS ####

# from pipeline.synop.synopapi import SynopAPI
# from pipeline.synop.synopgeopy import SynopGeopy

# synop = SynopAPI('data/synop/postesSynop.csv','data/synop/postesSynopTout.csv',
#                 'Latitude', 'Longitude')
# synop.synchro(['departement', 'region', 'pays'])


#### EXEMPLE 1 : RELATION ENTRE TEMPERATURE ET CONSO ELEC ####
# Y a-t-il une relation entre température et consommation électrique ?

# Jeu de données de consommation électrique
Pipeline([ImportJsonGz('data/input/2022-01.json.gz'),
          SelectionVariables(
              ['region', 'date_heure', 'consommation_brute_electricite_rte']),
          EnleveValMq([None]),
          FormaterDate('date_heure', '%Y-%m-%dT%H:%M:%S%z'),
          ExportCsvGz(filename='conso_elec.csv.gz')]).run()

# Jeu de données sur la température et jointure avec la consommation électrique (région et date)
Pipeline([ImportCsvGz('data/input/synop.202201.csv.gz', ';'),
          SelectionVariables(['numer_sta', 'date', 't']),
          EnleveValMq([None, 'mq']),
          FormaterDate('date', '%Y%m%d%H%M%S'),
          AgregationSpatiale('data/synop/postesSynopAvecRegions.csv',
                             'ID', 'numer_sta', 'Region', groupby=['date']),
          Jointure(ImportCsvGz('data/output/conso_elec.csv.gz', ';').importe(),
                   ['Region', 'date'], ['region', 'date_heure']),
          ExportCsv(filename="conso_temp.csv")]).run()

# Jeu de données température/consommation électrique pour la Bretagne
Pipeline([ImportCsv('data/output/conso_temp.csv', ';'),
          EnleveValMq([None, 'mq']),
          SelectionObservations(['Region'], ['='], ['Bretagne'], ['str']),
          Normalisation(['t', 'consommation_brute_electricite_rte']),
          MoyenneGlissante('t', 21, 'date'),
          MoyenneGlissante('consommation_brute_electricite_rte', 21, 'date'),
          ExportCsv(filename="conso_temp_bretagne.csv")]).run()

#### EXEMPLE 2 : RELATION ENTRE VENT ET CONSO ELEC ####
# Le vent joue-t-il un rôle dans cette consommation?

# Jeu de données sur le vent et jointure avec la consommation électrique (région et date)
Pipeline([ImportCsvGz('data/input/synop.202201.csv.gz', ';'),
          SelectionVariables(['numer_sta', 'date', 'ff']),
          EnleveValMq([None, 'mq']),
          FormaterDate('date', '%Y%m%d%H%M%S'),
          AgregationSpatiale('data/synop/postesSynopAvecRegions.csv',
                             'ID', 'numer_sta', 'Region', groupby=['date']),
          Jointure(ImportCsvGz('data/output/conso_elec.csv.gz', ';').importe(),
                   ['Region', 'date'], ['region', 'date_heure']),
          ExportCsv(filename="conso_vent.csv")]).run()

########## GRAPHIQUES ##########
lplot = LinePlot()
conso_temp = ImportCsv('data/output/conso_temp.csv', ';').importe()

#### GRAPHIQUE : PLOT DE LA CONSO ELEC SELON LA TEMPERATURE ####
lplot.plot(conso_temp, 't', 'consommation_brute_electricite_rte', 'Region')

#### GRAPHIQUE : PLOT DE LA SERIE TEMPORELLE DE LA CONSO ELEC SELON REGIONS ####
lplot.serie_temp(conso_temp, 'date',
                 'consommation_brute_electricite_rte', 'Region')

#### GRAPHIQUE : PLOT DES SERIES TEMPORELLES DE TEMPERATURE ET DE CONSO ELEC ####
conso_temp_bretagne = ImportCsv(
    'data/output/conso_temp_bretagne.csv', ';').importe()
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['moygli_t', 'moygli_consommation_brute_electricite_rte'])
