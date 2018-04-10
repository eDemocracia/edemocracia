isIE = /*@cc_on!@*/false || !!document.documentMode;
isEdge = !isIE && !!window.StyleMedia;

var banner = document.createElement('div');
banner.setAttribute('class', 'info-banner');
banner.innerHTML = '<div class="info-banner"> <img class="info-banner__image" src="/static/img/warning.png" alt="Atenção"> <div class="info-banner__content"> <p class="info-banner__text">O e-Democracia não está pronto para uso nesta versão de navegador.</p><p class="info-banner__text">Utilize um destes navegadores para participar:</p><div class="info-banner__links"> <a class="info-banner__link" href="https://www.google.com.br/chrome/browser/desktop/index.html"> <i class="icon icon-chrome"></i><span class="info-banner__text-span">Google Chrome</span> </a> <a class="info-banner__link" href="https://www.mozilla.org/pt-BR/firefox/new/"> <i class="icon icon-firefox"></i><span class="info-banner__text-span">Mozilla Firefox</span> </a> <a class="info-banner__link" href="https://support.apple.com/pt_BR/downloads/safari"> <i class="icon icon-safari"></i><span class="info-banner__text-span">Safari</span> </a> </div></div></div>';

if (isIE || isEdge) {
  document.body.appendChild(banner);
}
