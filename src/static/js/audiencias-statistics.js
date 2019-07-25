function getResources(path, dataset, callback) {
    var request = $.ajax(path);
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
        $('.JS-loading').remove();
        $('.JS-tableContent').show();
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
                "bVisible": false
            },
            {
                "data": "date"
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
        params['date_joined__gte'] = url.searchParams.get('startDate');
    }

    if (url.searchParams.has('endDate')) {
        params['date_joined__lte'] = url.searchParams.get('endDate');
    }

    return $.param(params);
}

function roomsUrlParams() {
    var url = new URL(location);
    var params = {}

    if (url.searchParams.has('startDate')) {
        params['date__gte'] = url.searchParams.get('startDate');
    }

    if (url.searchParams.has('endDate')) {
        params['date__lte'] = url.searchParams.get('endDate');
    }

    return $.param(params);
}

getResources('/audiencias/api/user/?' + usersUrlParams(), [], loadUserTable);
getResources('/audiencias/api/room/?' + roomsUrlParams(), [], loadRoomTable);