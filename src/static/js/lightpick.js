var picker = new Lightpick({
  lang: 'auto',
  field: document.getElementById('startDate'),
  secondField: document.getElementById('endDate'),
  singleDate: true,
  repipck: true,
  parentEl: '.page-statistics > .menu > .wrapper > .date',
  minDate: moment().startOf('month').add(7, 'day'),
  maxDate: moment().endOf('month').subtract(7, 'day'),
});

$('.JS-updateDate').click(function() {
  var startDate = $('#startDate').val();
  var endDate = $('#endDate').val();

  var url = new URL(location);
  if (startDate) {
    if (url.searchParams.has('startDate')) {
      url.searchParams.set('startDate', startDate);
    } else {
      url.searchParams.append('startDate', startDate);
    }
  } else {
    url.searchParams.delete('startDate');
  }

  if (endDate) {
    if (url.searchParams.has('endDate')) {
      url.searchParams.set('endDate', endDate);
    } else {
      url.searchParams.append('endDate', endDate);
    }
  } else {
    url.searchParams.delete('endDate');
  }

  window.location = url;
})