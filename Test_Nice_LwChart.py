# -*- coding: utf-8 -*-

import asyncio

from lwchart import LwChart
import pandas as pd
from nicegui import app, ui
 
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


watermark_options = {
    'horzAlign': 'center',
    'vertAlign': 'center',
    'lines': [
        {
            'text': '',
            'color': 'rgba(171, 71, 188, 0.5)',
            'fontSize': 36,
        },
    ],
}

df = pd.read_csv("OHLC_Test_Minute_Data.csv")
df = df.fillna('')

df['time'] = df['date'].values.astype('datetime64[s]').astype('int64')
data = df.to_dict('records')

chart = None
candlestick_series = None
volume_series = None
rsi_series = None


def candlestick_apply_colors():
	candlestick_series.applyOptions({
		 'upColor': 'red',
		 'downColor': 'blue',
	})
			
async def update():
	global data, candlestick_series, volume_series, rsi_series
	
	for d in data[0:50]:

		candlestick_series.update(d)
		volume_series.update({'time':d['time'], 'value': d['volume']})
		rsi_series.update({'time':d['time'], 'value': d['rsi']})
		
		await asyncio.sleep(0.05)
		
	data = data[50:]

async def on_click(e):
	global candlestick_series
	
	if 'point' not in e.args: return
	
	#print("click params", e)
	
	price = await candlestick_series.coordinateToPrice(e.args['point']['y'])

	if 'time' in e.args.keys():	
		print("You clicked candle (time, price)", e.args['time'], price)
	else:
		print("You clicked price", price)

@ui.page('/', title='Chart page')
async def page():
	
	global chart, data, candlestick_series, volume_series, rsi_series
			
	# expand column to full page height
	ui.query('.nicegui-content').classes('absolute-full')	
	
	with ui.column().classes('w-full h-full gap-1'):				
		
		chart = LwChart(chart_options, on_click=on_click).classes('w-full h-full min-w-[200px] min-h-[200px]')
	
		watermark = await chart.createTextWatermark(0, watermark_options)

		with ui.button_group().classes('gap-1'):
	
			ui.button('run update', on_click=update)
			ui.button('apply candlestick colors', on_click=candlestick_apply_colors)
			ui.button('add watermark', on_click=lambda: watermark.setText('Watermark Example'))
			ui.button('remove watermark', on_click=lambda: watermark.setText(''))
			ui.button('fit content', on_click=chart.fitContent)
		
		ui.button('shutdown', on_click=app.shutdown, color='red')	
	
	candlestick_series = await chart.addSeries('CandlestickSeries', candlestick_series_options)

	volume_series = await chart.addSeries('HistogramSeries',
		{
			'priceFormat': {
				'type': 'volume',
			},
			'priceScaleId': "",
		},
		
	)

	volume_series.priceScale().applyOptions({
		'scaleMargins': {
			'top': 0.7, # highest point of the series will be 70% away from the top
			'bottom': 0,
		},
	})

	rsi_series = await chart.addSeries('LineSeries', rsi_series_options, 1)
	
	panes = await chart.panes()
	panes[0].setStretchFactor(0.8);
	panes[1].setStretchFactor(0.2);
	#panes[1].setHeight(100)

	candlestick_series.setData(data[0:100])
	volume_series.setData([{'time':d['time'], 'value': d['volume']} for d in data[0:100]])
	rsi_series.setData([{'time':d['time'], 'value': d['rsi']} for d in data[0:100]])
				
	data = data[100:]
				

ui.run(native=True, reload=False, dark=True)
