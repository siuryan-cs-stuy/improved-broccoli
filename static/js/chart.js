var ctx;

$(document).ready(
  function() {
    ctx = document.getElementById("myChart").getContext('2d');

    var myDoughnutChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: chartConfig.degrees_data,
          backgroundColor: generateColors(chartConfig.degrees_data.length, 0.2),
            //'rgba(255, 99, 132, 0.2)',
            //'rgba(255, 206, 86, 0.2)',
            //'rgba(54, 162, 235, 0.2)'
          borderColor: generateColors(chartConfig.degrees_data.length, 1)
            //'rgba(255, 99, 132, 1)',
            //'rgba(255, 206, 86, 1)',
            //'rgba(54, 162, 235, 1)'
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: chartConfig.degrees_labels
      },
      options: {}
    });
  }
)

function generateColors(num, a) {
  // random starting values
  return generateRGBColors(num, 255, 99, 132, a);
}

function generateRGBColors(num, r, g, b, a) {
  var colors = [];
  for (i = 0; i < num; i++) {
    var string = "rgba(" + r + ", " + g + ", " + b + ", " + a + ")";
    colors.push(string);
    b = (b + 73) % 255;
    g = (g + 221) % 255;
    r = (r + 37) % 255;
  }
  return colors;
}

console.log(generateColors(chartConfig.degrees_data.length, 0.2));
console.log(generateColors(chartConfig.degrees_data.length, 1));
