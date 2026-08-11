"""Inline SVG diagrams.

Versioned in the repo, themed with CSS custom properties, no network weight and
no external asset dependency. Every diagram carries a title/desc for assistive
technology and is described in prose nearby so the page still reads without it.
"""

import zlib


def _frame(body, view="0 0 900 420", label="", desc="", cls=""):
    # zlib.crc32 rather than hash(): PRNG-seeded string hashing would change the
    # generated ids on every build and make the output non-reproducible.
    uid = zlib.crc32(label.encode("utf-8")) % 99999
    return (
        '<svg class="dgm%s" viewBox="%s" role="img" aria-labelledby="t%d d%d" '
        'preserveAspectRatio="xMidYMid meet">'
        '<title id="t%d">%s</title><desc id="d%d">%s</desc>%s</svg>'
    ) % ((" " + cls) if cls else "", view, uid, uid, uid, label, uid, desc, body)


def pipeline():
    """The five mission stages, as the product actually sequences them.

    Laid out vertically: this diagram sits in the hero's right-hand column,
    against a tall text column. A wide, short arrangement would render at a
    fraction of the column height and read as an afterthought, so the stages
    stack and the block fills its column.
    """
    # Sub-labels are kept short on purpose: they are rendered as SVG <text>,
    # which does not wrap. The full document list lives in the prose nearby.
    stages = [
        ("Acceptation", "Indépendance, fiche d'acceptation"),
        ("Contractualisation", "Lettre de mission, budget"),
        ("Planification", "Plan de mission, organisation"),
        ("Travaux", "Documents de travail"),
        ("Restitution", "Lettre d'affirmation, rapport"),
    ]
    W = 620          # viewBox width
    PAD = 16         # left inset of the card column
    CARD_W = W - PAD * 2
    CARD_H = 92
    GAP = 22
    TOP = 96         # first card's y
    BADGE_CX = PAD + 42

    parts = []
    for idx, (name, sub) in enumerate(stages):
        y = TOP + idx * (CARD_H + GAP)
        mid = y + CARD_H // 2
        parts.append(
            '<g class="dgm-node">'
            '<rect x="%d" y="%d" width="%d" height="%d" rx="14"/>'
            '<circle class="dgm-badge" cx="%d" cy="%d" r="19"/>'
            '<text class="dgm-badge-n" x="%d" y="%d">%d</text>'
            '<text class="dgm-t" x="%d" y="%d">%s</text>'
            '<text class="dgm-s" x="%d" y="%d">%s</text>'
            "</g>"
            % (PAD, y, CARD_W, CARD_H,
               BADGE_CX, mid,
               BADGE_CX, mid + 6, idx + 1,
               BADGE_CX + 42, mid - 6, name,
               BADGE_CX + 42, mid + 18, sub)
        )
        if idx < len(stages) - 1:
            parts.append(
                '<path class="dgm-arrow" d="M%d %d L%d %d" marker-end="url(#ah)"/>'
                % (BADGE_CX, y + CARD_H, BADGE_CX, y + CARD_H + GAP - 5)
            )

    bottom = TOP + len(stages) * (CARD_H + GAP) - GAP
    defs = (
        '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" class="dgm-arrowhead"/></marker></defs>'
    )
    head = (
        '<text class="dgm-cap" x="%d" y="34">Déroulé d\'une mission dans CheckIA</text>'
        '<text class="dgm-caps" x="%d" y="60">Chaque étape s\'ouvre manuellement ;</text>'
        '<text class="dgm-caps" x="%d" y="78">les documents d\'une même étape avancent en parallèle.</text>'
        % (PAD, PAD, PAD)
    )
    foot = (
        '<text class="dgm-caps" x="%d" y="%d">Fin de mission à l\'envoi du rapport signé.</text>'
        % (PAD, bottom + 30)
    )
    return _frame(
        defs + head + "".join(parts) + foot,
        view="0 0 %d %d" % (W, bottom + 44),
        label="Les cinq étapes d'une mission",
        desc="Acceptation, contractualisation, planification, travaux, restitution.",
        cls="dgm-v",
    )


def lifecycle():
    """Document status lifecycle — the seven states, verbatim from the spec."""
    states = [
        ("À valider", 30, "s-a"),
        ("Validé", 178, "s-b"),
        ("En attente signature", 326, "s-c"),
        ("Signé", 528, "s-d"),
        ("Signé par client", 676, "s-e"),
    ]
    parts = []
    for label, x, cls in states:
        w = 132 if len(label) < 16 else 176
        parts.append(
            '<g class="dgm-pill %s"><rect x="%d" y="96" width="%d" height="38" rx="19"/>'
            '<text x="%d" y="120">%s</text></g>' % (cls, x, w, x + w / 2, label)
        )
    arrows = [
        (162, 200, "Validation collaborateur"),
        (310, 348, "Notification au CAC"),
        (502, 550, "Signature du CAC"),
        (660, 698, "Signature client"),
    ]
    for x1, x2, lab in arrows:
        mid = (x1 + x2) / 2
        parts.append(
            '<path class="dgm-arrow" d="M%d 115 L%d 115" marker-end="url(#ah2)"/>'
            '<text class="dgm-edge" x="%d" y="84">%s</text>' % (x1, x2 - 4, mid, lab)
        )
    # the two loops
    parts.append(
        '<path class="dgm-loop" d="M232 140 C232 190 96 190 96 140" '
        'marker-end="url(#ah2)"/>'
        '<text class="dgm-edge dgm-edge-lo" x="164" y="205">Mise à jour par le collaborateur</text>'
    )
    parts.append(
        '<path class="dgm-loop dgm-loop-r" d="M414 92 C414 40 96 40 96 90" '
        'marker-end="url(#ah2)"/>'
        '<text class="dgm-edge dgm-edge-r" x="255" y="32">À mettre à jour — le CAC renvoie le document</text>'
    )
    defs = (
        '<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" class="dgm-arrowhead"/></marker></defs>'
    )
    return _frame(
        defs + "".join(parts),
        view="0 0 880 225",
        label="Cycle de vie d'un document de mission",
        desc=(
            "À valider, validé, en attente de signature, signé, signé par client, "
            "avec une boucle de mise à jour et une boucle de renvoi."
        ),
    )


def before_after():
    """The formalisation problem, stated as two paths."""
    before = ["Pièces éparses", "Ressaisie Word/Excel", "Copier-coller",
              "Relecture des écarts", "Dossier hétérogène"]
    after = ["Données de mission", "Trames du cabinet", "Génération",
             "Validation humaine", "Dossier traçable"]

    def row(items, y, cls, label):
        parts = ['<text class="dgm-rowlab" x="18" y="%d">%s</text>' % (y - 26, label)]
        x = 18
        for idx, it in enumerate(items):
            parts.append(
                '<g class="dgm-chip %s"><rect x="%d" y="%d" width="150" height="46" rx="10"/>'
                '<text x="%d" y="%d">%s</text></g>' % (cls, x, y, x + 75, y + 28, it)
            )
            if idx < len(items) - 1:
                parts.append(
                    '<path class="dgm-arrow" d="M%d %d L%d %d" marker-end="url(#ah3)"/>'
                    % (x + 152, y + 23, x + 166, y + 23)
                )
            x += 168
        return "".join(parts)

    defs = (
        '<defs><marker id="ah3" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" class="dgm-arrowhead"/></marker></defs>'
    )
    return _frame(
        defs + row(before, 52, "chip-mute", "Formalisation manuelle")
        + row(after, 168, "chip-live", "Avec CheckIA"),
        view="0 0 880 240",
        label="Formalisation manuelle comparée au flux CheckIA",
        desc=(
            "En haut, un enchaînement manuel aboutissant à un dossier hétérogène. "
            "En bas, données de mission, trames, génération, validation humaine, "
            "dossier traçable."
        ),
    )


def generic_vs_checkia():
    """Why a generic chatbot is a different object from a mission platform."""
    left = ["Prompt", "Texte généré"]
    right = ["Mission", "Documents sources", "Contexte structuré",
             "Trame du cabinet", "Document produit", "Revue humaine", "Traçabilité"]
    parts = [
        '<text class="dgm-rowlab" x="18" y="34">Assistant généraliste</text>',
        '<text class="dgm-rowlab" x="18" y="140">Plateforme de mission</text>',
    ]
    x = 18
    for idx, it in enumerate(left):
        parts.append(
            '<g class="dgm-chip chip-mute"><rect x="%d" y="48" width="164" height="44" rx="10"/>'
            '<text x="%d" y="75">%s</text></g>' % (x, x + 82, it)
        )
        if idx < len(left) - 1:
            parts.append('<path class="dgm-arrow" d="M%d 70 L%d 70" marker-end="url(#ah4)"/>' % (x + 166, x + 180))
        x += 182
    x = 18
    for idx, it in enumerate(right):
        parts.append(
            '<g class="dgm-chip chip-live"><rect x="%d" y="154" width="112" height="44" rx="10"/>'
            '<text class="dgm-sm" x="%d" y="181">%s</text></g>' % (x, x + 56, it)
        )
        if idx < len(right) - 1:
            parts.append('<path class="dgm-arrow" d="M%d 176 L%d 176" marker-end="url(#ah4)"/>' % (x + 114, x + 124))
        x += 126
    defs = (
        '<defs><marker id="ah4" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" class="dgm-arrowhead"/></marker></defs>'
    )
    return _frame(
        defs + "".join(parts),
        view="0 0 900 215",
        label="Assistant généraliste comparé à une plateforme de mission",
        desc=(
            "Un assistant généraliste va du prompt au texte. Une plateforme de mission "
            "va de la mission aux documents sources, au contexte structuré, à la trame "
            "du cabinet, au document produit, à la revue humaine et à la traçabilité."
        ),
    )


REGISTRY = {
    "pipeline": pipeline,
    "lifecycle": lifecycle,
    "before-after": before_after,
    "generic-vs-checkia": generic_vs_checkia,
}


def get(name):
    fn = REGISTRY.get(name)
    return fn() if fn else ""
