$('#search').keyup(function () {
  $('#tabla_autores').DataTable().search($(this).val()).draw();
})
$('#status_filter').change(function () {
  $('#tabla_autores').DataTable().draw();
});
$('#type_filter').change(function () {
  $('#tabla_autores').DataTable().draw();
});
$('#zona').change(function () {
  $('#tabla_autores').DataTable().draw();
});

$('#tabla_autores tbody').on('click', 'button', function () {
  let data = table.row($(this).parents('tr')).data();
  let class_name = $(this).attr('class');
  id = data['id'];

  if (class_name == 'btn btn-edit') {
    $("#confirm").modal();
  } else if (class_name == 'btn btn-show') {
    $('#cover-spin').show(0)
    $.ajax({
      url: '/incidentes/'+ id +'/detalle/',
      type: 'get',
      data: {},
      success: function (data, textStatus, jQxhr) {
        $('#cover-spin').hide()
        let incidente = data['data'][0]
        console.log(incidente)
        let title = "Incidente " +incidente['codigo']
        $("#modalIncidente").modal();
        $('#modal_title').text(title);
        $('#informante').val(incidente['nombre']);
        $('select[name=tipo] option:first').html(types[incidente['tipoAfectacion']]);
        let fecha = incidente['fechaRegistro']
        var parts = fecha.split("/");
        var dt = new Date(parseInt(parts[2], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[0], 10));
        var currentDate = dt.toISOString().slice(0, 10);
        $('#fecha').val(currentDate);
        $('#correo').val(incidente['correo']);
        $('#telefono').val(incidente['telefono']);
        $('#descripcion').val(incidente['descripcion']);
        $('select[name=status] option:first').html(status_filter[incidente['status']]);
      },
      error: function (jqXhr, textStatus, errorThrown) {
        $('#cover-spin').hide()
      }
    });
  } else {
    // DELETE button
    $("#del").modal();
  }
});