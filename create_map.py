#import libraries
import os, sys
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
#In/Out variable
path = "D:\playground\map-dashboard"
file_basemap = os.path.join(path,"data\Carto-Voyager.xml")
file_csv = os.path.join(path,"data\earthquakes_2019.csv")
style_layer_gempa = os.path.join(path,"data\style_gempa.qml")
qpt_path = os.path.join(path,"img/report_template_A4.qpt")
output_pdf = os.path.join(path,"report/report_A4.pdf")
csv_filtered = os.path.join(path,"data\earthquakes_filtered.csv")
#CRS definition
wgs84 = QgsCoordinateReferenceSystem(4326)
#Create Pandas DataFrame for statistics
start_date = '2019-01-01'
end_date ='2019-09-30'
df = pd.read_csv(file_csv,sep=',')
df['datetime'] = pd.to_datetime(df['time'], format='%Y-%m-%dT%H:%M:%S.%fZ') #convert string as datetime format
mask_date = (df['datetime'] >= start_date) & (df['datetime'] <= end_date) #filter datetime
df_filtered = df.loc[mask_date]
df_filtered.to_csv(csv_filtered, index=False)
#stats summary
max_mag = df_filtered['mag'].max()
max_depth = df_filtered['depth'].max()
min_depth = df_filtered['depth'].min()
avg_depth = df_filtered['depth'].mean()
count_eq = len(df_filtered.index)

#Add layer to canvas
layer_basemap = iface.addRasterLayer(file_basemap, "", "gdal")
layer_gempa = iface.addVectorLayer(csv_filtered, "csv", "ogr")
layer_gempa.setCrs(wgs84, True)

#apply style to layer gempa
layer_gempa.loadNamedStyle(style_layer_gempa)
layer_gempa.triggerRepaint()



#{Pivot dataframe for chart
df_filtered['month'] = df_filtered['datetime'].dt.strftime('%Y-%m') #add column month
dfEq = pd.pivot_table(df_filtered, index=['month'], values=["mag"], aggfunc='count',fill_value=0) #number of eq per month
plt.bar(dfEq.index, dfEq['mag'], label = 'Count', color='#22e4de')
#remove lines axes and box
plt.box(False)
#plt.grid(axis='y')
fig = plt.gcf()
#save chart to image file
chart_count_mag = os.path.join(path,"img/chart_count_mag.jpg")
fig.set_size_inches(12, 1.7)
fig.savefig(chart_count_mag, dpi=300, bbox_inches = "tight", facecolor='#f4f4f4')
plt.close(fig)

color = [str(item/255.) for item in df_filtered['depth']]
area = [2**n for n in df_filtered['mag'] ]
plt.scatter(df_filtered['datetime'], df_filtered['depth'], s=area, c=color, alpha=3/4)
#remove lines axes and box
plt.box(False)
plt.grid(axis='y')
fig = plt.gcf()
plt.gca().invert_yaxis()

#save chart to image file
fig.set_size_inches(12, 1.7)
chart_avg_depth = os.path.join(path,'img/chart_avg_depth.jpg')
fig.savefig(chart_avg_depth, dpi=300, bbox_inches = "tight", facecolor='#f4f4f4')
plt.close(fig)

###LAYOUT COMPOSING
document = QDomDocument()
project = QgsProject.instance()
composition = QgsPrintLayout(project)

layout = QgsLayout(project)
layout.initializeDefaults()
# read template content
template_file = open(qpt_path)
template_content = template_file.read()
template_file.close()
document.setContent(template_content)

# load layout from template and add to Layout Manager
composition.loadFromTemplate(document, QgsReadWriteContext())
project.layoutManager().addLayout(composition)
layout = project.layoutManager().layoutByName("Report A4")
#add map to layout
map = QgsLayoutItemMap(layout)
map.setRect(20, 20, 20, 20)

#get extent from layer gempa
ext = layer_gempa.extent()
map.setExtent(ext)
layout.addLayoutItem(map)
map.setFrameStrokeWidth(QgsLayoutMeasurement(0.2,QgsUnitTypes.LayoutMillimeters))
map.attemptMove(QgsLayoutPoint(9.275, 22, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(191.118, 88, QgsUnitTypes.LayoutMillimeters))
scale = map.scale()

# call functions in utils
sys.path.append(path)
from utils import *

# add label max_mag, avg_depth, count_eq
addLabel(layout, str(max_mag), 'Arial', 36, QFont.Bold, False, '#21908d', 0,0, 28.852, 125) #Magnitude  label
addLabel(layout, str(round(avg_depth,2)), 'Arial', 36, QFont.Bold, False, '#21908d', 0,0, 93, 125) #Depth  label
addLabel(layout, str(count_eq), 'Arial', 36, QFont.Bold, False, '#21908d', 0,0, 156, 125) #Magnitude  label

# add chart 1
addImage(layout,chart_count_mag,10, 175, 190, 34) #chart1: donut chart dumping point
addImage(layout,chart_avg_depth,10, 237, 190, 34) #chart1: donut chart dumping point

# export layout to file 
# creats a QgsLayoutExporter object
exporter = QgsLayoutExporter(layout)
settings = exporter.PdfExportSettings()
#this exports a pdf of the layout object
exporter.exportToPdf(output_pdf, settings)
#exporter.exportToImage('D:/playground/map-dashboard/report/report_A4.png', QgsLayoutExporter.ImageExportSettings())

