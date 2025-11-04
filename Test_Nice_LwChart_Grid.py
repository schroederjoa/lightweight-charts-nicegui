# -*- coding: utf-8 -*-

import asyncio
from lwchart import LwChart
from lwchart_definitions import CrosshairMode, LineStyle, MismatchDirection

from nicegui import app, ui
 
chart_options = {
	'TimeChartOptions' : {
		'autoSize': True,
		'layout': {
			'attributionLogo': False,
		},				
	}		
}

cs_data = [
    { 'time': '2018-12-22', 'open': 75.16, 'high': 82.84, 'low': 36.16, 'close': 45.72 },
    { 'time': '2018-12-23', 'open': 45.12, 'high': 53.90, 'low': 45.12, 'close': 48.09 },
    { 'time': '2018-12-24', 'open': 60.71, 'high': 60.71, 'low': 53.39, 'close': 59.29 },
    { 'time': '2018-12-25', 'open': 68.26, 'high': 68.26, 'low': 59.04, 'close': 60.50 },
    { 'time': '2018-12-26', 'open': 67.71, 'high': 105.85, 'low': 66.67, 'close': 91.04 },
    { 'time': '2018-12-27', 'open': 91.04, 'high': 121.40, 'low': 82.70, 'close': 111.40 },
    { 'time': '2018-12-28', 'open': 111.51, 'high': 142.83, 'low': 103.34, 'close': 131.25 },
    { 'time': '2018-12-29', 'open': 131.33, 'high': 151.17, 'low': 77.68, 'close': 96.43 },
    { 'time': '2018-12-30', 'open': 106.33, 'high': 110.20, 'low': 90.39, 'close': 98.10 },
    { 'time': '2018-12-31', 'open': 109.87, 'high': 114.69, 'low': 85.66, 'close': 111.26 },
]

candlestick_series_options = {
	'priceScaleId': 'right', 
	'upColor': '#5aaf55',
	'downColor': '#cb2d2e',
	'borderUpColor': '#5aaf55',
	'borderDownColor': '#cb2d2e',			
	'wickUpColor': '#5aaf55',
	'wickDownColor': '#cb2d2e',	
	'priceLineVisible': True,
	'lastValueVisible': True,			
}
	
@ui.page('/', title='Chart page')
async def page():
				
	# expand column to full page height
	ui.query('.nicegui-content').classes('absolute-full')

	num_charts = 6
	
	
	######################################################################################
	# this sets the chart height correctly and stretches + shrinks
	######################################################################################
	
	with ui.grid(columns=3).classes('w-full h-full gap-1'):

		for i in range(num_charts):
			
			chart = LwChart(chart_options).classes('w-full h-full min-w-[200px] min-h-[200px]')
			
			candlestick_series = await chart.addSeries('CandlestickSeries', {})
			candlestick_series.setData(cs_data)
	
	'''
	######################################################################################
	# this stretches, but does not shrink the chart height anymore
	######################################################################################
	
	with ui.grid(columns=3).classes('w-full h-full gap-1'):

		for i in range(num_charts):
			
			with ui.column().classes('w-full h-full gap-1'):
				ui.label("Placeholder for control element")
				chart = LwChart(chart_options).classes('w-full h-full min-w-[200px] min-h-[200px]')
			
			candlestick_series = await chart.addSeries('CandlestickSeries', candlestick_series_options)
			candlestick_series.setData(cs_data)
	'''	
								
ui.run(native=True)
