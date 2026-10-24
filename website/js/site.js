// Greystone Guesthouse: shared nav, mobile menu, scroll reveal and conversion tracking.
(function () {
  var nav = document.getElementById('nav');

  // Nav scroll effect
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 80); };
    window.addEventListener('scroll', onScroll, { passive: true });
    requestAnimationFrame(onScroll); // first check waits a frame, so it doesn't force layout at start-up
  }

  // Mobile menu: the toggle opens the full list; Esc or a link click closes it.
  var toggle = nav && nav.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    var setOpen = function (open, returnFocus) {
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) {
        var first = menu.querySelector('a');
        if (first) first.focus();
      } else if (returnFocus) {
        toggle.focus();
      }
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true', true);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) setOpen(false, true);
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a') && nav.classList.contains('open')) setOpen(false, false);
    });
    // Tabbing out of the bar closes the menu, so the focused link isn't hidden under the panel.
    nav.addEventListener('focusout', function (e) {
      if (nav.classList.contains('open') && e.relatedTarget && !nav.contains(e.relatedTarget)) setOpen(false, false);
    });
    window.addEventListener('resize', function () {
      if (nav.classList.contains('open') && getComputedStyle(toggle).display === 'none') setOpen(false, false);
    });
  }

  // Scroll reveal via IntersectionObserver
  var revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          observer.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('visible'); });
  }

  // Conversion tracking (event names are counted by the weekly and monthly reports: don't rename)
  document.addEventListener('click', function (e) {
    if (typeof gtag !== 'function') return;
    var link = e.target.closest('a[href]');
    if (!link) return;
    var href = link.href;
    var label = link.getAttribute('aria-label') || link.textContent.trim();
    if (href.indexOf('book.nightsbridge.com') !== -1) {
      gtag('event', 'begin_booking', {
        event_category: 'conversion',
        event_label: label,
        link_url: href
      });
    } else if (href.indexOf('wa.me') !== -1) {
      var params = {
        event_category: 'conversion',
        event_label: label,
        link_url: href
      };
      // "Staying at Greystone?" boxes say which help they offer: surf, shuttle or restaurants.
      var topic = link.getAttribute('data-help-topic');
      if (topic) params.help_topic = topic;
      gtag('event', 'contact_whatsapp', params);
    } else if (href.indexOf('tel:') === 0) {
      // Tap-to-call in the footer: a call is as valuable as a WhatsApp message.
      gtag('event', 'contact_phone', {
        event_category: 'conversion',
        event_label: label,
        link_url: href
      });
    } else if (href.indexOf('reviews.html') !== -1) {
      gtag('event', 'view_reviews', {
        event_category: 'engagement',
        event_label: label
      });
    } else if (href.indexOf('booking.com') !== -1) {
      gtag('event', 'click_booking_com', {
        event_category: 'outbound',
        event_label: label,
        link_url: href
      });
    } else if (href.indexOf('tripadvisor') !== -1) {
      gtag('event', 'click_tripadvisor', {
        event_category: 'outbound',
        event_label: label,
        link_url: href
      });
    } else if (href.indexOf('#') !== -1) {
      var section = href.split('#')[1];
      if (section) {
        gtag('event', 'navigate_section', {
          event_category: 'engagement',
          event_label: section
        });
      }
    }
  });
})();
