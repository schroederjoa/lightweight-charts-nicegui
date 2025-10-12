# -*- coding: utf-8 -*-

import asyncio

from lwchart import LwChart, createTextWatermark
#import test_nice_ui_components as uic
import pandas as pd
from nicegui import app, ui
#import webview
#from multiprocessing import Process, Queue
#from nicegui.events import KeyEventArguments

#import signal
#import time
 
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
			'borderColor': 'gray',#'#5eff33',
		},
		'timeScale': {
			'borderColor': 'gray',#'#71649C',
			'barSpacing': 12,
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

df = pd.read_csv("OHLC_Test_Minute_Data.csv")
df['time'] = df['date'].values.astype('datetime64[s]').astype('int64')
data = df.to_dict('records')

chart = None
candlestick_series = None
volume_series = None

def candlestick_apply_options():
	candlestick_series.applyOptions({
		 'upColor': 'red',
		 'downColor': 'blue',
	})
			
async def update():
	global data, candlestick_series, volume_series
	
	for d in data[0:50]:
		#print(d)
		candlestick_series.update(d)
		volume_series.update({'time':d['time'], 'value': d['volume']})
		
		await asyncio.sleep(0.05)
		
	data = data[50:]

async def on_click(e):
	global candlestick_series
	
	if 'point' not in e.args: return
	
	print("click params", e)
	
	price = await candlestick_series.coordinateToPrice(e.args['point']['y'])

	print("You clicked candle (time, price)", e.args['time'], price)

def add_watermark(text):
	
	global chart

	#panes = await chart.panes()
	
	#print(panes)
	
	chart.setTextWatermark({
	    'horzAlign': 'center',
	    'vertAlign': 'center',
	    'lines': [
	        {
	            'text': text,
	            'color': 'rgba(171, 71, 188, 0.5)',
	            'fontSize': 24,
	        },
	    ],
	}
		
		)
	
	'''
	chart.createTextWatermark(0, {
	    'horzAlign': 'center',
	    'vertAlign': 'center',
	    'lines': [
	        {
	            'text': text,
	            'color': 'rgba(171, 71, 188, 0.5)',
	            'fontSize': 24,
	        },
	    ],
	})	
	'''

@ui.page('/', title='Chart page')
async def page():
	
	global chart, data, candlestick_series, volume_series
			
	# expand column to full page height
	ui.query('.nicegui-content').classes('absolute-full')	
	
	with ui.column().classes('w-full h-full gap-1'):				
		
		chart = LwChart(chart_options, on_click=on_click).classes('w-full h-full min-w-[200px] min-h-[200px]')

		ui.button('run update', on_click=update)
		ui.button('series: applyOptions', on_click=candlestick_apply_options)
		ui.button('add watermark', on_click=lambda: add_watermark('Watermark Example'))
		ui.button('remove watermark', on_click=lambda: add_watermark(''))
		ui.button('fit content', on_click=chart.fitContent)
		
		ui.button('shutdown', on_click=app.shutdown)	
	
	candlestick_series = await chart.addSeries('CandlestickSeries', candlestick_series_options)
	candlestick_series.setData(data[0:100])

	volume_series = await chart.addSeries('HistogramSeries',
		{
			'priceFormat': {
				'type': 'volume',
			},
			'priceScaleId': "",
		},
		
	)
	volume_series.setData([{'time':d['time'], 'value': d['volume']} for d in data[0:100]])

	volume_series.priceScale().applyOptions({
		'scaleMargins': {
			'top': 0.7, # highest point of the series will be 70% away from the top
			'bottom': 0,
		},
	})
			
	data = data[100:]
				

ui.run(native=True, reload=False, dark=True)
