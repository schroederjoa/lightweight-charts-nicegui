from typing import Dict, Optional

from nicegui import ui, app
#import pandas as pd
#from pathlib import Path
from typing import Callable#, Optional

app.add_static_files('/node_modules', './node_modules')

	
def createTextWatermark(pane, options):
	print("creating", pane.chart.id, pane.pane_index)
	ui.run_javascript(f'LightweightCharts.createTextWatermark(getElement({pane.chart.id}).chart.panes()[{pane.pane_index}], {options})')	


class Pane:
	
	def __init__(self, chart, pane_index):
		self.chart = chart
		self.pane_index=pane_index
	
class PriceScale:
	
	def __init__(self, series):
		self.series = series

	def applyOptions(self, options):

		ui.run_javascript(f'getElement({self.series.chart.id}).series[{self.series.series_id}].priceScale().applyOptions({options})')
		
class Series:

	def __init__(self, chart, series_id):

		self.chart = chart
		self.series_id = series_id


	def applyOptions(self, options):

		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].applyOptions({options})')
		
	async def coordinateToPrice(self, coordinate):

		return await ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].coordinateToPrice({coordinate})')
		

	def moveToPane(self, index):

		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].moveToPane({index})')		

	def priceScale(self):
		
		return PriceScale(self)


	def setData(self, data):

		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].setData({data})')		


	def update(self, data):
		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].update({data})')		

		

class LwChart(ui.element,
                   component='lwchart.js',
                   dependencies=['node_modules/lightweight-charts/dist/lightweight-charts.standalone.production.js',
											#'node_modules/moment/dist/moment.js',
											#'node_modules/moment-timezone/builds/moment-timezone-with-data.js',
											]):

	def __init__(self, options: Optional[Dict] = None, on_click: Optional[Callable] = None) -> None:
		"""SignaturePad

		An element that integrates the lightweight-charts library.
		https://github.com/tradingview/lightweight-charts
		"""
		super().__init__()
		#self._props['options'] = options or {}
		
		#print(self.__dict__)
		
		#print(options)
		ui.add_head_html('<script src="/node_modules/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>')
		#ui.add_head_html('<script src="/node_modules/moment/dict/moment.js"></script>')
		#ui.add_head_html('<script src="/node_modules/moment-timezone/builds/moment-timezone-with-data.js"></script>')
		#ui.add_head_html('<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>')
		#print("add ok")
		
		self._props['options'] = options
		self.on('click', on_click)

	async def addSeries(self, series_type, series_options, pane_index = 0):

		series_id = await self.run_method('addSeries', series_type, series_options, pane_index)	
		return Series(self, series_id)		
	

	def fitContent(self):
		ui.run_javascript(f'getElement({self.id}).chart.timeScale().fitContent();')		
		
	async def panes(self):
		num_panes = await self.run_method('getPanes')	
		return [Pane(self, i) for i in range(num_panes)]

	def setTextWatermark(self, options):
		self.run_method('setTextWatermark', options)	
		

	def createTextWatermark(self, pane_index, options):
		ui.run_javascript(f'LightweightCharts.createTextWatermark(getElement({self.id}).chart.panes()[{pane_index}], {options})')	
	
	

