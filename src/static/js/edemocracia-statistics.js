function getResources(path, dataset, callback) {
  var url = path.replace('http://', 'https://')
  var request = $.ajax(url);
  request.done(function (data) {
    dataset = dataset.concat(data.results);
    if (data.next) {
      getResources(data.next, dataset, callback);
    } else {
      callback(dataset);
    }
  })
}

function loadUserTable(data) {
  $('#users-table').DataTable({
    "initComplete": function (settings, json) {
      var dataTables = $(this).parent().parent();
      hideLoading(dataTables);
    },
    "pagingType": "full_numbers",
    "scrollX": true,
    "language": {
      "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json"
    },
    dom: 'Bfrtip',
    buttons: [{
        extend: 'colvis',
        collectionLayout: 'fixed three-column',
        text: 'Mostrar/esconder colunas'
      },
      'csv',
      'excel'
    ],
    data: data,
    "columns": [{
        "data": "id",
        "bVisible": false
      },
      {
        "data": "username"
      },
      {
        "data": "first_name",
      },
      {
        "data": "last_name",
      },
      {
        "data": "last_login",
        "bVisible": false,
        "render": function (data, type, full) {
          if (data == null)
            return '';
          else
            if (type == 'display')
              return moment(new Date(data)).locale('pt').format('DD/MM/YYYY HH:mm');
            else
              return moment(new Date(data)).format('YYYY/MM/DD HH:mm:ss');
        }
      },
      {
        "data": "date_joined",
        "bVisible": false,
        "render": function (data, type, full) {
          if (data == null)
            return '';
          else
            if (type == 'display')
              return moment(new Date(data)).locale('pt').format('DD/MM/YYYY HH:mm');
            else
              return moment(new Date(data)).format('YYYY/MM/DD HH:mm:ss');
        }
      },
      {
        "data": "profile.gender"
      },
      {
        "data": "profile.uf"
      },
      {
        "data": "profile.birthdate",
        "bVisible": false,
        "render": function (data, type, full) {
         if (data == null)
           return '';
         else
          if (type == 'display')
            return moment(new Date(data)).locale('pt').format('DD/MM/YYYY');
          else
            return moment(new Date(data)).format('YYYY/MM/DD');
        }
      }
    ]
  });
};

function usersUrlParams() {
  var url = new URL(location);
  var params = {}

  if (url.searchParams.has('startDate')) {
    params['date_joined__gte'] = startPicker.toString('YYYY-MM-DD');
  }

  if (url.searchParams.has('endDate')) {
    params['date_joined__lte'] = endPicker.toString('YYYY-MM-DD');
  }

  return $.param(params);
}

getResources('/api/v1/user/?' + usersUrlParams(), [], loadUserTable);

$('.JS-toggleStatisticsLinks').click(function(){
  $(this).toggleClass('-active');
  $('.JS-statisticsLinks').toggleClass('-active');

  if ($('.JS-toggleStatisticsLinks').hasClass('-active')) {
    $(this).text('Fechar');
  } else {
    $(this).text('Menu');
  }
})
