"""
Démonstration du Pipeline

Soutenance du projet traitement de données
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
from pipelinepackage.plots.cartoplot import CartoPlot

# Y A-T-IL UNE RELATION ENTRE TEMPERATURE ET CONSOMMATION ELECTRIQUE ?

# Jeu de données de consommation électrique
Pipeline([ImportJsonGz('data/input/2022-01.json.gz'),
          SelectionVariables(
              ['region', 'date_heure', 'consommation_brute_electricite_rte']),
          EnleveValMq([None]),
          FormaterDate('date_heure', '%Y-%m-%dT%H:%M:%S%z'),
          ExportCsvGz(filename='conso_elec.csv.gz')]).run()

lplot = LinePlot()
conso_elec = ImportCsvGz('data/output/conso_elec.csv.gz', ';').importe()
lplot.serie_temp(conso_elec, 'date_heure',
                 'consommation_brute_electricite_rte')
lplot.serie_temp(conso_elec, 'date_heure',
                 'consommation_brute_electricite_rte', 'region')

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

conso_temp = ImportCsv('data/output/conso_temp.csv', ';').importe()
lplot.plot(conso_temp, 't', 'consommation_brute_electricite_rte')
lplot.plot(conso_temp, 't', 'consommation_brute_electricite_rte', 'Region')


# Jeu de données température/consommation électrique pour la Bretagne
Pipeline([ImportCsv('data/output/conso_temp.csv', ';'),
          EnleveValMq([None, 'mq']),
          SelectionObservations(['Region'], ['='], ['Bretagne'], ['str']),
          MoyenneGlissante('t', 21, 'date'),
          MoyenneGlissante('consommation_brute_electricite_rte', 21, 'date'),
          ExportCsv(filename="conso_temp_bretagne.csv")]).run()

conso_temp_bretagne = ImportCsv(
    'data/output/conso_temp_bretagne.csv', ';').importe()
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['consommation_brute_electricite_rte', 'moygli_consommation_brute_electricite_rte'])
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['t', 'moygli_t'])
lplot.plot(conso_temp_bretagne, 'moygli_t', 'moygli_consommation_brute_electricite_rte')
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['moygli_t', 'moygli_consommation_brute_electricite_rte'])

# Jeu de données température/consommation électrique pour la Bretagne
Pipeline([ImportCsv('data/output/conso_temp.csv', ';'),
          EnleveValMq([None, 'mq']),
          SelectionObservations(['Region'], ['='], ['Bretagne'], ['str']),
          Normalisation(['t', 'consommation_brute_electricite_rte']),
          MoyenneGlissante('t', 21, 'date'),
          MoyenneGlissante('consommation_brute_electricite_rte', 21, 'date'),
          ExportCsv(filename="conso_temp_bretagne.csv")]).run()

conso_temp_bretagne = ImportCsv(
    'data/output/conso_temp_bretagne.csv', ';').importe()
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['consommation_brute_electricite_rte', 'moygli_consommation_brute_electricite_rte'])
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['t', 'moygli_t'])
lplot.series_temps(conso_temp_bretagne, 'date',
                   ['moygli_t', 'moygli_consommation_brute_electricite_rte'])

#### CARTE DE LA TEMPERATURE MOYENNE PAR REGION ####
Pipeline([ImportCsvGz('data/input/synop.202201.csv.gz', ';'),
          SelectionVariables(['numer_sta', 't']),
          EnleveValMq([None, 'mq']),
          AgregationSpatiale('data/synop/postesSynopAvecRegions.csv',
                             'ID', 'numer_sta', 'Region'),
          ExportCsv(filename="temp_reg.csv")]).run()

table = ImportCsv('data/output/temp_reg.csv', ';').importe()
cp = CartoPlot(colormap='coolwarm')
fig = cp.plot_reg_map(data={row['Region']: float(row['t'])-273.15 for row in table.body},
                      d_lim=(0, 10), x_lim=(-6, 10), y_lim=(41, 52), figsize=(13, 11))
fig.show()
fig.savefig('data/output/temp_reg.jpg')
