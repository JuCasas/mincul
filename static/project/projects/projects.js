let table = $('#tabla_autores').DataTable({
  "searching": false,
  "serverSide": true,
  "processing": true,
  "lengthChange": false,
  "ajax": function (data, callback, settings) {
    //var columna_filtro = data.columns[data.order[0].column].data.replace(/\./g,"__")
    $.get('', {
          length: data.length,
          start: data.start,
          search_value: $('#search').val(),

        }, function (res) {
          console.log(res)
          callback({
            recordsTotal: res.recordsTotal,
            recordsFiltered: res.recordsFiltered,
            data: res.data
          });
        },
    );
  },
  "columns": [
    {"data": "codigo"},
    {"data": "nombre"},
    {"data": "descripcion"},
    {"data": "nombre"},
    {"data": "fechaInicio"},
    {"data": "nombre"},
    {
      "data": null,
      "defaultContent": '<button type="button" class="btn btn-show"><i class="fas fa-eye"></i></button>' + '&nbsp;&nbsp' +
          '<button type="button" class="btn btn-edit"><i class="fas fa-edit"></i></button>' + '&nbsp;&nbsp' +
          '<button type="button" class="btn btn-delete"><i class="fas fa-trash-alt"></i></button>'
    }
  ],
  "language": {
        "sProcessing":    "Procesando...",
        "sLengthMenu":    "Mostrar _MENU_ registros",
        "sZeroRecords":   "No se encontraron resultados",
        "sEmptyTable":    "Ningún dato disponible en esta tabla",
        "sInfo":          "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "sInfoEmpty":     "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered":  "(filtrado de un total de _MAX_ registros)",
        "sInfoPostFix":   "",
        "sSearch":        "Buscar:",
        "sUrl":           "",
        "sInfoThousands":  ",",
        "sLoadingRecords": "Cargando...",
        "oPaginate": {
            "sFirst":    "Primero",
            "sLast":    "Último",
            "sNext":    "Siguiente",
            "sPrevious": "Anterior"
        },
        "oAria": {
            "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
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

  if (class_name == 'btn btn-edit') {
    // EDIT button
    $('#nombre').val(data['nombre']);
    $('#codigo').val(data['codigo']);
    $('#type').val('edit');
    $('#modal_title').text('Editar Proyecto');
    $("#myModal").modal();
  } else if (class_name == 'btn btn-show') {
    window.location.pathname = "/conservacion/proyectos/" + id + "/actvidades/";
  } else {
    // DELETE button
    $('#modal_title').text('DELETE');
    $("#confirm").modal();
  }


});

$('form').on('submit', function (e) {
  e.preventDefault();
  let $this = $(this);
  let type = $('#type').val();
  let method = '';
  let url = '/conservacion/proyectos/';
  if (type == 'new') {
    // new
    url = url + 'add/';
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
      $('#myModal').modal('hide')
      $("#tabla_autores").DataTable().draw();
    },
    error: function (error) {
      console.log(error)
    }
  });
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


$('#new').on('click', function (e) {
  $('#codigo').val('');
  $('#nombre').val('');
  $('#type').val('new');
  $('#modal_title').text('Nuevo Proyecto');
  $("#myModal").modal();
});