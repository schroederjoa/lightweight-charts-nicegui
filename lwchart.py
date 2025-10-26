from typing import Dict, Optional

from nicegui import ui, app
from typing import Callable

app.add_static_files('/node_modules', './node_modules')

class Pane:
	
	def __init__(self, chart, pane_index):
		self.chart = chart
		self.pane_index = pane_index
		
	def setHeight(self, height):	
		ui.run_javascript(f'getElement({self.chart.id}).chart.panes()[{self.pane_index}].setHeight({height})')

	def setStretchFactor(self, factor):
		ui.run_javascript(f'getElement({self.chart.id}).chart.panes()[{self.pane_index}].setStretchFactor({factor})')

class PriceLine:

	def __init__(self, series, line_id):
		self.series = series		
		self.line_id = line_id
	
class PriceScale:
	
	def __init__(self, series):
		self.series = series

	def applyOptions(self, options):

		ui.run_javascript(f'getElement({self.series.chart.id}).series[{self.series.series_id}].priceScale().applyOptions({options})')


		
class Series:

	def __init__(self, chart, series_id, pane_index):

		self.chart = chart
		self.series_id = series_id
		self.pane_index = pane_index
		

	def applyOptions(self, options):

		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].applyOptions({options})')
		
	async def coordinateToPrice(self, coordinate):

		return await ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].coordinateToPrice({coordinate})')
	
	async def createPriceLine(self, line_options):
		
		#return await ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].createPriceLine({line_options})')

		line_id = await self.chart.run_method('createPriceLine', self.series_id, line_options)	
		return PriceLine(self, line_id)
		
	async def data(self):
		return await ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].data()')		
		
	def moveToPane(self, index):

		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].moveToPane({index})')		

	def priceScale(self):
		
		return PriceScale(self)

	def removePriceLine(self, line):
		self.chart.run_method('removePriceLine', self.series_id, line.line_id)	

	def setData(self, data):

		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].setData({data})')		


	def update(self, data):
		ui.run_javascript(f'getElement({self.chart.id}).series[{self.series_id}].update({data})')		

class SeriesMarkers:

	def __init__(self, chart, series_markers_id):

		self.chart = chart
		self.series_markers_id = series_markers_id

	def setMarkers(self, markers):
		ui.run_javascript(f'getElement({self.chart.id}).series_markers[{self.series_markers_id}].setMarkers({markers})')
		
		
		
class TextWatermark:

	def __init__(self, chart, watermark_id, options):

		self.chart = chart
		self.watermark_id = watermark_id
		self.options = options

	def applyOptions(self, options):

		self.options = options
		
		ui.run_javascript(f'getElement({self.chart.id}).watermarks[{self.watermark_id}].applyOptions({self.options})')
		
	def setText(self, text):
		if 'lines' not in self.options.keys(): return
		
		self.options['lines'][0]['text'] = text
		ui.run_javascript(f'getElement({self.chart.id}).watermarks[{self.watermark_id}].applyOptions({self.options})')
				

class LwChart(ui.element,
                   component='lwchart.js',
                   dependencies=['node_modules/lightweight-charts/dist/lightweight-charts.standalone.production.js',
											]):

	def __init__(self, options: Optional[Dict] = None, on_click: Optional[Callable] = None) -> None:
		"""
		An element that integrates the lightweight-charts library.
		https://github.com/tradingview/lightweight-charts
		"""
		super().__init__()

		ui.add_head_html('<script src="/node_modules/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>')
		
		self._props['options'] = options
		self.on('click', on_click)

	async def addSeries(self, series_type, series_options, pane_index = 0):

		series_id = await self.run_method('addSeries', series_type, series_options, pane_index)	
		return Series(self, series_id, pane_index)		
	
	def fitContent(self):
		ui.run_javascript(f'getElement({self.id}).chart.timeScale().fitContent();')		
		
	async def panes(self):
		num_panes = await self.run_method('getPanes')	
		return [Pane(self, i) for i in range(num_panes)]

	async def createSeriesMarkers(self, series, options):
		series_markers_id = await self.run_method('createSeriesMarkers', series.series_id, options)	
		return SeriesMarkers(self, series_markers_id)
		
	async def createTextWatermark(self, pane_index, options):
		watermark_id = await self.run_method('createTextWatermark', pane_index, options)	
		return TextWatermark(self, watermark_id, options)
	
	

