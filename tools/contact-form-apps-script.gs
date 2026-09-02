/**
 * Backend du formulaire de contact checkia.fr/contact/
 *
 * Déploiement :
 * 1. Aller sur https://script.google.com (connecté au compte qui gère contact@checkia.fr).
 * 2. Nouveau projet → coller ce code.
 * 3. Déployer → Nouveau déploiement → type « Application web » :
 *    - Exécuter en tant que : Moi
 *    - Accès : Tout le monde
 * 4. Copier l'URL « /exec » et la coller dans SCRIPT_URL
 *    du fichier contact/index.html.
 */

var DESTINATAIRE = "contact@checkia.fr";

function doPost(e) {
  try {
    var p = e.parameter;

    var nom = (p.nom || "").trim();
    var email = (p.email || "").trim();
    var cabinet = (p.cabinet || "").trim();
    var telephone = (p.telephone || "").trim();
    var message = (p.message || "").trim();

    if (!nom || !email) {
      return reponse({ ok: false, error: "Champs requis manquants" });
    }

    var sujet = "Nouveau message via checkia.fr — " + nom + (cabinet ? " (" + cabinet + ")" : "");

    var corps =
      "Nouveau message reçu via le formulaire de contact checkia.fr\n\n" +
      "Nom : " + nom + "\n" +
      "E-mail : " + email + "\n" +
      "Cabinet / Société : " + (cabinet || "—") + "\n" +
      "Téléphone : " + (telephone || "—") + "\n\n" +
      "Message :\n" + (message || "—") + "\n";

    MailApp.sendEmail({
      to: DESTINATAIRE,
      replyTo: email,
      subject: sujet,
      body: corps
    });

    return reponse({ ok: true });
  } catch (err) {
    return reponse({ ok: false, error: String(err) });
  }
}

function reponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
