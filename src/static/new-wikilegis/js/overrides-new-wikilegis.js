// Open sidebar when accesing Wikilegis login links
$(document).on('click', 'a.js-loginButton', function(e){
  e.preventDefault();
  openEdemSidebar('signin');
});