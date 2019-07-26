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

function showDate() {
  var startDate = $('#startDate').val();
  var endDate = $('#endDate').val();

  if (startDate || endDate) {
    $('.JS-statisticsDate').removeClass('hide');

    $('.JS-tableTitle').each(function(){
      var newTitle = $(this).text().replace(':', ' no período:');

      $(this).text(newTitle);
    });

    if (startDate && endDate) {
      $('.JS-statisticsTextDate').text(`Dados de ${startDate} à ${endDate}`);
    } else if (startDate && !endDate) {
      $('.JS-statisticsTextDate').text(`Dados a partir de ${startDate}`);
    } else if (!startDate && endDate) {
      $('.JS-statisticsTextDate').text(`Dados até ${endDate}`);
    }
  }
}

showDate();

$('.JS-removeStatisticsDate').click(function(){
  var startDate = $('#startDate').val();
  var endDate = $('#endDate').val();

  var url = new URL(location);

  if (url.searchParams.has('startDate') || url.searchParams.has('endDate')) {
    url.searchParams.delete('startDate');
    url.searchParams.delete('endDate');

    window.location = url;
  }
});

$('.JS-inputDate').click(function(){
  $(this).focus().on('keydown', function(e){
    if (e.keyCode == 8) {
      $(this).val('');
    }
  });
});
