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
    {
      "data": "tipoProyecto", render: function (data, type, row) {
        console.log(data);
        if (data == '0') {
          resp = 'Preventivo'
        } else if (data == '1') {
          resp = 'Correctivo'
        } else {
          resp = 'Curativo'
        }
        return resp;
      }
    },
    {"data": "fechaInicio"},
    {
      "data": "status", render: function (data, type, row) {
        console.log(data);
        if (data == '0') {
          resp = 'En Proceso'
        } else if (data == '1') {
          resp = 'Pendiente'
        } else {
          resp = 'Completo'
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

Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

$('#tabla_autores tbody').on('click', 'button', function () {
  let data = table.row($(this).parents('tr')).data();
  let class_name = $(this).attr('class');

  id = data['id'];

  if (class_name == 'btn btn-edit') {
    // EDIT button
    $('#nombre').val(data['nombre']);
    $('#codigo').val(data['codigo']);
    let opt = data['tipoProyecto']
    console.log(opt)
    $("#tipoPlan option[value=opt]").attr('selected','selected')
    fecha = data['fechaInicio']
    var parts = fecha.split("/");
    var dt = new Date(parseInt(parts[2], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[0], 10));
    console.log(dt)
    $('#fechaRegistro').val(dt);
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
  $('#fechaRegistro').val(new Date().toDateInputValue());
  $('#fechaRegistro').prop( "disabled", true );
  $('#modal_title').text('Nuevo Proyecto');
  $("#myModal").modal();
});