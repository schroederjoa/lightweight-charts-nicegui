
export default {
  template: `
	  <div>
	  </div>
  `,
  props: {
    //options: Array,
    options: Object,
  },
  mounted() {
	
	this.chart = LightweightCharts.createChart(this.$el, this.options.TimeChartOptions);
	this.text_watermark = LightweightCharts.createTextWatermark(this.chart.panes()[0], {});
	this.series = new Object();
	this.watermarks = new Object();
	this.price_lines = new Object();
	this.series_markers = new Object();
	
	this.crosshairmove_last_time = null;
	
	this.chart.subscribeClick(param => {		
		
		delete param.seriesData;
		delete param.hoveredObjectId;
		delete param.hoveredSeries;

		this.$emit("click", param);
	});			

	this.chart.subscribeDblClick(param => {		
		
		delete param.seriesData;
		delete param.hoveredObjectId;
		delete param.hoveredSeries;

		this.$emit("dblclick", param);
	});	
  
	this.chart.subscribeCrosshairMove(param => {		
		
		delete param.seriesData;
		delete param.hoveredObjectId;
		delete param.hoveredSeries;
		
		if (param.time != this.crosshairmove_last_time) {
			this.$emit("crosshairmove_tschange", param);
			this.crosshairmove_last_time = param.time;
		}

		this.$emit("crosshairmove", param);
	});	  
	},
	methods: {

	addSeries(series_type, series_options, pane_index) {
	
		const series_id = Object.keys(this.series).length
		
		console.debug("adding series with type/id", series_type, series_id)
		
  	 	this.series[series_id] = this.chart.addSeries(LightweightCharts[series_type], series_options, pane_index);
		return series_id;
	},
	applyOptionsPriceLine(line_id, options) {
		this.price_lines[line_id].applyOptions(options);
	},
	createPriceLine(series_id, line_options) {
		const line_id = Object.keys(this.price_lines).length

		this.price_lines[line_id] = this.series[series_id].createPriceLine(line_options)	
		return line_id;
			
	},
	createSeriesMarkers(series_id, options) {
	
		const series_markers_id = Object.keys(this.watermarks).length
		
		this.series_markers[series_markers_id] = LightweightCharts.createSeriesMarkers(this.series[series_id], options)	
		return series_markers_id;
	},	
	createTextWatermark(pane_index, options) {
	
		const watermark_id = Object.keys(this.watermarks).length
		
		this.watermarks[watermark_id] = LightweightCharts.createTextWatermark(this.chart.panes()[pane_index], options)	
		return watermark_id;
	},
	getPanes() {
		return this.chart.panes().length;
	},
	removePriceLine(series_id, line_id) {
	
		//console.log(this.price_lines)
		//console.log(line_id)
	
		this.series[series_id].removePriceLine(this.price_lines[line_id]);
		delete this.price_lines[line_id];
	},
	setTextWatermark(options) {
		this.text_watermark.applyOptions( options );
	},
    clear() {
    },
  },
};
