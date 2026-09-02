/* CheckIA — comportements de la page d'accueil.
   Le contenu est visible sans JS ; ce script n'ajoute que du confort. */
(function () {
  "use strict";

  // Signale au chien de garde de index.html que le script a bien démarré.
  window.__checkiaReady = true;

  /* --- Barre de navigation : ombre au défilement ------------------------ */
  var nav = document.querySelector(".nav");

  if (nav) {
    var syncNav = function () {
      nav.classList.toggle("is-stuck", window.scrollY > 8);
    };

    syncNav();
    window.addEventListener("scroll", syncNav, { passive: true });
  }

  /* --- Menu mobile (hamburger) ------------------------------------------ */
  var navActions = nav ? nav.querySelector(".nav__actions") : null;
  var navLinks = nav ? nav.querySelector(".nav__links") : null;

  if (navActions && navLinks) {
    var burger = document.createElement("button");
    burger.type = "button";
    burger.className = "nav__burger";
    burger.setAttribute("aria-label", "Ouvrir le menu");
    burger.setAttribute("aria-expanded", "false");
    burger.innerHTML = "<span></span><span></span><span></span>";
    navActions.appendChild(burger);

    var setMenu = function (open) {
      nav.classList.toggle("nav--open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    };

    burger.addEventListener("click", function () {
      setMenu(!nav.classList.contains("nav--open"));
    });

    // Ferme le menu après un clic sur un lien ou en repassant en grand écran.
    navLinks.addEventListener("click", function () { setMenu(false); });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 992) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  /* --- Apparition progressive ------------------------------------------ */
  var revealables = document.querySelectorAll(".reveal");

  if (!("IntersectionObserver" in window)) {
    // Pas d'observateur : on affiche tout immédiatement.
    Array.prototype.forEach.call(revealables, function (el) {
      el.classList.add("is-in");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );

    Array.prototype.forEach.call(revealables, function (el) {
      observer.observe(el);
    });

    // Filet de sécurité : tout est révélé au bout de 3 s, quoi qu'il arrive.
    window.setTimeout(function () {
      Array.prototype.forEach.call(revealables, function (el) {
        el.classList.add("is-in");
      });
    }, 3000);
  }

  /* --- Onglets « Fonctionnalités opérationnelles » --------------------- */
  var tablist = document.querySelector('[role="tablist"]');

  if (tablist) {
    var tabs = Array.prototype.slice.call(
      tablist.querySelectorAll('[role="tab"]')
    );

    var select = function (tab, focus) {
      tabs.forEach(function (item) {
        var active = item === tab;
        var panel = document.getElementById(
          item.getAttribute("aria-controls")
        );

        item.setAttribute("aria-selected", active ? "true" : "false");
        item.setAttribute("tabindex", active ? "0" : "-1");

        if (panel) {
          panel.classList.toggle("is-active", active);
          panel.hidden = !active;
        }
      });

      if (focus) tab.focus();
    };

    tabs.forEach(function (tab, index) {
      tab.addEventListener("click", function () {
        select(tab, false);
      });

      tab.addEventListener("keydown", function (event) {
        var next = null;

        if (event.key === "ArrowDown" || event.key === "ArrowRight") {
          next = tabs[(index + 1) % tabs.length];
        } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
          next = tabs[(index - 1 + tabs.length) % tabs.length];
        } else if (event.key === "Home") {
          next = tabs[0];
        } else if (event.key === "End") {
          next = tabs[tabs.length - 1];
        }

        if (!next) return;
        event.preventDefault();
        select(next, true);
      });
    });
  }
})();
