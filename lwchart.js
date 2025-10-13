
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
	
	this.chart.subscribeClick(param => {		
		
		delete param.seriesData;
		delete param.hoveredObjectId;
		delete param.hoveredSeries;

		this.$emit("click", param);
	});			
    
	},
	methods: {

	addSeries(series_type, series_options, pane_index) {
	
		const series_id = Object.keys(this.series).length
		
		console.debug("adding series with type/id", series_type, series_id)
		
  	 	this.series[series_id] = this.chart.addSeries(LightweightCharts[series_type], series_options, pane_index);
		return series_id;
	},
	createTextWatermark(pane_index, options) {
	
		const watermark_id = Object.keys(this.watermarks).length
		
		this.watermarks[watermark_id] = LightweightCharts.createTextWatermark(this.chart.panes()[pane_index], options)	
		return watermark_id;
	},
	getPanes() {
		return this.chart.panes().length;
	},
	setTextWatermark(options) {
		this.text_watermark.applyOptions( options );
	},
    clear() {
    },
  },
};
