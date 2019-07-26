var startPicker = new Lightpick({
  lang: 'auto',
  field: document.getElementById('startDate'),
  parentEl: '.page-statistics > .menu > .wrapper > .date > .inputs',
});

var endPicker = new Lightpick({
  lang: 'auto',
  field: document.getElementById('endDate'),
  parentEl: '.page-statistics > .menu > .wrapper > .date > .inputs',
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
