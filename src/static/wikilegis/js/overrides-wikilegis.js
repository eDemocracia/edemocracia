// Open sidebar when accesing Wikilegis login links
$(document).on('click', 'a[href^="/wikilegis/accounts/login/"]', function(e){
  e.preventDefault();
  openEdemSidebar('signin');
});