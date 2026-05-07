"""
Render the Couples App architecture diagrams as PNGs.

Produces 6 diagrams in this directory:
  1_context.png         — C4 Level 1 (System Context)
  2_container.png       — C4 Level 2 (Containers)
  3_component.png       — C4 Level 3 (Components inside Next.js app)
  4_seq_signup.png      — Sequence: signup
  5_seq_pairing.png     — Sequence: couple pairing
  6_seq_todo.png        — Sequence: todo create + realtime fan-out

Style: warm/cream background, soft pastel boxes, dark-slate text.
Run:  python3 render.py
"""

from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Ellipse
from matplotlib.lines import Line2D

# ============================================================================
# Style
# ============================================================================

BG = "#FFFBF5"
INK = "#1F2937"
INK_SOFT = "#4B5563"
INK_FAINT = "#9CA3AF"

PALETTE = {
    "person":          ("#FDE68A", "#92400E"),
    "system_focus":    ("#BFDBFE", "#1E3A8A"),
    "external":        ("#F3F4F6", "#6B7280"),
    "container":       ("#DBEAFE", "#1E40AF"),
    "container_alt":   ("#DDD6FE", "#5B21B6"),
    "db":              ("#FECACA", "#991B1B"),
    "delivery":        ("#FEF3C7", "#92400E"),
    "adapters":        ("#DBEAFE", "#1E40AF"),
    "application":     ("#BBF7D0", "#166534"),
    "domain":          ("#FBCFE8", "#9D174D"),
    "boundary":        ("#FFFFFF", "#9CA3AF"),
}

FONT_FAMILY = "DejaVu Sans"

# ============================================================================
# Drawing helpers
# ============================================================================

def setup_ax(ax, w, h, title=None, subtitle=None):
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(BG)
    if title:
        ax.text(w / 2, h - 0.3, title,
                ha="center", va="top",
                fontsize=18, fontweight="bold", color=INK,
                family=FONT_FAMILY)
    if subtitle:
        ax.text(w / 2, h - 0.85, subtitle,
                ha="center", va="top",
                fontsize=11, color=INK_SOFT, style="italic",
                family=FONT_FAMILY)


def box(ax, x, y, w, h, label, *,
        kind="external", sublabel=None, fontsize=10, sub_fontsize=8.5,
        rounded=True):
    fill, border = PALETTE[kind]
    pad = 0.04
    rs = 0.18 if rounded else 0.04
    bbox = FancyBboxPatch(
        (x + pad, y + pad), w - 2 * pad, h - 2 * pad,
        boxstyle=f"round,pad={pad},rounding_size={rs}",
        facecolor=fill, edgecolor=border, linewidth=1.5,
    )
    ax.add_patch(bbox)
    cx = x + w / 2
    if sublabel:
        ax.text(cx, y + h * 0.62, label,
                ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=INK,
                family=FONT_FAMILY)
        ax.text(cx, y + h * 0.32, sublabel,
                ha="center", va="center",
                fontsize=sub_fontsize, color=INK_SOFT, style="italic",
                family=FONT_FAMILY,
                wrap=True)
    else:
        ax.text(cx, y + h / 2, label,
                ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=INK,
                family=FONT_FAMILY)


def cylinder(ax, x, y, w, h, label, *, sublabel=None):
    """A pseudo-cylinder for databases."""
    fill, border = PALETTE["db"]
    body = FancyBboxPatch(
        (x + 0.04, y + 0.08), w - 0.08, h - 0.20,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        facecolor=fill, edgecolor=border, linewidth=1.5,
    )
    ax.add_patch(body)
    top = Ellipse((x + w / 2, y + h - 0.14), w - 0.16, 0.22,
                  facecolor=fill, edgecolor=border, linewidth=1.5)
    bot = Ellipse((x + w / 2, y + 0.14), w - 0.16, 0.22,
                  facecolor=fill, edgecolor=border, linewidth=1.5)
    ax.add_patch(bot)
    ax.add_patch(top)
    cx = x + w / 2
    if sublabel:
        ax.text(cx, y + h * 0.58, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color=INK, family=FONT_FAMILY)
        ax.text(cx, y + h * 0.32, sublabel, ha="center", va="center",
                fontsize=8.5, color=INK_SOFT, style="italic", family=FONT_FAMILY)
    else:
        ax.text(cx, y + h * 0.5, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color=INK, family=FONT_FAMILY)


def boundary(ax, x, y, w, h, label):
    """A dashed boundary box around a logical group."""
    rect = Rectangle((x, y), w, h, fill=False,
                     edgecolor=INK_FAINT, linewidth=1.0, linestyle=(0, (4, 4)))
    ax.add_patch(rect)
    ax.text(x + 0.18, y + h - 0.22, label,
            ha="left", va="top",
            fontsize=10, fontweight="bold", color=INK_SOFT,
            family=FONT_FAMILY)


def arrow(ax, x1, y1, x2, y2, label=None, *,
          dashed=False, color=None, curve=0.0, fontsize=8.5,
          label_offset=(0, 0.0), label_bg=True):
    color = color or INK_SOFT
    ls = (0, (5, 4)) if dashed else "-"
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>",
        mutation_scale=14,
        color=color, linewidth=1.3, linestyle=ls,
        connectionstyle=f"arc3,rad={curve}",
        shrinkA=4, shrinkB=4,
    )
    ax.add_patch(a)
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        text_kwargs = dict(ha="center", va="center",
                           fontsize=fontsize, color=INK_SOFT,
                           family=FONT_FAMILY)
        if label_bg:
            text_kwargs["bbox"] = dict(facecolor=BG, edgecolor="none", pad=5)
        ax.text(mx, my, label, **text_kwargs)


# ============================================================================
# Diagram 1 — Level 1 / System Context
# ============================================================================

def render_context(out_path):
    W, H = 14, 8
    fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
    setup_ax(ax, W, H,
             title="C4 Level 1 — System Context",
             subtitle="The Couples App as a black box: who uses it, what external services it depends on")

    # Persons (left)
    box(ax, 0.6, 5.2, 2.6, 1.2, "Stef",
        kind="person", sublabel="Partner A — Android")
    box(ax, 0.6, 3.5, 2.6, 1.2, "Partner",
        kind="person", sublabel="Partner B — iOS")

    # System (centre)
    box(ax, 5.2, 4.2, 3.6, 1.6, "Couples App",
        kind="system_focus", sublabel="PWA — shared todos & household tasks",
        fontsize=12)

    # External services (right)
    box(ax, 10.8, 5.2, 2.8, 1.2, "Email provider",
        kind="external", sublabel="via Supabase Auth")
    box(ax, 10.8, 3.5, 2.8, 1.2, "Web Push service",
        kind="external", sublabel="future v2 (APNs / FCM)")

    # Arrows
    arrow(ax, 3.2, 5.8, 5.2, 5.4, "opens, manages todos",
          label_offset=(0, 0.18))
    arrow(ax, 3.2, 4.1, 5.2, 4.6, "opens, manages todos",
          label_offset=(0, -0.18))

    arrow(ax, 8.8, 5.4, 10.8, 5.8, "password reset emails",
          label_offset=(0, 0.18))
    arrow(ax, 8.8, 4.6, 10.8, 4.1, "notifications (v2)",
          dashed=True, label_offset=(0, -0.18))

    # Legend
    ax.text(0.4, 0.6, "Legend:", fontsize=9, color=INK, family=FONT_FAMILY,
            fontweight="bold")
    legend_items = [
        ("person", "Person"),
        ("system_focus", "System we own"),
        ("external", "External service"),
    ]
    lx = 1.6
    for key, lbl in legend_items:
        fill, border = PALETTE[key]
        ax.add_patch(Rectangle((lx, 0.4), 0.5, 0.4,
                               facecolor=fill, edgecolor=border, linewidth=1.0))
        ax.text(lx + 0.6, 0.6, lbl, fontsize=9, color=INK_SOFT,
                va="center", family=FONT_FAMILY)
        lx += 2.4

    fig.savefig(out_path, dpi=110, facecolor=BG)
    plt.close(fig)


# ============================================================================
# Diagram 2 — Level 2 / Containers
# ============================================================================

def render_container(out_path):
    W, H = 16, 10
    fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
    setup_ax(ax, W, H,
             title="C4 Level 2 — Containers (zoom into the Couples App)",
             subtitle="Open up the box from Level 1: the deployable units that make up the system, and how they communicate")

    # Three column boundaries
    boundary(ax, 0.5, 1.2, 4.4, 6.8, "User device  (phone or laptop)")
    boundary(ax, 5.6, 1.2, 4.4, 6.8, "Vercel edge")
    boundary(ax, 10.7, 1.2, 4.8, 6.8, "Supabase Cloud")

    # Device containers
    box(ax, 1.0, 5.6, 3.4, 1.4, "Next.js PWA",
        kind="container", sublabel="React 19 + Tailwind v4\ninstalled via Add to Home Screen")
    box(ax, 1.0, 3.4, 3.4, 1.4, "Service Worker",
        kind="container_alt", sublabel="offline shell + cached assets")

    # Vercel
    box(ax, 6.1, 4.6, 3.4, 1.6, "Next.js server",
        kind="container", sublabel="Server Components +\nServer Actions")

    # Supabase
    box(ax, 11.2, 6.0, 3.8, 1.2, "Supabase Auth",
        kind="container", sublabel="email + password")
    cylinder(ax, 11.2, 3.7, 3.8, 1.6, "Postgres",
             sublabel="Row-Level Security on every user-data table")
    box(ax, 11.2, 1.7, 3.8, 1.2, "Realtime",
        kind="container_alt", sublabel="websockets via logical replication")

    # Arrows — left to centre
    arrow(ax, 4.4, 6.3, 6.1, 5.6, "HTTPS",
          label_offset=(0, 0.15))
    arrow(ax, 6.1, 4.9, 4.4, 5.9, "httpOnly secure cookie",
          curve=0.15, label_offset=(0, -0.15))
    # SW caches PWA
    arrow(ax, 2.7, 4.8, 2.7, 5.6, "cache shell", dashed=True, fontsize=8,
          label_offset=(0.7, 0))

    # Centre to Supabase
    arrow(ax, 9.5, 5.7, 11.2, 6.4, "JWT verify",
          label_offset=(0, 0.15))
    arrow(ax, 9.5, 5.2, 11.2, 4.5, "SQL via supabase-js",
          curve=-0.05, label_offset=(0, 0.18))

    # Device direct to Realtime — routed below Postgres via a deep curve.
    # Label is placed near the curve apex (which sits well below the straight
    # midpoint with the negative curvature).
    arrow(ax, 4.4, 4.2, 11.2, 2.4, "WS subscribe",
          curve=-0.35, label_offset=(-0.6, -1.55))
    # Realtime <- DB (vertical, on the right side)
    arrow(ax, 14.4, 3.7, 14.4, 2.9, "logical\nreplication",
          fontsize=8, label_offset=(0.0, 0), label_bg=True)

    fig.savefig(out_path, dpi=110, facecolor=BG)
    plt.close(fig)


# ============================================================================
# Diagram 3 — Level 3 / Components inside Next.js app
# ============================================================================

def render_component(out_path):
    W, H = 16, 11
    fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
    setup_ax(ax, W, H,
             title="C4 Level 3 — Clean Architecture inside the Next.js application",
             subtitle="Zoom into the Next.js PWA + Next.js server containers from Level 2 (they share one codebase) · "
                      "four layers · dependencies always point inward (the dependency rule)")

    # Layer bands (back to front so labels render on top)
    layer_x = 0.7
    layer_w = 14.6
    layers = [
        # (y, h, name, kind)
        (8.0, 1.5, "Delivery / Infrastructure", "delivery"),
        (6.1, 1.5, "Interface Adapters",        "adapters"),
        (4.2, 1.5, "Application — use cases",   "application"),
        (2.3, 1.5, "Domain",                    "domain"),
    ]
    for y, h, name, kind in layers:
        fill, border = PALETTE[kind]
        rect = FancyBboxPatch(
            (layer_x, y), layer_w, h,
            boxstyle="round,pad=0.04,rounding_size=0.10",
            facecolor=fill, edgecolor=border, linewidth=1.4, alpha=0.55,
        )
        ax.add_patch(rect)
        ax.text(layer_x + 0.3, y + h - 0.25, name,
                fontsize=11, fontweight="bold", color=INK_SOFT,
                family=FONT_FAMILY)

    # Delivery layer components
    box(ax, 1.2, 8.25, 3.6, 1.0, "Server Components",
        kind="delivery", sublabel="app/.../page.tsx")
    box(ax, 5.4, 8.25, 3.6, 1.0, "Server Actions",
        kind="delivery", sublabel="features/*/adapters/actions.ts")
    box(ax, 9.6, 8.25, 3.6, 1.0, "Route Handlers",
        kind="delivery", sublabel="app/api/*")

    # Adapters layer
    box(ax, 1.2, 6.35, 3.0, 1.0, "Supabase repos",
        kind="adapters", sublabel="SupabaseTodoRepository, …")
    box(ax, 4.6, 6.35, 2.6, 1.0, "Zod validators",
        kind="adapters", sublabel="schema.ts")
    box(ax, 7.6, 6.35, 2.8, 1.0, "Supabase clients",
        kind="adapters", sublabel="server / browser")
    box(ax, 10.8, 6.35, 3.4, 1.0, "Composition root",
        kind="adapters", sublabel="composition.ts — wires everything")

    # Application layer
    box(ax, 1.2, 4.45, 6.6, 1.0, "Use cases",
        kind="application",
        sublabel="createTodo · toggleTodo · listTodos · signUp · pairCouple · redeemInvite")
    box(ax, 8.2, 4.45, 6.0, 1.0, "Repository interfaces",
        kind="application",
        sublabel="TodoRepository · UserRepository · CoupleRepository")

    # Domain layer
    box(ax, 1.2, 2.55, 6.6, 1.0, "Entities & value objects",
        kind="domain",
        sublabel="Todo · Couple · User · Email · branded ID types")
    box(ax, 8.2, 2.55, 6.0, 1.0, "Pure rules",
        kind="domain",
        sublabel="validateTitle · toggleStatus · markDone · domain errors")

    # Dependency arrows (always pointing INWARD = downward)
    arrow(ax, 3.0, 8.25, 3.0, 7.35, "uses", label_bg=True, fontsize=8.5)
    arrow(ax, 7.2, 8.25, 7.2, 7.35, "uses", label_bg=True, fontsize=8.5)
    arrow(ax, 11.4, 8.25, 11.4, 7.35, "uses", label_bg=True, fontsize=8.5)

    arrow(ax, 4.0, 6.35, 4.0, 5.45, "uses", label_bg=True, fontsize=8.5)
    arrow(ax, 12.5, 6.35, 11.0, 5.45, "uses", curve=0.05, label_bg=True, fontsize=8.5)

    arrow(ax, 4.0, 4.45, 4.0, 3.55, "uses", label_bg=True, fontsize=8.5)
    arrow(ax, 11.0, 4.45, 11.0, 3.55, "uses", label_bg=True, fontsize=8.5)

    # Implementation arrow — from adapter Repos UP to interface (dashed)
    arrow(ax, 2.6, 6.35, 8.4, 5.05, "implements",
          dashed=True, curve=-0.18,
          label_offset=(-0.5, 0.3), fontsize=8.5)

    # Side note — dependency rule
    note_x, note_y = 0.7, 0.5
    rect = FancyBboxPatch(
        (note_x, note_y), 14.6, 1.1,
        boxstyle="round,pad=0.05,rounding_size=0.08",
        facecolor="#FFF7ED", edgecolor="#9A3412", linewidth=1.0,
    )
    ax.add_patch(rect)
    ax.text(note_x + 0.3, note_y + 0.85,
            "The dependency rule",
            fontsize=11, fontweight="bold", color="#9A3412",
            family=FONT_FAMILY)
    ax.text(note_x + 0.3, note_y + 0.40,
            "infrastructure  →  adapters  →  application  →  domain      "
            "(always inward; an inner layer never imports from an outer one)",
            fontsize=10, color=INK, family=FONT_FAMILY)

    fig.savefig(out_path, dpi=110, facecolor=BG)
    plt.close(fig)


# ============================================================================
# Sequence diagram primitives
# ============================================================================

class Seq:
    """Minimal sequence-diagram drawer."""
    def __init__(self, ax, lifelines, *, top=8.5, lifeline_color=INK_FAINT,
                 box_w=2.1, box_h=0.85, default_gap=0.55):
        self.ax = ax
        self.top = top
        self.box_h = box_h
        self._default_gap = default_gap
        # Start sequence content BELOW the header boxes (with padding)
        self.cy = top - box_h - 0.45
        self.lifelines = lifelines  # list of (label, x, kind)
        # Draw header boxes + lifelines
        for label, x, kind in lifelines:
            fill, border = PALETTE[kind]
            head = FancyBboxPatch(
                (x - box_w / 2, top - box_h), box_w, box_h,
                boxstyle="round,pad=0.04,rounding_size=0.10",
                facecolor=fill, edgecolor=border, linewidth=1.3,
            )
            ax.add_patch(head)
            ax.text(x, top - box_h / 2, label, ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=INK,
                    family=FONT_FAMILY)
            # Lifeline (dashed vertical) starts below the header box
            ax.add_line(Line2D([x, x], [top - box_h - 0.05, 0.6],
                               linestyle=(0, (3, 4)),
                               color=lifeline_color, linewidth=1.0))
        self._note_color = "#FEF3C7"

    def _x_of(self, name):
        for label, x, _ in self.lifelines:
            if label == name:
                return x
        raise KeyError(name)

    def msg(self, src, dst, label, *, dashed=False, gap=None):
        if gap is None:
            gap = self._default_gap
        x1, x2 = self._x_of(src), self._x_of(dst)
        y = self.cy
        ls = (0, (5, 4)) if dashed else "-"
        a = FancyArrowPatch(
            (x1, y), (x2, y),
            arrowstyle="-|>",
            mutation_scale=12,
            color=INK_SOFT, linewidth=1.2, linestyle=ls,
            shrinkA=2, shrinkB=2,
        )
        self.ax.add_patch(a)
        # Label above the arrow line
        mx = (x1 + x2) / 2
        self.ax.text(mx, y + 0.16, label, ha="center", va="bottom",
                     fontsize=8.7, color=INK, family=FONT_FAMILY,
                     bbox=dict(facecolor=BG, edgecolor="none", pad=1.5))
        self.cy -= gap

    def selfmsg(self, who, label, gap=0.7, *, side="right"):
        x = self._x_of(who)
        y = self.cy
        sign = 1 if side == "right" else -1
        # small loop on the chosen side
        path_x = [x, x + sign * 0.55, x + sign * 0.55, x + sign * 0.05]
        path_y = [y, y, y - 0.32, y - 0.32]
        for i in range(len(path_x) - 1):
            line = Line2D([path_x[i], path_x[i+1]],
                          [path_y[i], path_y[i+1]],
                          color=INK_SOFT, linewidth=1.2)
            self.ax.add_line(line)
        # arrow head at end (very small)
        a = FancyArrowPatch(
            (x + sign * 0.10, y - 0.32), (x, y - 0.32),
            arrowstyle="-|>",
            mutation_scale=10, color=INK_SOFT, linewidth=1.2,
        )
        self.ax.add_patch(a)
        ha = "left" if side == "right" else "right"
        self.ax.text(x + sign * 0.65, y - 0.16, label, ha=ha, va="center",
                     fontsize=8.5, color=INK, family=FONT_FAMILY)
        self.cy -= gap

    def note(self, src, dst, label, *, gap=0.55, color=None):
        x1, x2 = sorted([self._x_of(src), self._x_of(dst)])
        y = self.cy
        h = 0.45
        rect = FancyBboxPatch(
            (x1 - 0.7, y - h / 2), (x2 - x1) + 1.4, h,
            boxstyle="round,pad=0.03,rounding_size=0.06",
            facecolor=color or self._note_color, edgecolor="#92400E", linewidth=1.0,
        )
        self.ax.add_patch(rect)
        self.ax.text((x1 + x2) / 2, y, label,
                     ha="center", va="center",
                     fontsize=9, color=INK, family=FONT_FAMILY,
                     fontstyle="italic")
        self.cy -= gap

    def gap(self, amount=0.35):
        self.cy -= amount


# ============================================================================
# Diagram 4 — Sequence: Signup
# ============================================================================

def render_seq_signup(out_path):
    W, H = 16, 11
    fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
    setup_ax(ax, W, H,
             title="Sequence — Signup",
             subtitle="Server Action → Use Case → Repository → Supabase Auth")

    lifelines = [
        ("User",        1.4,  "person"),
        ("Signup UI",   3.5,  "delivery"),
        ("signUpAction",5.8,  "delivery"),
        ("Zod schema",  8.0,  "adapters"),
        ("signUp UC",  10.2,  "application"),
        ("UserRepo",   12.4,  "adapters"),
        ("Supabase\nAuth + DB", 14.6, "container"),
    ]
    seq = Seq(ax, lifelines, top=9.6)

    seq.msg("User", "Signup UI", "enters email, password, name")
    seq.msg("Signup UI", "signUpAction", "submit (FormData)")
    seq.msg("signUpAction", "Zod schema", "parse(FormData)")
    seq.msg("Zod schema", "signUpAction", "SignUpInput (typed)", dashed=True)
    seq.msg("signUpAction", "signUp UC", "signUp({...})")
    seq.selfmsg("signUp UC", "domain validation\n(email format, password rules)")
    seq.msg("signUp UC", "UserRepo", "createWithCredentials(...)")
    seq.msg("UserRepo", "Supabase\nAuth + DB", "auth.signUp + insert profiles")
    seq.msg("Supabase\nAuth + DB", "UserRepo", "{ user, session }", dashed=True)
    seq.msg("UserRepo", "signUp UC", "User", dashed=True)
    seq.msg("signUp UC", "signUpAction", "User", dashed=True)
    seq.selfmsg("signUpAction", "set httpOnly + Secure cookie")
    seq.msg("signUpAction", "Signup UI", "redirect /onboarding", dashed=True)
    seq.msg("Signup UI", "User", "“check your email to confirm”", dashed=True)

    fig.savefig(out_path, dpi=110, facecolor=BG)
    plt.close(fig)


# ============================================================================
# Diagram 5 — Sequence: Couple pairing
# ============================================================================

def render_seq_pairing(out_path):
    W, H = 16, 14.5
    fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
    setup_ax(ax, W, H,
             title="Sequence — Couple pairing (invite + redeem)",
             subtitle="Two phases — A creates an invite code, B redeems it")

    lifelines = [
        ("Partner A",   1.5,  "person"),
        ("Partner B",   3.7,  "person"),
        ("App",         6.2,  "delivery"),
        ("pairCouple\nuse case",   9.2,  "application"),
        ("CoupleRepo", 12.0,  "adapters"),
        ("Postgres",   14.5,  "db"),
    ]
    seq = Seq(ax, lifelines, top=13.1, default_gap=0.46)

    seq.note("Partner A", "Postgres", "Phase 1 — A generates an invite",
             color="#FEF3C7")
    seq.msg("Partner A", "App", "tap “invite partner”")
    seq.msg("App", "pairCouple\nuse case", "createInvite(userId=A)")
    seq.msg("pairCouple\nuse case", "CoupleRepo", "createInvite(A)")
    seq.msg("CoupleRepo", "Postgres", "INSERT couple_invites")
    seq.msg("Postgres", "CoupleRepo", "invite row", dashed=True)
    seq.msg("CoupleRepo", "pairCouple\nuse case", "invite", dashed=True)
    seq.msg("pairCouple\nuse case", "App", "code “MOON-RIVER-42”", dashed=True)
    seq.msg("Partner A", "Partner B", "shares code (any channel)")

    seq.gap(0.15)
    seq.note("Partner B", "Postgres", "Phase 2 — B redeems",
             color="#DCFCE7")
    seq.msg("Partner B", "App", "enters “MOON-RIVER-42”")
    seq.msg("App", "pairCouple\nuse case", "redeemInvite(code, B)")
    seq.msg("pairCouple\nuse case", "CoupleRepo", "findInviteByCode(code)")
    seq.msg("CoupleRepo", "Postgres", "SELECT (not expired)")
    seq.msg("Postgres", "CoupleRepo", "invite (inviter=A)", dashed=True)
    seq.msg("CoupleRepo", "pairCouple\nuse case", "invite", dashed=True)
    seq.selfmsg("pairCouple\nuse case",
                "invariant: neither already paired", gap=0.65)
    seq.msg("pairCouple\nuse case", "CoupleRepo", "createCouple(A, B)")
    seq.msg("CoupleRepo", "Postgres",
            "TX: INSERT couples, DELETE invite")
    seq.msg("Postgres", "CoupleRepo", "couple", dashed=True)
    seq.msg("CoupleRepo", "pairCouple\nuse case", "couple", dashed=True)
    seq.msg("pairCouple\nuse case", "App", "paired ✓", dashed=True)

    fig.savefig(out_path, dpi=110, facecolor=BG)
    plt.close(fig)


# ============================================================================
# Diagram 6 — Sequence: Create todo + realtime fan-out
# ============================================================================

def render_seq_todo(out_path):
    W, H = 16, 10.5
    fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
    setup_ax(ax, W, H,
             title="Sequence — Create todo with realtime fan-out",
             subtitle="A creates a todo; B sees it via Realtime within ~1 second")

    lifelines = [
        ("Partner A",       1.2,  "person"),
        ("A's app",         3.1,  "delivery"),
        ("createTodo\nAction", 5.3, "delivery"),
        ("createTodo\nUC",  7.6,  "application"),
        ("TodoRepo",        9.7,  "adapters"),
        ("Postgres",       11.6,  "db"),
        ("Realtime",       13.3,  "container_alt"),
        ("B's app",        14.9,  "delivery"),
    ]
    seq = Seq(ax, lifelines, top=9.2, box_w=1.85)

    seq.msg("Partner A", "A's app", "type “buy oat milk”, ↵")
    seq.msg("A's app", "createTodo\nAction", "form submit")
    seq.selfmsg("createTodo\nAction", "Zod parse(FormData)")
    seq.msg("createTodo\nAction", "createTodo\nUC", "createTodo(input)")
    seq.selfmsg("createTodo\nUC", "domain validation\n(title 1–200 chars)")
    seq.msg("createTodo\nUC", "TodoRepo", "create(todo)")
    seq.msg("TodoRepo", "Postgres", "INSERT (RLS: own couple)")
    seq.msg("Postgres", "TodoRepo", "row", dashed=True)
    seq.msg("TodoRepo", "createTodo\nUC", "Todo", dashed=True)
    seq.msg("createTodo\nUC", "createTodo\nAction", "Todo", dashed=True)
    seq.selfmsg("createTodo\nAction", "revalidatePath('/todos')")

    seq.gap(0.2)
    seq.note("Postgres", "B's app", "Realtime fan-out (parallel)",
             color="#DBEAFE")
    seq.msg("Postgres", "Realtime", "logical replication: INSERT todos")
    seq.msg("Realtime", "B's app", "WS message — INSERT todos for couple")
    seq.selfmsg("B's app", "append to local list (optimistic UI)", side="left")

    fig.savefig(out_path, dpi=110, facecolor=BG)
    plt.close(fig)


# ============================================================================
# Main
# ============================================================================

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    targets = [
        ("1_context.png",      render_context),
        ("2_container.png",    render_container),
        ("3_component.png",    render_component),
        ("4_seq_signup.png",   render_seq_signup),
        ("5_seq_pairing.png",  render_seq_pairing),
        ("6_seq_todo.png",     render_seq_todo),
    ]
    for name, fn in targets:
        path = os.path.join(here, name)
        fn(path)
        print(f"  ✓  {name}")
    print(f"\nDone. {len(targets)} diagrams written to {here}")


if __name__ == "__main__":
    main()
g",  render_seq_pairing),
        ("6_seq_todo.png",     render_seq_todo),
    ]
    for name, fn in targets:
        path = os.path.join(here, name)
        fn(path)
        print(f"  ok  {name}")
    print(f"\nDone. {len(targets)} diagrams written to {here}")


if __name__ == "__main__":
    main()
_todo),
    ]
    for name, fn in targets:
        path = os.path.join(here, name)
        fn(path)
        print(f"  ok  {name}")
    print(f"\nDone. {len(targets)} diagrams written to {here}")


if __name__ == "__main__":
    main()
    main()
