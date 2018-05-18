var color = Chart.helpers.color;

var MyChart = {
	xyChartData: {
		datasets: [{
			label: 'Данные',
			xAxisID: 'x-axis-1',
			yAxisID: 'y-axis-1',
			//borderColor: [],
			//backgroundColor: [],
			pointBackgroundColor: [],
			data: []
		}]
	},
	draw: function() {
		//ChartCanvas
		MyChart.xyChartData.datasets[0].data = [];
		for(var i = 0; i < Data.xyDots.length; i++) {
			MyChart.xyChartData.datasets[0].data.push({x: Data.xyDots[i][0], y: Data.xyDots[i][1]});
			MyChart.xyChartData.datasets[0].pointBackgroundColor.push(Data.colors[Data.another[i]]);
		}
		var ctx = document.getElementById('ChartCanvas').getContext('2d');
		window.myScatter = Chart.Scatter(ctx, {
			data: MyChart.xyChartData,
			options: {
				
				responsive: true,
				title: {
		            display: true,
		            text: ''
		        },
		        legend: {
		            display: false,
		            labels: {
		                boxWidth: 16
		            }
		        },
		        layout: {
		            padding: {
		                left: 0,
		                right: 0,
		                top: -43,
		                bottom: 0
		            }
		        },
				scales: {
					xAxes: [{
						position: 'bottom',
						gridLines: {
							zeroLineColor: 'rgba(0,0,0,1)'
						}
					}],
					yAxes: [{
						type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
						display: true,
						position: 'left',
						id: 'y-axis-1',
					}, {
						type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
						display: true,
						position: 'right',
						reverse: true,
						id: 'y-axis-2',

						// grid line settings
						gridLines: {
							drawOnChartArea: false, // only want the grid lines for one axis to show up
						},
					}],
				}
			}
		});
	}
}