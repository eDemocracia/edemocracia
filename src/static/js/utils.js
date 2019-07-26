function hideLoading(table) {
  $(table).parent().parent().parent().prev('.JS-loading').remove();
  $(table).show();
}
