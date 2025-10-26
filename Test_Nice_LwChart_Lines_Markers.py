# -*- coding: utf-8 -*-

import asyncio

from lwchart import LwChart
import pandas as pd
from nicegui import app, ui
import random
 
chart_options = {
	'TimeChartOptions' : {
		'autoSize': True,
		'layout': {
			'background': { 'color': '#000000' },
			'textColor': '#DDD',
			'fontSize': 12,
			'attributionLogo': False,
			'panes': {
				'separatorColor': '#808080',
				'separatorHoverColor': '#808080',
				'enableResize': False,
			},
		},
		'grid': {
			'vertLines': { 'color': '#808080', 'style': 1},
			'horzLines': { 'color': '#808080', 'style': 1 },
		},
		'crosshair': {
			'mode': 0, # normal mode
			'vertLine': {
				'labelBackgroundColor': '#9B7DFF',
			},
			'horzLine': {
				'labelBackgroundColor': '#9B7DFF',
			},
		},
		'rightPriceScale': {
			'visible': True,
			'borderColor': 'gray',
		},
		'timeScale': {
			'borderColor': 'gray',
			'barSpacing': 10,
			'timeVisible': True,
			'visible': True,					
		},				
	}		
}

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

rsi_series_options = { 
	'color': 'rgba(255,191,0, 1)',
	'lineStyle': 0, 
	'lineWidth': 1,
	'lastValueVisible': True
}

df = pd.read_csv("OHLC_Test_Minute_Data.csv")
df = df.fillna('')

df['time'] = df['date'].values.astype('datetime64[s]').astype('int64')
data = df.to_dict('records')

chart = None
candlestick_series = None
candlestick_series_markers = None
rsi_series = None
lines = []


async def add_line():
	global candlestick_series
	
	myPriceLine = {
	    'price': random.randint(17160, 17240)/100,
	    'color': '#3179F5',
	    'lineWidth': 2,
	    'lineStyle': 2, # LineStyle.Dashed
	    'axisLabelVisible': True,
	    'title': 'my label ' + str(len(lines)),
	};

	line = await candlestick_series.createPriceLine(myPriceLine)
	lines.append(line)

def remove_lines():
	global lines

	for l in lines:
		candlestick_series.removePriceLine(l)
	
	lines = []

async def set_markers():
	
	rsi_data = await rsi_series.data()
	
	marker_options = {
		 'color': 'yellow',
		 'position': 'belowBar',
		 'shape': 'arrowUp',		 
	}
	
	markers = [{**marker_options, **{'time':r['time'], 'text':f'rsi is {r['value']:.1f}'}} for r in rsi_data if r['value'] < 30]

	candlestick_series_markers.setMarkers(markers)
	
def remove_markers():

	candlestick_series_markers.setMarkers([])
	
		
@ui.page('/', title='Chart page')
async def page():
	
	global chart, data, candlestick_series, rsi_series, candlestick_series_markers
			
	# expand column to full page height
	ui.query('.nicegui-content').classes('absolute-full')	
	
	with ui.column().classes('w-full h-full gap-1'):				
		
		chart = LwChart(chart_options).classes('w-full h-full min-w-[200px] min-h-[200px]')
	
		with ui.button_group().classes('gap-1'):
	
			ui.button('add line', on_click=add_line)
			ui.button('remove lines', on_click=remove_lines)

			ui.button('set markers', on_click=set_markers)
			ui.button('remove markers', on_click=remove_markers)

		
		ui.button('shutdown', on_click=app.shutdown, color='red')	
	
	candlestick_series = await chart.addSeries('CandlestickSeries', candlestick_series_options)

	candlestick_series_markers = await chart.createSeriesMarkers(candlestick_series, [])

	rsi_series = await chart.addSeries('LineSeries', rsi_series_options, 1)
	
	panes = await chart.panes()
	panes[0].setStretchFactor(0.8);
	panes[1].setStretchFactor(0.2);
	
	candlestick_series.setData(data[0:100])
	rsi_series.setData([{'time':d['time'], 'value': d['rsi']} for d in data[0:100] if d['rsi'] != '' ])

							

ui.run(native=True, reload=False, dark=True)
