# -*- coding: utf-8 -*-

import asyncio

from lwchart import LwChart
from lwchart_definitions import CrosshairMode, LineStyle, MismatchDirection

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
			'vertLines': { 'color': '#808080', 'style': LineStyle.Dotted },
			'horzLines': { 'color': '#808080', 'style': LineStyle.Dotted },
		},
		'crosshair': {
			'mode': CrosshairMode.Normal,
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
			'barSpacing': 6,
			'rightOffset': 10,
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
	
	print("click params", e)

	if e.args['paneIndex'] == 0:	
		value = await candlestick_series.coordinateToPrice(e.args['point']['y'])

	elif e.args['paneIndex'] == 1:	
		value = await rsi_series.coordinateToPrice(e.args['point']['y'])
		
	else:
		return
	
	if 'time' in e.args.keys():	
		print("You clicked candle (time, value)", e.args['time'], value)
	else:
		print("You clicked value", value)


async def on_crosshairmove(e):
	global candlestick_series
		
	if 'logical' in e.args.keys():	
		print("Crosshair moving over logical index", e.args['logical'])

	# moving over pane 0 / cabdkestick series?
	pane_index = e.args.get('paneIndex', -1)
	if pane_index == 0:	
	
		if 'time' in e.args.keys():
			data = await candlestick_series.dataByIndex(e.args['logical'])
			print("Moving over OHLC", data)
		else:
			print("Moving outside of candle range")
	

async def on_dblclick(e):
	
	print("Double-Click", e)
	
async def getVisLogRange():
	global chart

	print(await chart.timeScale().getVisibleLogicalRange())


async def reset():			
	global chart, candlestick_series
			
	chart.timeScale().resetTimeScale()
	candlestick_series.priceScale().applyOptions({ 'autoScale':True})		


	
@ui.page('/', title='Chart page')
async def page():
	
	global chart, data, candlestick_series, volume_series, rsi_series
			
	# expand column to full page height
	ui.query('.nicegui-content').classes('absolute-full')	

	with ui.column().classes('w-full h-full gap-1'):				
		
		# '''on_crosshairmove=on_crosshairmove'''
		chart = LwChart(chart_options, on_click=on_click, on_dblclick=on_dblclick, on_crosshairmove_tschange=on_crosshairmove).classes('w-full h-full min-w-[200px] min-h-[200px]')
	
		watermark = await chart.createTextWatermark(0, watermark_options)

		with ui.grid(columns=4).classes('gap-1'):
	
			ui.button('run update', on_click=update)
			ui.button('apply Candlestick Colors', on_click=candlestick_apply_colors)
			ui.button('add Watermark', on_click=lambda: watermark.setText('Watermark Example'))
			ui.button('remove Watermark', on_click=lambda: watermark.setText(''))
			
			ui.button('fitContent', on_click=chart.timeScale().fitContent)
			ui.button('reset', on_click=reset)
			ui.button('scrollToPosition 20', on_click=lambda: chart.timeScale().scrollToPosition(20, False))
			ui.button('set VisLogRange 0-100', on_click=lambda: chart.timeScale().setVisibleLogicalRange({ 'from': 0, 'to': 100}))
			ui.button('get VisLogRange', on_click=getVisLogRange)
			
	
		ui.button('shutdown', on_click=app.shutdown, color='red')	
	
	candlestick_series = await chart.addSeries('CandlestickSeries', candlestick_series_options)

	candlestick_series.priceScale().applyOptions({
		'autoScale': True,
		'scaleMargins': {
			'top': 0.1,
			'bottom': 0.2,
		},
	})
	
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
	rsi_series.setData([{'time':d['time'], 'value': d['rsi']} for d in data[0:100] if d['rsi'] != '' ])
					
	data = data[100:]
				

ui.run(native=True, reload=False, dark=True)
