/* CheckIA — mesure des interactions (Google Analytics 4).
   Envoie des événements personnalisés via gtag ; sans effet si gtag est absent.
   Événements : button_click, book_call, email_click, contact_form_submit. */
(function () {
  "use strict";

  function track(name, params) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, params || {});
  }
  window.checkiaTrack = track;

  function label(el) {
    var text = el.getAttribute("aria-label");
    if (!text) {
      // Libellé le plus lisible : titre d'onglet, sinon texte du bouton
      // sans la variante courte du bouton de navigation (« démo »).
      var title = el.querySelector(".tab__title");
      if (title) {
        text = title.textContent;
      } else {
        var clone = el.cloneNode(true);
        var shorts = clone.querySelectorAll(".nav-cta__short");
        for (var i = 0; i < shorts.length; i++) shorts[i].parentNode.removeChild(shorts[i]);
        text = clone.textContent || "";
      }
    }
    return text.replace(/\s+/g, " ").trim().slice(0, 100);
  }

  function buttonType(el, href) {
    if (href.indexOf("calendar.notion.so") !== -1) return "prise_de_rendez_vous";
    if (href.indexOf("mailto:") === 0) return "email";
    if (el.getAttribute("type") === "submit") return "envoi_formulaire";
    if (el.classList.contains("nav-cta")) return "navigation";
    if (el.classList.contains("btn")) return "appel_a_l_action";
    if (el.classList.contains("videoshell__play") || el.classList.contains("player__facade")) return "video";
    if (el.classList.contains("tab")) return "onglet";
    if (el.hasAttribute("data-copy-link")) return "copier_le_lien";
    return "autre";
  }

  document.addEventListener("click", function (e) {
    var el = e.target.closest ? e.target.closest("a.btn, a.nav-cta, a[href*='calendar.notion.so'], a[href^='mailto:'], button") : null;
    if (!el) return;

    var href = el.getAttribute("href") || "";
    var params = {
      button_text: label(el),
      button_type: buttonType(el, href),
      link_url: href,
      page_path: window.location.pathname
    };

    track("button_click", params);
    if (params.button_type === "prise_de_rendez_vous") track("book_call", params);
    if (params.button_type === "email") track("email_click", params);
  }, true);
})();
