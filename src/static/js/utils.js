function hideLoading(dataTables) {
  $(dataTables).parent().prev('.JS-loading').remove();
  $(dataTables).find('table').show();
}
