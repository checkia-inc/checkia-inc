/* CheckIA — comportements des pages blog.
   Tout le contenu est lisible et indexable sans JS ; ce script n'ajoute
   que du confort (progression de lecture, chargement différé des vidéos,
   copie du lien de partage). */
(function () {
  "use strict";

  window.__checkiaReady = true;

  /* --- Barre de progression de lecture (pages article uniquement) ------- */
  var progressBar = document.querySelector(".progress__bar");
  var articleBody = document.querySelector(".article-body");

  if (progressBar && articleBody) {
    var syncProgress = function () {
      var rect = articleBody.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      var done = total > 0 ? Math.min(Math.max(-rect.top / total, 0), 1) : 1;
      progressBar.style.transform = "scaleX(" + done + ")";
    };

    syncProgress();
    window.addEventListener("scroll", syncProgress, { passive: true });
    window.addEventListener("resize", syncProgress, { passive: true });
  }

  /* --- Façade vidéo : l'iframe YouTube n'est injectée qu'au clic --------
     La page ne charge aucun script tiers tant que l'utilisateur n'a pas
     demandé la lecture (performance + RGPD via youtube-nocookie). */
  var shells = document.querySelectorAll(".videoshell[data-video-id]");

  Array.prototype.forEach.call(shells, function (shell) {
    var play = shell.querySelector(".videoshell__play");
    if (!play) return;

    play.addEventListener("click", function () {
      var id = shell.getAttribute("data-video-id");
      var iframe = document.createElement("iframe");

      iframe.src =
        "https://www.youtube-nocookie.com/embed/" +
        encodeURIComponent(id) +
        "?autoplay=1&rel=0";
      iframe.title = shell.getAttribute("data-video-title") || "Vidéo";
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.setAttribute("allowfullscreen", "");

      shell.appendChild(iframe);
      shell.classList.add("is-playing");
      play.remove();
    });
  });

  /* Chapitres : recharge la vidéo au bon horodatage --------------------- */
  var chapterLinks = document.querySelectorAll(".chapters a[data-start]");

  Array.prototype.forEach.call(chapterLinks, function (link) {
    link.addEventListener("click", function (event) {
      var shell = document.querySelector(".videoshell[data-video-id]");
      if (!shell) return;

      event.preventDefault();

      var id = shell.getAttribute("data-video-id");
      var start = parseInt(link.getAttribute("data-start"), 10) || 0;
      var play = shell.querySelector(".videoshell__play");
      if (play) play.remove();

      var iframe = shell.querySelector("iframe");
      if (!iframe) {
        iframe = document.createElement("iframe");
        iframe.title = shell.getAttribute("data-video-title") || "Vidéo";
        iframe.allow =
          "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
        iframe.setAttribute("allowfullscreen", "");
        shell.appendChild(iframe);
      }

      iframe.src =
        "https://www.youtube-nocookie.com/embed/" +
        encodeURIComponent(id) +
        "?autoplay=1&rel=0&start=" + start;

      shell.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });

  /* --- Copie du lien de l'article --------------------------------------- */
  var copyBtn = document.querySelector("[data-copy-link]");

  if (copyBtn && navigator.clipboard) {
    var initialLabel = copyBtn.textContent;

    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(window.location.href).then(function () {
        copyBtn.textContent = "Lien copié";
        window.setTimeout(function () {
          copyBtn.textContent = initialLabel;
        }, 2000);
      });
    });
  }
})();
