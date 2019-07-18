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
