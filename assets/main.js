// EventBuzz - minimal JS: mobile nav + current year + countdowns + scroll reveal
(function () {
  var toggle = document.querySelector('[data-nav-toggle]');
  var mobileNav = document.querySelector('[data-mobile-nav]');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', function () {
      var isOpen = mobileNav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }
  var yearEls = document.querySelectorAll('[data-year]');
  var year = new Date().getFullYear();
  yearEls.forEach(function (el) { el.textContent = year; });

  // Every countdown on the page ticks (hero badge + featured panel).
  document.querySelectorAll('[data-countdown]').forEach(function (cd) {
    var target = new Date(cd.getAttribute('data-countdown'));
    if (isNaN(target)) return;
    var dEl = cd.querySelector('[data-cd-days]');
    var hEl = cd.querySelector('[data-cd-hours]');
    var mEl = cd.querySelector('[data-cd-mins]');
    var sEl = cd.querySelector('[data-cd-secs]');
    function pad(n){ return (n<10?'0':'')+n; }
    function tick(){
      var diff = target - new Date();
      if (diff <= 0) {
        if (dEl) dEl.textContent = '0';
        if (hEl) hEl.textContent = '00';
        if (mEl) mEl.textContent = '00';
        if (sEl) sEl.textContent = '00';
        return;
      }
      var d = Math.floor(diff/86400000);
      var h = Math.floor(diff%86400000/3600000);
      var m = Math.floor(diff%3600000/60000);
      var s = Math.floor(diff%60000/1000);
      if (dEl) dEl.textContent = d;
      if (hEl) hEl.textContent = pad(h);
      if (mEl) mEl.textContent = pad(m);
      if (sEl) sEl.textContent = pad(s);
    }
    tick();
    setInterval(tick, 1000);
  });

  // Tasteful scroll reveal — progressive enhancement only.
  var revealEls = document.querySelectorAll('.card, .section-head, .featured-card, .hero-visual, .cta-band');
  if (revealEls.length) {
    document.documentElement.classList.add('js-reveal');
    revealEls.forEach(function (el) { el.classList.add('reveal'); });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -4% 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add('in-view'); });
    }
  }
})();
