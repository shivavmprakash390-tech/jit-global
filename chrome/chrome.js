/*! JIT Global shared chrome behavior */
(function () {
  if (window.__JIT_CHROME_INIT__) return;
  window.__JIT_CHROME_INIT__ = true;
  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function initYear() {
    var el = document.getElementById('year');
    if (el) el.textContent = String(new Date().getFullYear());
  }

  function initScrollNav() {
    var navbar = document.getElementById('navbar');
    if (!navbar) return;
    var onScroll = function () {
      if (window.scrollY > 40) {
        navbar.classList.add('nav-scrolled');
        navbar.classList.remove('nav-top');
      } else {
        navbar.classList.add('nav-top');
        navbar.classList.remove('nav-scrolled');
      }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function initMobileMenu() {
    var toggle = document.getElementById('menu-toggle');
    var menu = document.getElementById('mobile-menu');
    if (!toggle || !menu) return;
    var iconOpen = document.getElementById('icon-open');
    var iconClose = document.getElementById('icon-close');
    var setOpen = function (open) {
      if (open) {
        menu.hidden = false;
        menu.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
        if (iconOpen) iconOpen.classList.add('hidden');
        if (iconClose) iconClose.classList.remove('hidden');
      } else {
        menu.classList.remove('open');
        menu.hidden = true;
        toggle.setAttribute('aria-expanded', 'false');
        if (iconOpen) iconOpen.classList.remove('hidden');
        if (iconClose) iconClose.classList.add('hidden');
      }
    };
    toggle.addEventListener('click', function () {
      setOpen(!!menu.hidden);
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
  }

  function initInnerMegas() {
    var ids = ['nav-services', 'nav-technology', 'nav-industries', 'nav-company'];
    var navbar = document.getElementById('navbar');
    var CLOSE_DELAY_MS = 160;
    var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var closeTimer = null;
    var items = [];

    var clearCloseTimer = function () {
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
    };
    var closeAll = function () {
      clearCloseTimer();
      items.forEach(function (entry) {
        entry.item.classList.remove('is-open');
        if (entry.btn) entry.btn.setAttribute('aria-expanded', 'false');
      });
    };
    var openItem = function (target) {
      clearCloseTimer();
      items.forEach(function (entry) {
        var on = entry.item === target;
        entry.item.classList.toggle('is-open', on);
        if (entry.btn) entry.btn.setAttribute('aria-expanded', on ? 'true' : 'false');
      });
    };
    var scheduleCloseAll = function () {
      clearCloseTimer();
      closeTimer = setTimeout(closeAll, CLOSE_DELAY_MS);
    };

    ids.forEach(function (id) {
      var item = document.getElementById(id);
      if (!item) return;
      var btn = item.querySelector(':scope > .nav-link, :scope > button.nav-link');
      var panel = item.querySelector('.mega-panel');
      if (!btn || !panel) return;
      items.push({ item: item, btn: btn, panel: panel });

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        clearCloseTimer();
        if (item.classList.contains('is-open')) closeAll();
        else openItem(item);
      });

      if (canHover) item.addEventListener('mouseenter', function () { openItem(item); });

      panel.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () { closeAll(); });
      });

      item.querySelectorAll('.mega-side-btn').forEach(function (sb) {
        sb.addEventListener('click', function (e) {
          e.stopPropagation();
          clearCloseTimer();
          var tab = sb.getAttribute('data-mega-tab');
          item.querySelectorAll('.mega-side-btn').forEach(function (b) {
            var on = b === sb;
            b.classList.toggle('is-active', on);
            b.setAttribute('aria-selected', on ? 'true' : 'false');
          });
          item.querySelectorAll('.mega-panel-body').forEach(function (body) {
            body.hidden = body.getAttribute('data-mega-panel') !== tab;
          });
        });
      });

      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          if (item.classList.contains('is-open')) closeAll();
          else openItem(item);
        }
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          openItem(item);
          var first = panel.querySelector('a, button.mega-side-btn');
          if (first) first.focus();
        }
        if (e.key === 'Escape') closeAll();
      });
    });

    if (canHover && navbar) {
      navbar.addEventListener('mouseenter', clearCloseTimer);
      navbar.addEventListener('mouseleave', scheduleCloseAll);
    }
    document.addEventListener('click', function (e) {
      if (navbar && !navbar.contains(e.target)) closeAll();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeAll();
    });
  }

  ready(function () {
    initYear();
    initScrollNav();
    initMobileMenu();
    initInnerMegas();
  });
})();
