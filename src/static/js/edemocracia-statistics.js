$(document).ready(function() {
  var table = $('#data-tables').DataTable( {
    "pagingType": "full_numbers",
    "language": {
      "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json"
    },
    dom: 'Bfrtip',
    buttons: [
      'csv', 'excel'
    ]
  });

  $('a.toggle-vis').on( 'click', function (e) {
    e.preventDefault();

    // Get the column API object
    var column = table.column( $(this).attr('data-column') );

    // Toggle the visibility
    column.visible( ! column.visible() );
  });
});

var ctx = $('#myLineChart');
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
          'JAN',
          'FEV',
          'MAR',
          'ABR',
          'MAIO',
          'JUN',
          'JUL',
          'AGO',
          'SET',
          'OUT',
          'NOV',
          'DEZ'
        ],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
      legend: {
        position: 'bottom'
      },
      scales: {
          // xAxes: [{
          //     gridLines: {
          //         color: "rgba(0, 0, 0, 0)",
          //     }
          // }],
          yAxes: [{
              gridLines: {
                  color: "rgba(0, 0, 0, 0)",
              }
          }]
      },
    },
});

$('.JS-toggleStatisticsLinks').click(function(){
  $(this).toggleClass('-active');
  $('.JS-statisticsLinks').toggleClass('-active');

  if ($('.JS-toggleStatisticsLinks').hasClass('-active')) {
    $(this).text('Fechar');
  } else {
    $(this).text('Menu');
  }
})
