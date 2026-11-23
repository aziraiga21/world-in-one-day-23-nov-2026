#!/usr/bin/env python3
"""news-image-20261123 entry: one 1024x1024 Pillow newspaper front page, 35 stories.

Deterministic: no random, no timestamps, no network. Every text block is
measured with font.getlength and wrapped / shrunk until it fits its box.
Layout is adaptive: tightness levels shrink decorative heights and type until
the whole page fits 1024px; the first level that fits is used.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
CW = W - 2 * MARGIN  # 976
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (158, 43, 37)
NAVY = (31, 53, 82)
NAVY_BLACK = (18, 28, 44)
GREY = (96, 96, 96)
SEA = (220, 232, 238)
LAND = (232, 217, 168)
LAND_LINE = (120, 105, 70)
WHITE = (255, 255, 255)
PANEL_LINE = (70, 70, 70)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
# NOTE: DejaVuSerif-Italic.ttf is listed in the brief but is NOT installed
# on this machine (dejavu dir holds only Serif, Serif-Bold, Sans, Sans-Bold,
# SansMono variants). Substitute: Liberation Serif Italic (true serif italic).
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, max(1, int(round(size))))


def wrap(text, font, max_w):
    """Greedy word wrap by measured width. Returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, path, size, max_w, max_lines, min_size):
    """Shrink font until text wraps to <= max_lines. Returns (font, lines)."""
    s = size
    while s > min_size:
        f = F(path, s)
        lines = wrap(text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        s -= 0.5
    f = F(path, min_size)
    return f, wrap(text, f, max_w)


def draw_ls(d, x, y, text, font, fill, tracking=2):
    """Draw letterspaced text, return total width."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += font.getlength(ch) + tracking
    return cx - x - tracking


def text_h(font):
    return font.getbbox("Ay")[3] - font.getbbox("Ay")[1]


# ---------------------------------------------------------------- content
EYEBROW_L = "THE WORLD IN ONE DAY"
EYEBROW_R = "35 STORIES \u00b7 6 REGIONS \u00b7 ALL FROM THIS ONE DAY"
MASTHEAD = "Monday 23 November 2026"
STAND = ("Iran readies tankers to break the blockade \u00b7 COP31 collapses in "
         "Antalya \u00b7 Zelensky counts 109 bridge strikes")

REGIONS = [("MIDDLE EAST", 5, (158, 43, 37)), ("EUROPE", 7, (31, 53, 82)),
           ("AMERICAS", 6, (46, 107, 52)), ("ASIA", 9, (176, 118, 28)),
           ("AFRICA", 3, (122, 74, 33)), ("GLOBAL", 5, (91, 91, 91))]

STATS = [("14+", "Iranian tankers massed off Kharg to test the blockade"),
         ("\u22123.7%", "S&P 500's Friday fall to 6,910"),
         ("\u221214%", "Nvidia's Friday plunge"),
         ("$450m", "Mets' Skubal deal, richest pitcher contract"),
         ("109", "bridge strikes counted by Zelensky"),
         ("24", "body bags recovered at the Cikande factory fire")]

HEROES = [
    {"kicker": "1 \u00b7 HORMUZ \u00b7 GULF WAR",
     "headline": "Iran readies tankers to break the US blockade",
     "deck": ("14+ tankers mass off Kharg as Tehran calls the blockade "
              "'an act of war'; Trump dares Iran to test it: 'bottom of the sea'."),
     "source": "\u2014 Al Jazeera \u00b7 Reuters \u00b7 Fox",
     "scene": "gulf"},
    {"kicker": "2 \u00b7 ANTALYA \u00b7 CLIMATE",
     "headline": "COP31 collapses in Antalya",
     "deck": ("EU and others reject the Antalya Pact; the longest COP ends with "
              "no deal \u2014 first failure since Copenhagen 2009."),
     "source": "\u2014 CNN \u00b7 UN News \u00b7 Le Monde",
     "scene": "cop"},
    {"kicker": "3 \u00b7 KYIV \u00b7 BRIDGES \u00b7 WAR",
     "headline": "Zelensky: Russia hit bridges 109 times",
     "deck": ("Kyiv counts 109 bridge strikes before its retaliation; a Russian "
              "drone hits a Kyiv-region block, 2 dead, 11 missing."),
     "source": "\u2014 Wires \u00b7 Reuters",
     "scene": "bridge"},
]

TILES = [
    {"kicker": "4 \u00b7 BENGHAZI \u00b7 WAR",
     "headline": "Ukrainian drones hit Russian corvette in Libya",
     "deck": "Merkury severely damaged, capsizes; 10 hurt.", "scene": "warship"},
    {"kicker": "5 \u00b7 WARSAW \u00b7 WAR",
     "headline": "Poland: fallen objects were Russian missiles",
     "deck": "Three objects confirmed cruise missiles; NATO to meet.",
     "scene": "missile"},
    {"kicker": "6 \u00b7 GAZA \u00b7 WAR",
     "headline": "Israeli strike kills 3 Gaza aid staff",
     "deck": "Four hurt; Hamas seeks urgent talks.", "scene": "truck"},
    {"kicker": "7 \u00b7 NIGERIA \u00b7 DISASTER",
     "headline": "Boat sinks on way to a funeral",
     "deck": "At least 24 killed; captain flees.", "scene": "river"},
    {"kicker": "8 \u00b7 TAIPEI \u00b7 MARKETS",
     "headline": "Taiwan bans short sales as shares slump",
     "deck": "Stocks down 17.5% in a week.", "scene": "chart"},
    {"kicker": "9 \u00b7 LISBON \u00b7 PROTEST",
     "headline": "Thousands march as living costs fuel anger",
     "deck": "Cost-of-living protests spread.", "scene": "crowd"},
    {"kicker": "10 \u00b7 SEOUL \u00b7 POLITICS",
     "headline": "Education minister resigns over exam changes",
     "deck": "Suneung rule shift takes the blame.", "scene": "gov"},
    {"kicker": "11 \u00b7 RIYADH \u00b7 WAR",
     "headline": "Saudi intercepts Houthi drone and missile",
     "deck": "Attack aimed at the south stopped.", "scene": "skyline"},
    {"kicker": "12 \u00b7 LONDON \u00b7 DEFENCE",
     "headline": "UK to build long-range drones for Ukraine at home",
     "deck": "New UAV production in Britain.", "scene": "drone"},
    {"kicker": "13 \u00b7 NEW YORK \u00b7 SPORT",
     "headline": "Mets agree $450m Skubal deal",
     "deck": "Richest pitcher contract ever.", "scene": "baseball"},
]

BRIEFS = [
    "14 KHARTOUM \u2014 Drone strikes damage a UN facility; 3 killed in Omdurman. Wires",
    "15 RAMALLAH \u2014 Settlers torch 12 vehicles in 4 villages; Eisenkot calls it \u201cterrorism by Jews\u201d. Wires",
    "16 CIKANDE \u2014 Search resumes Monday at the candy-factory fire; 24 body bags found Sunday. AP",
    "17 OKINAWA \u2014 Shuri Castle main hall reopens, 7 years after the fire. AP",
    "18 FINLAND \u2014 Russian cargo ship still burning off Finland; towing begins. Wires",
    "19 YANGON \u2014 Myanmar calls the ASEAN decision \u201bunfair and imbalanced\u201d. Wires",
    "20 LONDON \u2014 NHS: 31 trusts warn hospitals face \u201cunpalatable\u201d cuts. Guardian",
    "21 WASHINGTON \u2014 Trump: no rush to strike Iran again, as hawks urge action. SimpleLife",
    "22 HORMUZ \u2014 Two supertankers hit mines Sunday and catch fire. Anadolu",
    "23 NEW YORK \u2014 Asian markets on alert after Wall Street's Friday plunge. Reuters",
    "24 GOLD \u2014 Gold rebounds ~2% to $3,582 after a 9% weekly fall to a 14-month low. TradingView",
    "25 TAIPEI \u2014 Export orders extend a 21-month rise. SimpleLife",
    "26 ANTALYA \u2014 90+ nations sign an electrification pledge amid the collapse. CNN",
    "27 ADDIS ABABA \u2014 Focus shifts to COP32 in Addis Ababa. UN News",
    "28 WASHINGTON \u2014 Trump: working with Schumer \u201cwould be difficult\u201d. SimpleLife",
    "29 TAIPEI \u2014 TWSE weighs cutting the margin ratio to 120%. SimpleLife",
    "30 TALLINN \u2014 RIA Novosti claims Estonia \u201ccollapsing\u201d over the border closure. Wires",
    "31 WASHINGTON \u2014 Incoming Speaker Jeffries backs penalties for violent settlers. Wires",
    "32 NEW DELHI \u2014 JEE Main 2027 session 1 registration closes today. JagranJosh",
    "33 NEW YORK \u2014 Nvidia plunges 14% in Friday's tech sell-off. Capitallytics",
    "34 SEOUL \u2014 South Korea readies a stock stabilisation fund. Yonhap",
    "35 BITCOIN \u2014 Bitcoin steadies near $61,000 after sliding to $55,150 Saturday. Coinbell",
]

FOOTER = ("DATE CHECK \u2713 Every story on this page happened, or was first "
          "reported, on Monday 23 November 2026. REPORTED MONDAY, HAPPENED "
          "SUNDAY: the COP31 collapse (decided late Sunday, reported across "
          "Monday wires), the Benghazi corvette strike, the Dymer block hit. "
          "LEFT OUT AS EARLIER NEWS: the ATP Finals result (Alcaraz beat "
          "Zverev, Sunday), Marquez's eighth MotoGP title (Sunday), the Hong "
          "Kong Election Committee vote (Sunday), India's 720/9 (Sunday), "
          "BepiColombo's Mercury orbit (21 Nov), Nvidia's CEO stepping down "
          "(12 Nov).")

CREDIT = ("Claims are attributed, not stated as fact \u00b7 Pictures and map: "
          "original, drawn in code \u00b7 Sources: Al Jazeera, CNN, Le Monde, "
          "UN News, Reuters, AP, AFP, BBC, Fox Business, BusinessWorld, "
          "TradingView, SignaLetter \u00b7 2026-11-23")

CONTINENTS = {
    "North America": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                      (-85, 66), (-75, 62), (-65, 60), (-55, 52), (-60, 45),
                      (-70, 42), (-75, 35), (-80, 25), (-85, 30), (-95, 20),
                      (-105, 20), (-110, 25), (-120, 35), (-125, 48),
                      (-140, 60), (-155, 58), (-165, 60)],
    "South America": [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5),
                      (-40, -10), (-35, -15), (-40, -25), (-50, -30),
                      (-60, -35), (-70, -40), (-75, -50), (-70, -55),
                      (-75, -35), (-80, -20), (-80, -5)],
    "Africa": [(-10, 35), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
               (40, 20), (45, 12), (50, 10), (45, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -30), (10, -15), (5, 0), (0, 5),
               (-10, 10), (-15, 25)],
    "Europe": [(-10, 36), (-5, 40), (0, 43), (5, 45), (10, 55), (15, 58),
               (20, 60), (25, 65), (30, 70), (35, 68), (30, 60), (25, 55),
               (20, 50), (15, 45), (10, 40), (5, 38), (0, 36)],
    "Asia": [(35, 70), (50, 72), (70, 73), (90, 75), (110, 76), (130, 72),
             (150, 70), (170, 66), (160, 60), (150, 55), (140, 45), (130, 40),
             (120, 35), (110, 25), (100, 20), (95, 10), (90, 5), (85, 15),
             (80, 20), (75, 25), (70, 30), (60, 30), (55, 25), (50, 30),
             (45, 35), (40, 40), (35, 45), (35, 55), (40, 60)],
    "Australia": [(113, -22), (120, -15), (130, -12), (140, -17), (145, -15),
                  (150, -22), (150, -30), (145, -38), (140, -38), (130, -32),
                  (120, -35), (113, -30)],
}

# (number, lon, lat) — positions nudged so neighbours do not overlap.
DOTS = [(1, 58, 24), (2, 28, 38), (3, 33, 52), (4, 20, 32), (5, 17, 53),
        (6, 35, 32), (7, 7, 9), (8, 121, 25), (9, -9, 39), (10, 127, 37),
        (11, 45, 24), (12, -4, 54), (13, -73, 41), (14, 32, 16),
        (16, 107, -6), (17, 131, 27), (18, 22, 61), (19, 96, 16),
        (21, -82, 36), (27, 38, 9), (30, 31, 64), (32, 77, 28)]

# ---------------------------------------------------------------- banners
def _sky(d, box, top, bot):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def paint_banner(d, box, scene):
    """Small procedural illustration inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if scene == "warship":
        _sky(d, box, (24, 38, 66), (58, 84, 120))
        d.rectangle([x0, y0 + h * 0.62, x1, y1], fill=(30, 56, 90))
        d.polygon([(x0 + w * 0.18, y0 + h * 0.62), (x0 + w * 0.82, y0 + h * 0.55),
                   (x0 + w * 0.78, y0 + h * 0.72), (x0 + w * 0.24, y0 + h * 0.75)],
                  fill=(92, 98, 112))
        d.rectangle([x0 + w * 0.45, y0 + h * 0.30, x0 + w * 0.48, y0 + h * 0.58],
                    fill=(92, 98, 112))
        d.rectangle([x0 + w * 0.60, y0 + h * 0.42, x0 + w * 0.68, y0 + h * 0.58],
                    fill=(200, 205, 215))
        for wx in (0.32, 0.42, 0.52):
            d.rectangle([x0 + w * wx, y0 + h * 0.63, x0 + w * wx + 4,
                         y0 + h * 0.63 + 3], fill=(250, 220, 120))
        for sx in (0.25, 0.55, 0.8):
            d.ellipse([x0 + w * sx, y0 + h * 0.80, x0 + w * sx + 5, y0 + h * 0.80 + 3],
                      fill=(180, 190, 205))
    elif scene == "missile":
        _sky(d, box, (214, 222, 228), (238, 236, 228))
        d.ellipse([x0 + w * 0.72, y0 + h * 0.30, x0 + w * 0.86, y0 + h * 0.62],
                  fill=(158, 43, 37))
        d.ellipse([x0 + w * 0.76, y0 + h * 0.38, x0 + w * 0.82, y0 + h * 0.54],
                  fill=(247, 243, 232))
        d.line([(x0 + w * 0.15, y0 + h * 0.80), (x0 + w * 0.62, y0 + h * 0.30)],
               fill=(70, 70, 70), width=3)
        d.polygon([(x0 + w * 0.62, y0 + h * 0.30), (x0 + w * 0.70, y0 + h * 0.24),
                   (x0 + w * 0.68, y0 + h * 0.36)], fill=(70, 70, 70))
        d.line([(x0 + w * 0.15, y0 + h * 0.80), (x0 + w * 0.30, y0 + h * 0.68)],
               fill=(180, 180, 180), width=2)
    elif scene == "truck":
        _sky(d, box, (168, 172, 176), (205, 205, 200))
        d.rectangle([x0, y0 + h * 0.70, x1, y1], fill=(96, 90, 80))
        d.rectangle([x0 + w * 0.08, y0 + h * 0.26, x0 + w * 0.56, y0 + h * 0.70],
                    fill=(232, 228, 218))
        d.rectangle([x0 + w * 0.58, y0 + h * 0.38, x0 + w * 0.82, y0 + h * 0.70],
                    fill=(158, 43, 37))
        d.rectangle([x0 + w * 0.61, y0 + h * 0.42, x0 + w * 0.71, y0 + h * 0.54],
                    fill=(200, 220, 230))
        for cx in (0.24, 0.66):
            d.ellipse([x0 + w * cx, y0 + h * 0.68, x0 + w * cx + 9, y0 + h * 0.68 + 9],
                      fill=(30, 30, 30))
    elif scene == "river":
        _sky(d, box, (150, 190, 210), (190, 215, 225))
        d.rectangle([x0, y0 + h * 0.55, x1, y1], fill=(52, 96, 128))
        d.polygon([(x0 + w * 0.25, y0 + h * 0.62), (x0 + w * 0.75, y0 + h * 0.55),
                   (x0 + w * 0.70, y0 + h * 0.72), (x0 + w * 0.30, y0 + h * 0.75)],
                  fill=(120, 70, 40))
        d.line([(x0 + w * 0.30, y0 + h * 0.58), (x0 + w * 0.45, y0 + h * 0.30)],
               fill=(90, 60, 30), width=2)
        for sx, sy in ((0.55, 0.82), (0.70, 0.86), (0.40, 0.88)):
            d.ellipse([x0 + w * sx, y0 + h * sy, x0 + w * sx + 4, y0 + h * sy + 3],
                      fill=(230, 235, 240))
    elif scene == "chart":
        d.rectangle(box, fill=(250, 248, 240))
        d.line([(x0 + 8, y0 + h - 6), (x1 - 6, y0 + h - 6)], fill=(150, 150, 150))
        d.line([(x0 + 8, y0 + 5), (x0 + 8, y0 + h - 6)], fill=(150, 150, 150))
        pts = [(x0 + 12 + i * (w - 22) / 6, y0 + 8 + (i * i) * h / 48)
               for i in range(7)]
        d.line(pts, fill=(158, 43, 37), width=2)
        d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3],
                  fill=(158, 43, 37))
    elif scene == "crowd":
        _sky(d, box, (228, 220, 200), (240, 236, 224))
        for i, cx in enumerate((0.14, 0.30, 0.46, 0.62, 0.78, 0.92)):
            d.ellipse([x0 + w * cx - 5, y0 + h * 0.42, x0 + w * cx + 5,
                       y0 + h * 0.42 + 10], fill=(60, 50, 40))
            d.rectangle([x0 + w * cx - 8, y0 + h * 0.66, x0 + w * cx + 8, y1],
                        fill=((31, 53, 82) if i % 2 else (158, 43, 37)))
        d.rectangle([x0 + w * 0.08, y0 + h * 0.16, x0 + w * 0.42, y0 + h * 0.34],
                    fill=(247, 243, 232), outline=(120, 100, 60))
        d.rectangle([x0 + w * 0.58, y0 + h * 0.20, x0 + w * 0.92, y0 + h * 0.38],
                    fill=(247, 243, 232), outline=(120, 100, 60))
    elif scene == "gov":
        _sky(d, box, (200, 214, 226), (232, 230, 222))
        d.rectangle([x0 + w * 0.20, y0 + h * 0.42, x0 + w * 0.80, y0 + h * 0.88],
                    fill=(210, 200, 170))
        d.polygon([(x0 + w * 0.16, y0 + h * 0.42), (x0 + w * 0.50, y0 + h * 0.18),
                   (x0 + w * 0.84, y0 + h * 0.42)], fill=(170, 50, 40))
        for cx in (0.28, 0.42, 0.56, 0.70):
            d.rectangle([x0 + w * cx - 3, y0 + h * 0.48, x0 + w * cx + 3,
                         y0 + h * 0.88], fill=(247, 243, 232))
        d.line([(x0 + w * 0.88, y0 + h * 0.12), (x0 + w * 0.88, y0 + h * 0.48)],
               fill=(70, 70, 70), width=2)
        d.polygon([(x0 + w * 0.88, y0 + h * 0.12), (x0 + w * 0.99, y0 + h * 0.19),
                   (x0 + w * 0.88, y0 + h * 0.26)], fill=(31, 53, 82))
    elif scene == "skyline":
        _sky(d, box, (16, 24, 44), (44, 58, 88))
        for i, (bx, bw, bh) in enumerate(((0.05, 0.14, 0.55), (0.24, 0.12, 0.70),
                                          (0.42, 0.16, 0.48), (0.62, 0.12, 0.66),
                                          (0.80, 0.15, 0.52))):
            d.rectangle([x0 + w * bx, y1 - h * bh, x0 + w * (bx + bw), y1],
                        fill=(24, 32, 52))
            for wy in range(3):
                d.rectangle([x0 + w * (bx + 0.03), y1 - h * bh + 4 + wy * 8,
                             x0 + w * (bx + 0.06), y1 - h * bh + 8 + wy * 8],
                            fill=(240, 200, 90))
        for cx, cy in ((0.30, 0.25), (0.68, 0.18)):
            for a in range(8):
                ang = a * math.pi / 4
                d.line([(x0 + w * cx, y0 + h * cy),
                        (x0 + w * cx + 10 * math.cos(ang),
                         y0 + h * cy + 10 * math.sin(ang))],
                       fill=(250, 220, 120), width=1)
            d.ellipse([x0 + w * cx - 3, y0 + h * cy - 3, x0 + w * cx + 3,
                       y0 + h * cy + 3], fill=(250, 220, 120))
    elif scene == "drone":
        _sky(d, box, (210, 218, 226), (238, 236, 230))
        d.rectangle([x0, y0 + h * 0.72, x1, y1], fill=(120, 112, 100))
        d.polygon([(x0 + w * 0.06, y0 + h * 0.72), (x0 + w * 0.16, y0 + h * 0.58),
                   (x0 + w * 0.30, y0 + h * 0.72)], fill=(90, 84, 76))
        d.polygon([(x0 + w * 0.34, y0 + h * 0.72), (x0 + w * 0.44, y0 + h * 0.58),
                   (x0 + w * 0.58, y0 + h * 0.72)], fill=(90, 84, 76))
        d.rectangle([x0 + w * 0.62, y0 + h * 0.60, x0 + w * 0.76, y0 + h * 0.72],
                    fill=(90, 84, 76))
        d.ellipse([x0 + w * 0.42, y0 + h * 0.20, x0 + w * 0.58, y0 + h * 0.36],
                  fill=(20, 20, 24))
        for cx in (0.34, 0.66):
            d.line([(x0 + w * (cx - 0.12), y0 + h * 0.28),
                    (x0 + w * (cx + 0.12), y0 + h * 0.28)], fill=(20, 20, 24),
                   width=2)
            d.line([(x0 + w * cx, y0 + h * 0.28), (x0 + w * 0.50, y0 + h * 0.30)],
                   fill=(20, 20, 24), width=1)
    elif scene == "baseball":
        d.rectangle(box, fill=(250, 248, 240))
        cx, cy, r = x0 + w * 0.30, y0 + h * 0.52, min(w, h) * 0.34
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                  outline=(180, 60, 50), width=2)
        for a in (-50, -20, 10, 40):
            ang = math.radians(a)
            d.arc([cx - r, cy - r, cx + r, cy + r], a, a + 55,
                  fill=(180, 60, 50), width=2)
        f = F(SANS_B, 13)
        d.text((x0 + w * 0.58, y0 + h * 0.42), "$450m", font=f, fill=RED)
    elif scene == "gulf":
        _sky(d, box, (12, 20, 40), (30, 48, 78))
        for sx, sy in ((0.12, 0.20), (0.30, 0.12), (0.55, 0.22), (0.78, 0.14),
                       (0.92, 0.26)):
            d.ellipse([x0 + w * sx, y0 + h * sy, x0 + w * sx + 2, y0 + h * sy + 2],
                      fill=(230, 230, 240))
        d.rectangle([x0, y0 + h * 0.58, x1, y1], fill=(10, 26, 48))
        for tx in (0.10, 0.34, 0.58):
            d.rectangle([x0 + w * tx, y0 + h * 0.52, x0 + w * (tx + 0.16),
                         y0 + h * 0.66], fill=(24, 28, 34))
            d.rectangle([x0 + w * (tx + 0.05), y0 + h * 0.44,
                         x0 + w * (tx + 0.08), y0 + h * 0.52], fill=(24, 28, 34))
            d.ellipse([x0 + w * (tx + 0.02), y0 + h * 0.66, x0 + w * (tx + 0.05),
                       y0 + h * 0.68], fill=(200, 210, 225))
        d.polygon([(x0 + w * 0.80, y0 + h * 0.62), (x0 + w * 0.94, y0 + h * 0.62),
                   (x0 + w * 0.90, y0 + h * 0.70), (x0 + w * 0.84, y0 + h * 0.70)],
                  fill=(8, 12, 20))
        d.rectangle([x0 + w * 0.86, y0 + h * 0.50, x0 + w * 0.88, y0 + h * 0.62],
                    fill=(8, 12, 20))
        for mx, my in ((0.22, 0.30), (0.48, 0.22), (0.70, 0.32)):
            d.line([(x0 + w * mx, y0 + h * my), (x0 + w * (mx + 0.10),
                     y0 + h * (my - 0.14))], fill=(250, 200, 110), width=2)
            d.ellipse([x0 + w * (mx + 0.10) - 2, y0 + h * (my - 0.14) - 2,
                       x0 + w * (mx + 0.10) + 2, y0 + h * (my - 0.14) + 2],
                      fill=(250, 220, 140))
    elif scene == "cop":
        _sky(d, box, (216, 206, 182), (238, 232, 214))
        d.ellipse([x0 + w * 0.10, y0 + h * 0.18, x0 + w * 0.38, y0 + h * 0.82],
                  fill=(90, 140, 170), outline=(31, 53, 82), width=2)
        d.ellipse([x0 + w * 0.20, y0 + h * 0.28, x0 + w * 0.28, y0 + h * 0.44],
                  fill=(90, 160, 100))
        d.ellipse([x0 + w * 0.16, y0 + h * 0.55, x0 + w * 0.30, y0 + h * 0.72],
                  fill=(90, 160, 100))
        d.rectangle([x0 + w * 0.48, y0 + h * 0.30, x0 + w * 0.88, y0 + h * 0.78],
                    fill=(255, 255, 255), outline=(120, 120, 120))
        d.line([(x0 + w * 0.48, y0 + h * 0.54), (x0 + w * 0.88, y0 + h * 0.54)],
               fill=(158, 43, 37), width=2)
        d.line([(x0 + w * 0.52, y0 + h * 0.36), (x0 + w * 0.84, y0 + h * 0.36)],
               fill=(150, 150, 150), width=2)
        d.line([(x0 + w * 0.52, y0 + h * 0.44), (x0 + w * 0.84, y0 + h * 0.44)],
               fill=(150, 150, 150), width=2)
        d.line([(x0 + w * 0.52, y0 + h * 0.64), (x0 + w * 0.84, y0 + h * 0.64)],
               fill=(150, 150, 150), width=2)
        d.line([(x0 + w * 0.52, y0 + h * 0.72), (x0 + w * 0.76, y0 + h * 0.72)],
               fill=(150, 150, 150), width=2)
        f = F(SANS_B, 11)
        d.text((x0 + w * 0.50, y0 + h * 0.10), "OVERTIME", font=f, fill=RED)
        d.line([(x0 + w * 0.49, y0 + h * 0.09), (x0 + w * 0.68, y0 + h * 0.24)],
               fill=RED, width=2)
        d.line([(x0 + w * 0.68, y0 + h * 0.09), (x0 + w * 0.49, y0 + h * 0.24)],
               fill=RED, width=2)
    elif scene == "bridge":
        _sky(d, box, (170, 196, 216), (214, 226, 232))
        for i, (bx, bw, bh) in enumerate(((0.04, 0.10, 0.42), (0.18, 0.08, 0.55),
                                          (0.80, 0.09, 0.48), (0.92, 0.06, 0.38))):
            d.rectangle([x0 + w * bx, y0 + h * (0.92 - bh), x0 + w * (bx + bw),
                         y0 + h * 0.92], fill=(120, 128, 140))
        d.rectangle([x0, y0 + h * 0.78, x1, y1], fill=(70, 110, 140))
        d.rectangle([x0, y0 + h * 0.60, x0 + w * 0.42, y0 + h * 0.66],
                    fill=(90, 80, 70))
        d.polygon([(x0 + w * 0.58, y0 + h * 0.60), (x0 + w * 0.66, y0 + h * 0.68),
                   (x0 + w * 0.72, y0 + h * 0.60), (x0 + w * 0.64, y0 + h * 0.55)],
                  fill=(90, 80, 70))
        d.rectangle([x0 + w * 0.72, y0 + h * 0.60, x1, y0 + h * 0.66],
                    fill=(90, 80, 70))
        for tx in (0.30, 0.50, 0.70):
            d.rectangle([x0 + w * tx, y0 + h * 0.34, x0 + w * tx + 3,
                         y0 + h * 0.60], fill=(70, 62, 54))
        for cx, cy, r in ((0.60, 0.50, 10), (0.65, 0.44, 8), (0.55, 0.47, 6)):
            d.ellipse([x0 + w * cx - r, y0 + h * cy - r, x0 + w * cx + r,
                       y0 + h * cy + r], fill=(150, 150, 150))
    else:
        d.rectangle(box, fill=(220, 214, 196))


# ---------------------------------------------------------------- map
def project(lon, lat, mx, my, mw, mh):
    return mx + (lon + 180.0) / 360.0 * mw, my + (90.0 - lat) / 180.0 * mh


def draw_map(d, box):
    """World map panel. Returns (min_dot_distance, dot_count)."""
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    mw = min(pw, int(ph * 2))
    mh = mw // 2
    mx = x0 + (pw - mw) // 2
    my = y0 + (ph - mh) // 2
    d.rectangle(box, fill=SEA)
    for poly in CONTINENTS.values():
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # dot positions with min-distance self-check (nudge less-central dot)
    pts = []
    for num, lon, lat in DOTS:
        px, py = project(lon, lat, mx, my, mw, mh)
        pts.append([num, px, py])
    cx0, cy0 = mx + mw / 2, my + mh / 2
    for _ in range(30):
        worst, worst_d = None, 10.0
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[i][1] - pts[j][1]
                dy = pts[i][2] - pts[j][2]
                dist = math.hypot(dx, dy)
                if dist < worst_d:
                    worst, worst_d = (i, j), dist
        if worst is None:
            break
        i, j = worst
        di = math.hypot(pts[i][1] - cx0, pts[i][2] - cy0)
        dj = math.hypot(pts[j][1] - cx0, pts[j][2] - cy0)
        k = i if di > dj else j
        o = j if k == i else i
        dx = pts[k][1] - pts[o][1]
        dy = pts[k][2] - pts[o][2]
        n = math.hypot(dx, dy) or 1.0
        push = (10.0 - worst_d) + 1.0
        pts[k][1] += dx / n * push
        pts[k][2] += dy / n * push
    mind = 1e9
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            mind = min(mind, math.hypot(pts[i][1] - pts[j][1],
                                        pts[i][2] - pts[j][2]))
    assert mind >= 10.0, "map dots too close: %.2f" % mind
    for num, px, py in pts:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255))
        fs = 7 if num < 10 else 6
        f = F(SANS_B, fs)
        tw = f.getlength(str(num))
        d.text((px - tw / 2, py - fs / 2 - 1), str(num), font=f, fill=WHITE)
    return mind, len(pts)


# ---------------------------------------------------------------- layout
LEVELS = [
    # mast, stand, stat_num, stat_lab, hero_banner, hero_head, hero_deck,
    # tile_banner, tile_head, tile_deck, brief, footer, top_m, bot_m, gap,
    # brief_gap, title_pad
    dict(mast=62, stand=21, stat_num=30, stat_lab=11, hero_banner=100,
         hero_head=25, hero_deck=14, tile_banner=38, tile_head=15,
         tile_deck=11, brief=10.0, footer=11, top_m=24, bot_m=24, gap=7,
         brief_gap=2, title_pad=26),
    dict(mast=58, stand=20, stat_num=28, stat_lab=10.5, hero_banner=90,
         hero_head=25, hero_deck=14, tile_banner=34, tile_head=14.5,
         tile_deck=10.5, brief=9.5, footer=10.5, top_m=24, bot_m=24, gap=7,
         brief_gap=2, title_pad=26),
    dict(mast=56, stand=19, stat_num=27, stat_lab=10, hero_banner=82,
         hero_head=24, hero_deck=13.5, tile_banner=32, tile_head=14,
         tile_deck=10, brief=9.0, footer=10.5, top_m=22, bot_m=22, gap=6,
         brief_gap=1, title_pad=22),
    dict(mast=50, stand=19, stat_num=25, stat_lab=10, hero_banner=62,
         hero_head=23, hero_deck=13, tile_banner=26, tile_head=13.5,
         tile_deck=10, brief=9.0, footer=10, top_m=20, bot_m=20, gap=5,
         brief_gap=1, title_pad=20),
    dict(mast=48, stand=19, stat_num=24, stat_lab=9.5, hero_banner=56,
         hero_head=22, hero_deck=12.5, tile_banner=24, tile_head=13,
         tile_deck=9.5, brief=8.5, footer=10, top_m=20, bot_m=20, gap=4,
         brief_gap=0, title_pad=16),
]


def measure(level):
    """Compute section heights for a tightness level. Returns dict or None
    if the page cannot fit at this level."""
    p = LEVELS[level]
    g = p["gap"]
    # top sections
    eyebrow_h = 14
    mast_h = int(p["mast"] * 1.05)
    stand_f, stand_lines = fit_lines(STAND, SERIF_I, p["stand"], CW, 1, 16)
    stand_h = int(len(stand_lines) * p["stand"] * 1.25) + 2
    region_h = 20
    # stat strip: number + up to 3 label lines
    col_w = (CW - 5 * 10) // 6
    stat_lab_h = 0
    for _, label in STATS:
        f = F(SANS, p["stat_lab"])
        lines = wrap(label, f, col_w - 8)
        assert len(lines) <= 3, "stat label too long: %s" % label
        stat_lab_h = max(stat_lab_h, len(lines))
    stat_h = int(p["stat_num"] * 1.05) + 3 + int(stat_lab_h * p["stat_lab"] * 1.25)
    # hero row
    panel_w = (CW - 2 * 12) // 3
    inner = panel_w - 12
    hero_h = 0
    for hero in HEROES:
        _, hl = fit_lines(hero["headline"], SERIF_B, p["hero_head"], inner, 3, 18)
        _, dl = fit_lines(hero["deck"], SERIF, p["hero_deck"], inner, 3, 11)
        hh = (p["hero_banner"] + 4 + 13 + 3 + len(hl) * int(p["hero_head"] * 1.18)
              + 3 + len(dl) * int(p["hero_deck"] * 1.25) + 3 + 11 + 5)
        hero_h = max(hero_h, hh)
    # secondary grid
    tile_w = (CW - 4 * 10) // 5
    tin = tile_w - 10
    tile_h = 0
    for t in TILES:
        _, hl = fit_lines(t["headline"], SANS_B, p["tile_head"], tin, 2, 12)
        _, dl = fit_lines(t["deck"], SANS, p["tile_deck"], tin, 2, 9)
        th = (p["tile_banner"] + 3 + 12 + 2 + len(hl) * int(p["tile_head"] * 1.18)
              + 2 + len(dl) * int(p["tile_deck"] * 1.25) + 4)
        tile_h = max(tile_h, th)
    sec_h = 2 * tile_h + g
    # footer + credit (anchored at bottom)
    credit_h = 12
    foot_f = F(SANS, p["footer"])
    foot_lines = wrap(FOOTER, foot_f, CW - 16)
    footer_h = int(len(foot_lines) * p["footer"] * 1.28) + 12
    footer_top = H - p["bot_m"] - credit_h - 6 - footer_h
    # fixed part height (top margin + sections + gaps, ending after secondary)
    fixed = (p["top_m"] + eyebrow_h + g + mast_h + g + stand_h + g + region_h
             + g + stat_h + g + hero_h + g + sec_h + g)
    band_h = footer_top - g - fixed
    if band_h < 120:
        return None
    # also-on briefs: two columns of 11, pick font size that fits the band
    map_w = 440
    also_x = MARGIN + map_w + 12
    also_w = W - MARGIN - also_x
    colw = (also_w - 12) // 2
    brief_size = None
    for bs in (p["brief"], p["brief"] - 0.5, p["brief"] - 1.0):
        if bs < 8.5:
            continue
        bf = F(SANS, bs)
        lead = int(bs * 1.28)
        col_h = []
        for half in (BRIEFS[:11], BRIEFS[11:]):
            total = 0
            for b in half:
                lines = wrap(b, bf, colw)
                total += len(lines) * lead + p["brief_gap"]
            col_h.append(total)
        need = max(col_h) + p["title_pad"]
        if need <= band_h:
            brief_size = bs
            break
    if brief_size is None:
        return None
    total = fixed + g + band_h
    if total + footer_h + 6 + credit_h + p["bot_m"] > H:
        return None
    return dict(level=level, p=p, eyebrow_h=eyebrow_h, mast_h=mast_h,
                stand_f=stand_f, stand_lines=stand_lines, stand_h=stand_h,
                region_h=region_h, stat_h=stat_h, stat_lab_h=stat_lab_h,
                hero_h=hero_h, tile_h=tile_h, sec_h=sec_h,
                footer_h=footer_h, foot_lines=foot_lines, credit_h=credit_h,
                footer_top=footer_top, fixed=fixed, band_h=band_h,
                brief_size=brief_size, map_w=map_w, also_x=also_x,
                also_w=also_w, colw=colw)

def draw_page():
    level = None
    m = None
    for lv in range(len(LEVELS)):
        m = measure(lv)
        if m is not None:
            level = lv
            break
    assert m is not None, "page does not fit at any tightness level"
    p = m["p"]
    g = p["gap"]
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    y = p["top_m"]
    # 1. eyebrow
    f_eye = F(SANS_B, 13)
    draw_ls(d, x0, y, EYEBROW_L, f_eye, RED, tracking=2)
    rw = sum(f_eye.getlength(c) + 1 for c in EYEBROW_R) - 1
    draw_ls(d, x1 - rw, y, EYEBROW_R, f_eye, RED, tracking=1)
    y += m["eyebrow_h"]
    d.line([(x0, y + g // 2), (x1, y + g // 2)], fill=INK, width=1)
    y += g
    # 2. masthead
    f_mast = F(SERIF_B, p["mast"])
    d.text((x0, y), MASTHEAD, font=f_mast, fill=NAVY_BLACK)
    y += m["mast_h"]
    y += g
    # 3. standfirst (centred, single line, shrunk to fit)
    sw = m["stand_f"].getlength(STAND)
    d.text(((W - sw) / 2, y), STAND, font=m["stand_f"], fill=RED)
    y += m["stand_h"]
    y += g
    # 4. region strip
    f_reg = F(SANS_B, 11)
    chips = []
    for name, count, color in REGIONS:
        label = "%s %d" % (name, count)
        chips.append((label, color, f_reg.getlength(label) + 18))
    gap = 8
    total_w = sum(w for _, _, w in chips) + gap * (len(chips) - 1)
    cx = x0 + (CW - total_w) // 2
    for label, color, w in chips:
        d.rounded_rectangle([cx, y, cx + w, y + m["region_h"]], radius=4,
                            fill=color)
        tw = f_reg.getlength(label)
        d.text((cx + (w - tw) / 2, y + 5), label, font=f_reg, fill=WHITE)
        cx += w + gap
    y += m["region_h"]
    y += g
    # 5. stat strip
    col_w = (CW - 5 * 10) // 6
    f_num = F(SANS_B, p["stat_num"])
    f_lab = F(SANS, p["stat_lab"])
    for i, (num, label) in enumerate(STATS):
        colx = x0 + i * (col_w + 10)
        nw = f_num.getlength(num)
        d.text((colx + (col_w - nw) / 2, y), num, font=f_num, fill=NAVY)
        ly = y + int(p["stat_num"] * 1.05) + 3
        lines = wrap(label, f_lab, col_w - 8)
        for li, line in enumerate(lines):
            lw = f_lab.getlength(line)
            d.text((colx + (col_w - lw) / 2, ly + li * int(p["stat_lab"] * 1.25)),
                   line, font=f_lab, fill=INK)
        if i < 5:
            d.line([(colx + col_w + 5, y + 4),
                    (colx + col_w + 5, y + m["stat_h"] - 4)],
                   fill=(200, 196, 182), width=1)
    y += m["stat_h"]
    y += g
    # 6. hero row
    panel_w = (CW - 2 * 12) // 3
    for i, hero in enumerate(HEROES):
        px = x0 + i * (panel_w + 12)
        d.rectangle([px, y, px + panel_w, y + m["hero_h"]],
                    outline=PANEL_LINE, width=1)
        bx = (px, y, px + panel_w, y + p["hero_banner"])
        paint_banner(d, bx, hero["scene"])
        d.line([(px, y + p["hero_banner"]), (px + panel_w, y + p["hero_banner"])],
               fill=PANEL_LINE, width=1)
        ty = y + p["hero_banner"] + 4
        f_kick = F(SANS_B, 13)
        d.text((px + 6, ty), hero["kicker"], font=f_kick, fill=RED)
        ty += 13 + 3
        f_h, hl = fit_lines(hero["headline"], SERIF_B, p["hero_head"],
                            panel_w - 12, 3, 18)
        for line in hl:
            d.text((px + 6, ty), line, font=f_h, fill=INK)
            ty += int(f_h.size * 1.18)
        ty += 3
        f_d, dl = fit_lines(hero["deck"], SERIF, p["hero_deck"],
                            panel_w - 12, 3, 11)
        for line in dl:
            d.text((px + 6, ty), line, font=f_d, fill=(50, 50, 50))
            ty += int(f_d.size * 1.25)
        ty += 3
        f_s = F(SANS, 11)
        d.text((px + 6, ty), hero["source"], font=f_s, fill=GREY)
    y += m["hero_h"]
    y += g
    # 7. secondary grid
    tile_w = (CW - 4 * 10) // 5
    for r in range(2):
        for c in range(5):
            t = TILES[r * 5 + c]
            tx = x0 + c * (tile_w + 10)
            ty0 = y + r * (m["tile_h"] + 8)
            d.rectangle([tx, ty0, tx + tile_w, ty0 + m["tile_h"]],
                        outline=PANEL_LINE, width=1)
            bx = (tx, ty0, tx + tile_w, ty0 + p["tile_banner"])
            paint_banner(d, bx, t["scene"])
            d.line([(tx, ty0 + p["tile_banner"]),
                    (tx + tile_w, ty0 + p["tile_banner"])],
                   fill=PANEL_LINE, width=1)
            ty = ty0 + p["tile_banner"] + 3
            f_k = F(SANS_B, 11)
            d.text((tx + 5, ty), t["kicker"], font=f_k, fill=RED)
            ty += 12 + 2
            f_h, hl = fit_lines(t["headline"], SANS_B, p["tile_head"],
                                tile_w - 10, 2, 12)
            for line in hl:
                d.text((tx + 5, ty), line, font=f_h, fill=INK)
                ty += int(f_h.size * 1.18)
            ty += 2
            f_d, dl = fit_lines(t["deck"], SANS, p["tile_deck"],
                                tile_w - 10, 2, 9)
            for line in dl:
                d.text((tx + 5, ty), line, font=f_d, fill=(50, 50, 50))
                ty += int(f_d.size * 1.25)
    y += m["sec_h"]
    y += g
    # 8. bottom band: map (left) + also-on (right)
    band_y = y
    band_h = m["band_h"]
    # map panel
    d.rectangle([x0, band_y, x0 + m["map_w"], band_y + band_h],
                outline=PANEL_LINE, width=1)
    f_t = F(SANS_B, 13)
    d.text((x0 + 8, band_y + 6), "WHERE IT HAPPENED", font=f_t, fill=NAVY)
    map_box = (x0 + 4, band_y + 26, x0 + m["map_w"] - 4, band_y + band_h - 4)
    mind, ndots = draw_map(d, map_box)
    # also-on panel
    ax = m["also_x"]
    d.rectangle([ax, band_y, x1, band_y + band_h], outline=PANEL_LINE, width=1)
    d.text((ax + 8, band_y + 6), "ALSO ON MONDAY 23 NOVEMBER 2026",
           font=f_t, fill=NAVY)
    bf = F(SANS, m["brief_size"])
    lead = int(m["brief_size"] * 1.28)
    for ci, half in enumerate((BRIEFS[:11], BRIEFS[11:])):
        cx = ax + 8 + ci * (m["colw"] + 12)
        cy = band_y + 26
        for b in half:
            lines = wrap(b, bf, m["colw"])
            for line in lines:
                d.text((cx, cy), line, font=bf, fill=INK)
                cy += lead
            cy += 2
    y = band_y + band_h
    y += g
    # 9. date-check footer
    assert y <= m["footer_top"], "footer overlap: y=%d footer_top=%d" % (
        y, m["footer_top"])
    y = m["footer_top"]
    d.rectangle([x0, y, x1, y + m["footer_h"]], outline=RED, width=2)
    f_foot = F(SANS, p["footer"])
    fy = y + 6
    for line in m["foot_lines"]:
        d.text((x0 + 8, fy), line, font=f_foot, fill=INK)
        fy += int(p["footer"] * 1.28)
    # 10. credit line (shrunk to fit one line; the full text is ~230 chars
    # and overflows at 10px, so fit it down instead of clipping)
    f_cr, cr_lines = fit_lines(CREDIT, SANS, 10, CW, 1, 7.5)
    assert len(cr_lines) == 1, "credit does not fit one line: %s" % cr_lines
    cw = f_cr.getlength(cr_lines[0])
    assert cw <= CW, "credit still too wide: %.0f" % cw
    d.text(((W - cw) / 2, H - p["bot_m"] - 12), cr_lines[0], font=f_cr,
           fill=GREY)
    return img, level, mind, ndots


def main():
    img, level, mind, ndots = draw_page()
    img.save("entry.png", optimize=True)
    import os
    size = os.path.getsize("entry.png")
    assert img.size == (1024, 1024), img.size
    assert size < 1048576, "entry.png too big: %d" % size
    print("level=%d size=%d bytes dims=%sx%s map_mindot=%.1f dots=%d stories=35"
          % (level, size, img.size[0], img.size[1], mind, ndots))


if __name__ == "__main__":
    main()
