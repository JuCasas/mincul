
let table = $('#tabla_autores').DataTable({
  "searching": false,
  "serverSide": true,
  "processing": true,
  "lengthChange": false,
  "pageLength": 10,
  "scrollX": true,
  "ajax": function (data, callback, settings) {
    let order_column = data.order[0].column
    let order = data.order[0].dir

    $.ajax({
      url: '',
      type: 'get',
      data: {
          length: data.length,
          start: data.start,
          search_value: $('#search').val(),
          type_filter: $('#type_filter').val(),
          status_filter: $('#status_filter').val(),
          zone_filter: $('#zona').val(),
          order_column: order_column,
          order: order
      },
      success: function (data, textStatus, jQxhr) {
        console.log(data)
        callback({
            recordsTotal: data.recordsTotal,
            recordsFiltered: data.recordsFiltered,
            data: data.data
        });
      },
      error: function (jqXhr, textStatus, errorThrown) {
      }
    });
  },
  "columns": [
    {"data": "codigo"},
    {"data": "zona"},
    {"data": "tipoAfectacion"},
    {"data": "nombre"},
    {"data": "fechaRegistro"},
    {
      "data": "status", render: function (data, type, row) {
        if (data == '0') {
          resp = '<span class="badge badge rounded-capsule d-block badge-soft-primary">' + "En Proceso" + '</span>'
        } else if (data == '1') {
          resp = '<span class="badge badge rounded-capsule d-block badge-soft-warning">' + "Registrado" + '</span>'
        } else {
          resp = '<span class="badge badge rounded-capsule d-block badge-soft-success">' + "Completo" + '</span>'
        }
        return resp;
      }
    },
    {
      "data": null,
      "defaultContent": '<button type="button" class="btn btn-show"><i class="fas fa-eye"></i></button>' + '&nbsp;&nbsp' +
          '<button type="button" class="btn btn-edit"><i class="fas fa-edit"></i></button>' + '&nbsp;&nbsp' +
          '<button type="button" class="btn btn-delete"><i class="fas fa-trash-alt"></i></button>'
    }
  ],
  "language": {
    "processing": '<i class="fa fa-spinner fa-spin" style="font-size:24px;color:rgb(75, 183, 245);"></i>',
    "sLengthMenu": "Mostrar _MENU_ registros",
    "sZeroRecords": "No se encontraron resultados",
    "sEmptyTable": "Ningún dato disponible en esta tabla",
    "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
    "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
    "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
    "sInfoPostFix": "",
    "sSearch": "Buscar:",
    "sUrl": "",
    "sInfoThousands": ",",
    "sLoadingRecords": "Cargando...",
    "oPaginate": {
      "sFirst": "Primero",
      "sLast": "Último",
      "sNext": "Siguiente",
      "sPrevious": "Anterior"
    },
    "oAria": {
      "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
      "sSortDescending": ": Activar para ordenar la columna de manera descendente"
    }
  },
});
