var ctx;

$(document).ready(
  function() {
    ctx = document.getElementById("myChart").getContext('2d');

    var myDoughnutChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: chartConfig.degrees_data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(54, 162, 235, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(54, 162, 235, 1)'
          ],
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: chartConfig.degrees_labels
      },
      options: {}
    });
  }
)
