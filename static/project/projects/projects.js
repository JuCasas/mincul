$(document).ready(function () {
  $('#tabla_autores').DataTable({
    "searching": false,
    "serverSide": true,
    "processing": true,
    "ajax": function (data, callback, settings) {
      //var columna_filtro = data.columns[data.order[0].column].data.replace(/\./g,"__")
      $.get('', {
            length: data.length,
            start: data.start,
            search_value: $('#search').val()
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
        "defaultContent": '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' +
            '<button type="button" class="btn btn-danger">Delete</button>'
      }
    ],

  });
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

$('form').on('submit', function (e) {
  e.preventDefault();
  let $this = $(this);
  let type = $('#type').val();
  let method = '';
  let url = '/conservacion/proyectos/add/';
  if (type == 'new') {
    // new
    method = 'POST';
  } else {
    // edit
    url = url + id + '/';
    method = 'PUT';
  }

  $.ajax({
    url: url,
    method: method,
    data: $this.serialize(),

    success: function (response) {
      location.reload();
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