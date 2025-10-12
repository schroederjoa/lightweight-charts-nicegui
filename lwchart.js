
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

	console.log(this.options)
	
	this.chart = LightweightCharts.createChart(this.$el, this.options.TimeChartOptions);
	this.text_watermark = LightweightCharts.createTextWatermark(this.chart.panes()[0], {});
	this.series = new Object();
	
	this.chart.subscribeClick(param => {		

		/*if (!param.point) {
			return;
		}*/
		
		delete param.seriesData;
		delete param.hoveredObjectId;
		delete param.hoveredSeries;
		
		//param.value = this.series['main'].coordinateToPrice(param.point.y)
		
		//console.log(param.point)

		this.$emit("click", param);
	});			
    
  },
  methods: {

	addSeries(series_type, series_options) {
	
		const series_id = Object.keys(this.series).length
		
		console.debug("adding series with type/id", series_type, series_id)
		
  	 	this.series[series_id] = this.chart.addSeries(LightweightCharts[series_type], series_options);
		return series_id;
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
