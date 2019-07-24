
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
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ],
        data: getObjects('https://dev.edemocracia.camara.leg.br/audiencias/api/user/', []),
        "columns": [
            {
                "data": "id"
            },
            {
                "data": "username"
            },
            {
                "data": "first_name"
            },
            {
                "data": "last_name"
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
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json"
        },
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel'
        ],
        data: getObjects('https://dev.edemocracia.camara.leg.br/audiencias/api/room/', []),
        "columns": [
            {
                "data": "id"
            },
            {
                "data": "cod_reunion"
            },
            {
                "data": "legislative_body"
            },
            {
                "data": "legislative_body_initials"
            },
            {
                "data": "reunion_type"
            },
            {
                "data": "title_reunion"
            },
            {
                "data": "reunion_object"
            },
            {
                "data": "reunion_theme"
            },
            {
                "data": "location"
            },
            {
                "data": "created"
            },
            {
                "data": "date"
            },
            {
                "data": "max_online_users"
            },
            {
                "data": "questions_count"
            },
            {
                "data": "answered_questions_count"
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