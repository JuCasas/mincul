    $('#new').on('click', function (e) {
      $('#nombre').val('');
      $('#descripcion').val("");
      $('#fechaInicio').val("");
      $('#fechaFin').val("");
      $('#type').val('new');
      $('#modal_title').text('Nueva Actividad');
      $("#modalActividad").modal();
    });

    $('#formActividad').on('submit', function (e) {
      e.preventDefault();
      let $this = $(this);
      let type = $('#type').val();
      let method = '';
      let url = '/conservacion/proyectos/';
      if (type == 'new') {
        // new
        url = url + $('#idProject').val()+ '/actividades/add/';
        method = 'POST';
      } else {
        // edit
        url = url + 'edit/' + id + '/';
        method = 'POST';
      }

      $.ajax({
        url: url,
        method: method,
        data: $this.serialize(),

        success: function (response) {
          $('#modalActividad').modal('hide')
          $("#tabla_autores").DataTable().draw();
        },
        error: function (error) {
          console.log(error)
        }
      });
    });

$('#tabla_autores tbody').on('click', 'button', function () {
  console.log(this)
  let data = table.row($(this).parents('tr')).data();
  let class_name = $(this).attr('class');

  id = data['id'];
  console.log(data)

  if (class_name == 'btn btn-edit') {
    // EDIT button
    $('#nombre').val(data['nombre']);
    $('#descripcion').val(data['descripcion']);
    var patrimonio = (data['patrimonio']).toString();
    $('#patrimonio').val(patrimonio);
    fechaInicio = data['fechaInicio']
    var partsInicio = fechaInicio.split("/");
    var dtInicio = new Date(parseInt(partsInicio[2], 10),
        parseInt(partsInicio[1], 10) - 1,
        parseInt(partsInicio[0], 10));
    var currentDateInicio = dtInicio.toISOString().slice(0, 10);
    $('#fechaInicio').val(currentDateInicio);
    fechaFin = data['fechaFin']
    var partsFfin = fechaFin.split("/");
    var dtFin = new Date(parseInt(partsFfin[2], 10),
        parseInt(partsFfin[1], 10) - 1,
        parseInt(partsFfin[0], 10));
    var currentDateFin = dtFin.toISOString().slice(0, 10);
    $('#fechaFin').val(currentDateFin);
    $('#type').val('edit');
    $('#modal_title').text('Editar Actividad');
    $("#modalActividad").modal();
  } else {
    // DELETE button
    $('#modalActividad').text('DELETE');
    $("#confirm").modal();
  }
});

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
          // search_value: $('#search').val(),
          // type_filter: $('#type_filter').val(),
          // status_filter: $('#status_filter').val(),
          // order_column: order_column,
          // order: order
      },
      success: function (data, textStatus, jQxhr) {
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
    {"data": "nombre"},
    {"data": "fechaInicio"},
    {"data": "fechaFin"},
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



$('#search').keyup(function () {
  $('#tabla_autores').DataTable().search($(this).val()).draw();
})
$('#exampleFormControlSelect1').change(function () {
  $('#tabla_autores').DataTable().draw();
});
$('#exampleFormControlSelect2').change(function () {
  $('#tabla_autores').DataTable().draw();
});
$('#exampleFormControlSelect3').change(function () {
  $('#tabla_autores').DataTable().draw();
});

$('#tabla_autores tbody').on('click', 'button', function () {
  let data = table.row($(this).parents('tr')).data();
  let class_name = $(this).attr('class');

  id = data['id'];
  idProyectos = data['id'];

  if (class_name == 'btn btn-edit') {
    // EDIT button
    $('#nombre').val(data['nombre']);
    $('#codigo').val(data['codigo']);
    let opt = parseInt(data['tipoProyecto'])
    $("#tipoPlan").val(opt)
    fecha = data['fechaInicio']
    var parts = fecha.split("/");
    var dt = new Date(parseInt(parts[2], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[0], 10));
    var currentDate = dt.toISOString().slice(0, 10);
    $('#fechaRegistro').val(currentDate);
    $('#fechaRegistro').prop("disabled", true);
    $('#type').val('edit');
    $('#modal_title').text('Editar Proyecto');
    $("#myModal").modal();
  } else if (class_name == 'btn btn-show') {
    window.location.pathname = "/conservacion/actividades/" + id + "/tareas/";
  } else {
    // DELETE button
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
  }


});



$('#confirm').on('click', '#delete', function (e) {
  $.ajax({
    url: '/conservacion/proyectos/delete/' + id + '/',
    method: 'POST',
    success: function (response) {
      $('#confirm').modal('hide')
      $("#tabla_autores").DataTable().draw();
    },
    error: function (error) {
      console.log(error)
    }
  });
});


