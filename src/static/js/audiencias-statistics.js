
function getObjects(url, objectList) {
    var result = objectList;
    $.ajax({
        url: url,
        async: false,
        success: function (data) {
            result = result.concat(data.results)
            if (data.next) {
                getObjects(data.next, result);
            }
        }
    });
    return result;
}

$(document).ready(function () {
    $('#users-table').DataTable({
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
        data: getObjects('https://dev.edemocracia.camara.leg.br/audiencias/api/user/', []),
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
        data: getObjects('https://dev.edemocracia.camara.leg.br/audiencias/api/room/', []),
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

});
