function getResources(path, dataset, callback) {
  var request = $.ajax(path);
  request.done(function(data) {
    dataset = dataset.concat(data.objects);
    if (data.meta.next) {
      getResources(data.meta.next, dataset, callback);
    } else {
      callback(dataset);
    }
  })
}

function loadUserTable(data) {
  $('#user-table').DataTable( {
    "initComplete": function (settings, json) {
      hideLoading(this);
    },
    "pagingType": "full_numbers",
    "language": {
      "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json"
    },
    data: data,
    columns: [
      { data: 'username' },
      { data: 'bill_participations' },
      { data: 'votes_count' },
      { data: 'comments_count' },
      { data: 'additive_count' },
      { data: 'modifier_count' },
      { data: 'supress_count' },
    ],
    dom: 'Bfrtip',
    buttons: [
      {
        extend: 'colvis',
        text: 'Mostrar/esconder colunas'
      },
      'csv',
      'excel'
    ]
  });
}

function loadBillTable(data) {
  $('#bill-table').DataTable( {
    "initComplete": function (settings, json) {
      hideLoading(this);
    },
    "pagingType": "full_numbers",
    "language": {
      "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json"
    },
    data: data,
    columns: [
      { data: 'title' },
      { data: 'participants_count' },
      { data: 'votes_count' },
      { data: 'comments_count' },
      { data: 'amendments_count' },
      { data: 'additive_amendments_count' },
      { data: 'modifier_amendments_count' },
      { data: 'supress_amendments_count' },
    ],
    dom: 'Bfrtip',
    buttons: [
      {
        extend: 'colvis',
        text: 'Mostrar/esconder colunas'
      },
      'csv',
      'excel'
    ]
  });
}

function usersUrlParams() {
  var url= new URL(location);
  var params = {}

  if (url.searchParams.has('startDate')) {
    params['date_joined__gte'] = startPicker.toString('YYYY-MM-DD');
  }

  if (url.searchParams.has('endDate')) {
    params['date_joined__lte'] = endPicker.toString('YYYY-MM-DD');
  }

  return $.param(params);
}

function billsUrlParams() {
  var url= new URL(location);
  var params = {}

  if (url.searchParams.has('startDate')) {
    params['created__gte'] = startPicker.toString('YYYY-MM-DD');
  }

  if (url.searchParams.has('endDate')) {
    params['created__lte'] = endPicker.toString('YYYY-MM-DD');
  }

  return $.param(params);
}

getResources('/wikilegis/api/v1/user/?' + usersUrlParams(), [], loadUserTable);
getResources('/wikilegis/api/v1/bill/?' + billsUrlParams(), [], loadBillTable);
