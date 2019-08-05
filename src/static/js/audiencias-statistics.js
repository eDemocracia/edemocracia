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
        buttons: [
            {
                extend: 'colvis',
                collectionLayout: 'fixed three-column',
                text: 'Mostrar/esconder colunas'
            },
            'csv',
            'excel'
        ],
        data: data,
        "columns": [
            {
                "data": "id",
                "bVisible": false
            },
            {
                "data": "username"
            },
            {
                "data": "first_name",
                "bVisible": false
            },
            {
                "data": "last_name",
                "bVisible": false
            },
            {
                "data": "questions_count"
            },
            {
                "data": "messages_count"
            },
            {
                "data": "votes_count"
            },
            {
                "data": "participations_count"
            },
            {
                "data": "questions_votes_count"
            }
        ]
    });
};

function loadRoomTable(data) {
    $('#rooms-table').DataTable({
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
        buttons: [
            {
                extend: 'colvis',
                collectionLayout: 'fixed three-column',
                text: 'Mostrar/esconder colunas'
            },
            'csv',
            'excel'
        ],
        data: data,
        "columns": [
            {
                "data": "id",
                "bVisible": false
            },
            {
                "data": "cod_reunion",
                "bVisible": false
            },
            {
                "data": "legislative_body",
                "bVisible": false
            },
            {
                "data": "legislative_body_initials",
            },
            {
                "data": "reunion_type",
                "bVisible": false
            },
            {
                "data": "title_reunion",
                "bVisible": false
            },
            {
                "data": "reunion_object",
                "bVisible": false
            },
            {
                "data": "reunion_theme",
            },
            {
                "data": "location",
                "bVisible": false
            },
            {
                "data": "created",
                "bVisible": false,
                "render": function (data, type, full) {
                    if (type == 'display')
                        return moment(new Date(data)).locale('pt').format('DD/MM/YYYY HH:mm');
                    else
                        return moment(new Date(data)).format('YYYY/MM/DD HH:mm:ss');
                }
            },
            {
                "data": "date",
                "render": function (data, type, full) {
                    if (type == 'display')
                        return moment(new Date(data)).locale('pt').format('DD/MM/YYYY HH:mm');
                    else
                        return moment(new Date(data)).format('YYYY/MM/DD HH:mm:ss');
                }
            },
            {
                "data": "max_online_users",
                "bVisible": false
            },
            {
                "data": "questions_count"
            },
            {
                "data": "answered_questions_count",
                "bVisible": false
            },
            {
                "data": "messages_count"
            },
            {
                "data": "votes_count"
            },
            {
                "data": "participants_count"
            },
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

function roomsUrlParams() {
    var url = new URL(location);
    var params = {}

    if (url.searchParams.has('startDate')) {
        params['date__gte'] = startPicker.toString('YYYY-MM-DD');
    }

    if (url.searchParams.has('endDate')) {
        params['date__lte'] = endPicker.toString('YYYY-MM-DD');
    }

    return $.param(params);
}

getResources('/audiencias/api/user/?' + usersUrlParams(), [], loadUserTable);
getResources('/audiencias/api/room/?' + roomsUrlParams(), [], loadRoomTable);
