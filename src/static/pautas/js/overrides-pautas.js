// Open sidebar when accesing Pauta Participativa login links
$(document).on('click', 'a[href^="/home?next="]', function(e){
  e.preventDefault();
  openEdemSidebar('signin');
});

// Overriding Pauta functions
// Stick remaining votes taking into account .edem-topbar offset
$(window).scroll(function(event) {
  Scroll.themeNavigation();
  if ($('.JS-remaining-votes').length) {
    var navigation = $('.JS-tab-navigation');
    var edemTopbar = $('.edem-topbar');
    var remainingVotes = $('.JS-remaining-votes');
    var margin = parseInt(remainingVotes.css('margin-top'));
    var height = remainingVotesOffset - margin - edemTopbar.outerHeight() - navigation.outerHeight();
    if ($(document).scrollTop() >= height) {
      remainingVotes.addClass('-fixed');
      remainingVotes.attr('style', 'top: ' + navigation.outerHeight() + 'px');
    } else {
      remainingVotes.removeClass('-fixed');
      remainingVotes.removeAttr('style');
    }
  }
});