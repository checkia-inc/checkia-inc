/* Progressive enhancement only — every page is fully readable and navigable
   with this file blocked. Two behaviours: the desktop mega menu and the mobile
   drawer. No framework, no dependency, ~1.5 kB. */
(function () {
  "use strict";

  /* ---- mega menu ---- */
  var groups = Array.prototype.slice.call(document.querySelectorAll(".has-mm"));

  function close(g) {
    g.removeAttribute("data-open");
    var b = g.querySelector(".nav-btn");
    if (b) b.setAttribute("aria-expanded", "false");
  }

  function closeAll(except) {
    groups.forEach(function (g) { if (g !== except) close(g); });
  }

  groups.forEach(function (g) {
    var btn = g.querySelector(".nav-btn");
    if (!btn) return;
    var timer;

    btn.addEventListener("click", function () {
      var open = g.getAttribute("data-open") === "true";
      // On a pointer device the menu is already open from hover by the time
      // the click lands. Treating that as a toggle would close it on the way
      // in, so the first click after a hover-open is a no-op.
      if (open && g.dataset.viaHover === "1") {
        g.dataset.viaHover = "";
        return;
      }
      closeAll(g);
      if (open) { close(g); } else {
        g.setAttribute("data-open", "true");
        btn.setAttribute("aria-expanded", "true");
      }
    });

    g.addEventListener("mouseenter", function () {
      if (window.matchMedia("(hover: hover)").matches) {
        clearTimeout(timer);
        closeAll(g);
        g.dataset.viaHover = "1";
        g.setAttribute("data-open", "true");
        btn.setAttribute("aria-expanded", "true");
      }
    });

    g.addEventListener("mouseleave", function () {
      if (window.matchMedia("(hover: hover)").matches) {
        g.dataset.viaHover = "";
        timer = setTimeout(function () { close(g); }, 140);
      }
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll(null);
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-mm")) closeAll(null);
  });

  /* ---- mobile drawer ---- */
  var burger = document.querySelector(".burger");
  var drawer = document.getElementById("mnav");
  if (burger && drawer) {
    burger.addEventListener("click", function () {
      var open = drawer.hasAttribute("hidden");
      if (open) {
        drawer.removeAttribute("hidden");
        burger.setAttribute("aria-expanded", "true");
        burger.setAttribute("aria-label", "Fermer le menu");
      } else {
        drawer.setAttribute("hidden", "");
        burger.setAttribute("aria-expanded", "false");
        burger.setAttribute("aria-label", "Ouvrir le menu");
      }
    });
  }
})();
