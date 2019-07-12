var picker = new Lightpick({
  lang: 'auto',
  field: document.getElementById('datepicker'),
  singleDate: false,
  minDate: moment().startOf('month').add(7, 'day'),
  maxDate: moment().endOf('month').subtract(7, 'day'),
  onSelect: function(start, end){
    var str = '';
    str += start ? start.format('Do MMMM YYYY') + ' to ' : '';
    str += end ? end.format('Do MMMM YYYY') : '...';
    document.getElementById('result').innerHTML = str;
  }
});
