$(document).click(function(e) {
    var target = e.target
    if (!$(target).closest('.toggled').length) {

      $('.toggled')
        .removeClass('toggled');
    }
});

window.getCookie = function(name) {
  match = document.cookie.match(new RegExp(name + '=([^;]+)'));
  if (match) return match[1];
}

// Set CSRF Token on ajax requests
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

// Input file name show

(function($, window, document, undefined)
{
  $('.button--file').each( function()
  {
    var $input = $(this),
      $label = $input.next('label'),
      labelVal = $label.html();

    $input.on('change', function(e)
    {
      var fileName = '';

      if(this.files && this.files.length > 1)
        fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
      else if(e.target.value)
        fileName = e.target.value.split('\\').pop();

      if(fileName)
        $label.html(fileName);
      else
        $label.html(labelVal);
    });
  });
})(jQuery, window, document);

// User profile image input preview

function changeUserImg(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.user-profile--profile-page').attr('style','background-image:url("'+ e.target.result + '")');
        }
        reader.readAsDataURL(input.files[0]);
        $('.user-profile--profile-page i').hide();
    }
}
$('.user-profile__action--change-picture').change(function(){
    changeUserImg(this);

    // Uncheck clear image if is checked.
    if ($('.user-profile__action--clear-picture').is(':checked')) {
      $('.user-profile__action--clear-picture').click();
    }
});

// Hide user image and change label when clear picture button is checked

$('.user-profile__action--clear-picture').change(function(){
  if ($(this).is(':checked')) {
    $(this).next('label').html('Cancelar remoção');
    $(this).next('label').removeClass('alert');
    $(this).next('label').addClass('warning');
    $('.user-profile--profile-page').addClass('no-bg');
    $('.user-profile--profile-page').html('<i class="icon icon-user" aria-hidden="true"></i>');
  } else {
    $(this).next('label').html('Remover');
    $('.user-profile--profile-page').html('');
    $(this).next('label').addClass('alert');
    $(this).next('label').removeClass('warning');
    $('.user-profile--profile-page').removeClass('no-bg');
  }
});


// eDemocracia open/close edem-access

$('.js-access-link').click(function() {

  $('.edem-access').removeClass('-open');

  if ($(this).parent().hasClass('-active')) {
    $(this).parent().removeClass('-active');
  } else {
    $('.js-access-link').parent().removeClass('-active');
    $(this).parent().addClass('-active');

    if ($(this).hasClass('js-login-link')) {
      $('.js-edem-login').addClass('-open');
    }

    else if ($(this).hasClass('js-signup-link')) {
      $('.js-edem-signup').addClass('-open');
    }

  }

});


// eDemocracia edem-access input status

$('.form__field').focus(function() {
  $(this).addClass('form__field--filled');
});

$('.form__field').blur(function() {
  if (!$(this).val() == '') {
    $(this).addClass('form__field--filled');
  } else {
    $(this).removeClass('form__field--filled')
  }
});

$('#id_form_login').submit(function(event) {
  event.preventDefault();
  $.ajax({
    type:"POST",
    url: '/ajax/login/',
    data: $(event.target).serialize(),
    success: function(response){
      location.reload();
    },
    error: function(jqXRH){
      $('.form__input-error').text('');
      $('.form__input-error')
        .text(jqXRH.responseJSON['data'])
        .removeAttr('hidden');
    }
  });
});

// Go back function inside signup

$('.login-box__button--prev').click(function(){
  $('.login-box__signup-wrapper').removeClass('step-2');
});

// Toggle country/state input

$('.form__input-action.-state').click(function(){
  $(this)
    .closest('.form__input')
    .attr('hidden','');
  $('.form__input-action.-country')
    .closest('.form__input')
    .removeAttr('hidden');
  $('#id_uf')
    .val('')
    .removeClass('form__field--filled');
});

$('.form__input-action.-country').click(function(){
  $(this).closest('.form__input').attr('hidden','');
  $('.form__input-action.-state').closest('.form__input').removeAttr('hidden');
  $('#id_country').val('').removeClass('form__field--filled');
});

// Toggle show password

$('.form__field-action.-showpassword').click(function(){
  var input = $(this).closest('.form__field-container').find('.form__field');
  if (input.attr('type') === 'text') {
    input.attr('type', 'password');
    $(this).children('span').text('Mostrar Senha');
    $(this).children('i').addClass('icon-eye').removeClass('icon-eye-slash');
  } else {
    input.attr('type', 'text');
    $(this).children('span').text('Esconder Senha');
    $(this).children('i').addClass('icon-eye-slash').removeClass('icon-eye');
  }
});

$('#id_form_validation').submit(function(event) {
  event.preventDefault();
  $.ajax({
    type:"POST",
    url: '/ajax/validation/',
    data: $(event.target).serialize(),
    success: function(response){
      window.sessionStorage
        .setItem('userData', JSON.stringify(response['data']));
      $('.login-box__signup-wrapper').addClass('step-2');
    },
    error: function(jqXRH) {
      $('.form__input-error').text('');
      $.each(jqXRH.responseJSON["data"], function(key, value) {
        if (key != '__all__') {
          $(event.target)
            .find('[data-input-name="'+key+'"]')
            .text(value)
            .removeAttr('hidden');
        }
      });
    }
  });
});

$('#id_form_signup').submit(function(event) {
  event.preventDefault();
  var signup_form = {}
  $.map($(event.target).serializeArray(), function(n, i){
    signup_form[n['name']] = n['value'];
  });
  var user_data = $.extend(JSON.parse(sessionStorage.userData), signup_form);
  if (grecaptcha.getResponse() == ""){
    alert("Por favor preencha o reCAPTCHA.");
  } else {
    $.ajax({
      type:"POST",
      url: '/ajax/signup/',
      data: user_data,
      success: function(response){
        console.log(response["data"]);
      },
      error: function(jqXRH) {
        $('.form__input-error').text('');
        $.each(jqXRH.responseJSON["data"], function(key, value) {
          if (key == 'email') {
            $('.login-box__signup-wrapper').removeClass('step-2');
            $('#id_form_validation')
              .find('[data-input-name="'+key+'"]')
              .text(value)
              .removeAttr('hidden');
          } else if (key != '__all__') {
            $(event.target)
              .find('[data-input-name="'+key+'"]')
              .text(value)
              .removeAttr('hidden');
          }
        });
      }
    });
  }
});

