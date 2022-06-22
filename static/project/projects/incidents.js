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