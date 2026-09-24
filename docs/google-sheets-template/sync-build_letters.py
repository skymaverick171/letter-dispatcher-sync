import os
import sys

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

# Generates Letter_Dispatcher_Letters_Template.xlsx — the Google Sheets /
# Excel companion to build.py's Contacts template, in the same visual style
# (same palette, fonts, striping, instructions layout). See build.py for the
# full rationale behind that shared styling; this file only documents what's
# specific to the Letters sheet.

ACCENT = "1E4B8F"
ACCENT_SOFT = "E3EAF6"
INK = "1F2A24"
MUTED = "5C6A63"
BORDER_CLR = "D9DDD4"
STRIPE = "F5F6F3"

FONT_NAME = "Arial"

thin = Side(style="thin", color=BORDER_CLR)
box = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.Workbook()

# ----------------------------------------------------------------- Letters
ws = wb.active
ws.title = "Letters"

headers = ["Subject", "Body", "Cc", "Bcc", "Personalize", "ID (do not edit)"]
col_widths = [28, 60, 26, 26, 14, 20]

for i, (h, w) in enumerate(zip(headers, col_widths), start=1):
    col = get_column_letter(i)
    ws.column_dimensions[col].width = w
    cell = ws.cell(row=1, column=i, value=h)
    cell.font = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=ACCENT)
    cell.alignment = Alignment(horizontal="left", vertical="center")
    cell.border = box

# ID is the hidden bookkeeping column two-way sync needs to match a sheet
# row to a record in the app (see the Sync tab / README for setup). Leave
# it blank for new rows — the app fills it in the first time a row syncs.
ws.cell(row=1, column=6).comment = Comment(
    "Two-way sync (admin accounts) uses this hidden column to match sheet "
    "rows to records in the app. Leave it blank for new rows and don't "
    "type into it — the app fills it in automatically the first time a "
    "row is synced. One-way sync ignores this column entirely.",
    "Letter Dispatcher template",
)

ws.row_dimensions[1].height = 24
ws.freeze_panes = "A2"

# Personalize is a "yes/no" flag (blank counts as "yes" in the app) —
# whether {{name}}/{{email}} placeholders in Subject/Body get filled in per
# recipient when sending, vs. sent as one identical letter to everyone.
examples = [
    [
        "Payment Reminder (example)",
        "Hello, {{name}}!\n\nJust a reminder that your invoice is due in 3 days. "
        "If you've already paid, please disregard this message.\n\nThanks!",
        None,
        None,
        "yes",
        None,
    ],
    [
        "Meeting Invitation (example)",
        "Hi {{name}},\n\nYou're invited to a meeting this Thursday at 3:00 PM. "
        "Please let us know if that time works for you.\n\nBest regards",
        None,
        None,
        "yes",
        None,
    ],
]
example_font = Font(name=FONT_NAME, size=10.5, italic=True, color=MUTED)
for r, row in enumerate(examples, start=2):
    ws.row_dimensions[r].height = 60
    for c, val in enumerate(row, start=1):
        cell = ws.cell(row=r, column=c, value=val)
        cell.font = example_font
        cell.fill = PatternFill("solid", fgColor=STRIPE)
        cell.border = box
        cell.alignment = Alignment(vertical="center", wrap_text=(c == 2))

ws["A2"].comment = Comment(
    "Пример строки — можно удалить или перезаписать своими данными.\n"
    "Example row — delete or overwrite with your own data.\n"
    "Ligne d'exemple — supprimez-la ou remplacez-la par vos données.",
    "Letter Dispatcher template",
)

first_blank = 4
last_blank = 200
normal_font = Font(name=FONT_NAME, size=10.5, color=INK)
for r in range(first_blank, last_blank + 1):
    band = PatternFill("solid", fgColor=STRIPE) if r % 2 == 0 else PatternFill(fill_type=None)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=r, column=c)
        cell.font = normal_font
        cell.fill = band
        cell.border = box

ws.sheet_view.showGridLines = False

# Personalize dropdown — "yes"/"no", plain string list (no other sheet
# involved, unlike the Contacts Group dropdown), matching the app's own
# personalize toggle.
dv = DataValidation(type="list", formula1='"yes,no"', allow_blank=True, showDropDown=False)
dv.error = "Choose yes or no, or leave blank (treated as yes)."
dv.errorTitle = "Personalize"
dv.error_style = "information"
ws.add_data_validation(dv)
dv.add(f"E2:E{last_blank}")

# ---------------------------------------------------------------- Instructions (generic builder, one per language)


def build_instructions_sheet(wb, sheet_name, t):
    ins = wb.create_sheet(sheet_name)
    ins.sheet_view.showGridLines = False
    ins.column_dimensions["A"].width = 3
    ins.column_dimensions["B"].width = 92

    row = [2]

    def title_row(text, size=16):
        c = ins.cell(row=row[0], column=2, value=text)
        c.font = Font(name=FONT_NAME, size=size, bold=True, color=ACCENT)
        row[0] += 1

    def section_row(text):
        r = row[0]
        ins.merge_cells(start_row=r, start_column=2, end_row=r, end_column=2)
        c = ins.cell(row=r, column=2, value=text)
        c.font = Font(name=FONT_NAME, size=12, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=ACCENT)
        c.alignment = Alignment(vertical="center", indent=1)
        ins.row_dimensions[r].height = 22
        row[0] += 1

    def body_row(text, bold=False, color=INK, wrap=True, height=None):
        r = row[0]
        c = ins.cell(row=r, column=2, value=text)
        c.font = Font(name=FONT_NAME, size=10.5, bold=bold, color=color)
        c.alignment = Alignment(vertical="top", wrap_text=wrap)
        if height:
            ins.row_dimensions[r].height = height
        row[0] += 1

    def callout_row(text, fill=ACCENT_SOFT, text_color=ACCENT, height=44):
        r = row[0]
        ins.merge_cells(start_row=r, start_column=2, end_row=r, end_column=2)
        c = ins.cell(row=r, column=2, value=text)
        c.font = Font(name=FONT_NAME, size=10.5, bold=True, color=text_color)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(vertical="center", horizontal="left", wrap_text=True, indent=1)
        ins.row_dimensions[r].height = height
        row[0] += 1

    def blank():
        row[0] += 1

    title_row(t["title"])
    body_row(t["subtitle"], color=MUTED)
    blank()

    section_row(t["s1_head"])
    body_row(t["s1_body"], height=t["s1_h"])
    blank()

    section_row(t["s2_head"])
    body_row(t["s2_body"], height=t["s2_h"])
    blank()

    section_row(t["s3_head"])
    body_row(t["s3_body"], height=t["s3_h"])
    blank()

    callout_row(t["callout"], height=t["callout_h"])

    return ins


RU = dict(
    title="Letter Dispatcher ↔ Google Sheets — шаблоны писем",
    subtitle="Как использовать эту таблицу как набор готовых писем для приложения Letter Dispatcher.",
    s1_head="1. Заполните лист «Letters»",
    s1_body=(
        "Столбцы должны идти строго в этом порядке: Subject, Body, Cc, Bcc, Personalize.\n"
        "Обязательны только Subject и Body — Cc, Bcc и Personalize можно оставлять пустыми "
        "(пустой Personalize считается «yes», то есть персонализированным).\n"
        "В тексте письма (Body) можно использовать плейсхолдеры {{name}} и {{email}} — приложение "
        "заменит их данными получателя при отправке.\n"
        "Строки с пометкой «(example)» — это образец, их можно удалить или заменить своими данными."
    ),
    s1_h=94.5,
    s2_head="2. Перенести письма ИЗ таблицы в приложение",
    s2_body=(
        "1) Выделите заполненные строки в Letters (можно вместе с заголовком — приложение само его "
        "распознает).\n"
        "2) Скопируйте (Ctrl+C / ⌘+C).\n"
        "3) В Letter Dispatcher откройте вкладку Letters → «Import from Google Sheets».\n"
        "4) Вставьте (Ctrl+V) в поле и нажмите «Import pasted rows»."
    ),
    s2_h=69.75,
    s3_head="3. Получатели",
    s3_body=(
        "Список получателей в этот шаблон не входит — одно и то же письмо обычно рассылается разным "
        "людям в разное время, поэтому получателей нужно выбрать в приложении отдельно, уже после "
        "импорта письма (вкладка Letters → «Recipients for this letter»)."
    ),
    s3_h=54.75,
    callout=(
        "ℹ  Это ручной обмен буфером обмена / файлом, а не автоматическая синхронизация — "
        "изменения в одном месте не появляются в другом сами по себе, перенос нужно повторять."
    ),
    callout_h=43.5,
)

EN = dict(
    title="Letter Dispatcher ↔ Google Sheets — letter templates",
    subtitle="How to use this sheet as a set of ready-made letters for the Letter Dispatcher app.",
    s1_head='1. Fill in the "Letters" sheet',
    s1_body=(
        "Columns must be in exactly this order: Subject, Body, Cc, Bcc, Personalize.\n"
        "Only Subject and Body are required — Cc, Bcc and Personalize can be left blank "
        '(a blank Personalize is treated as "yes", i.e. personalized).\n'
        "The letter text (Body) can use the {{name}} and {{email}} placeholders — the app fills "
        "them in with each recipient's details when sending.\n"
        'Rows marked "(example)" are sample data — delete them or overwrite with your own.'
    ),
    s1_h=94.5,
    s2_head="2. Bring letters FROM this sheet INTO the app",
    s2_body=(
        "1) Select the filled-in rows in Letters (you can include the header row — the app "
        "recognizes it automatically).\n"
        "2) Copy (Ctrl+C / ⌘+C).\n"
        '3) In Letter Dispatcher, open the Letters tab → "Import from Google Sheets".\n'
        '4) Paste (Ctrl+V) into the box and click "Import pasted rows".'
    ),
    s2_h=69.75,
    s3_head="3. Recipients",
    s3_body=(
        "Recipients aren't part of this template — the same letter is usually sent to different "
        "people at different times, so you pick recipients in the app separately, after importing "
        'the letter (Letters tab → "Recipients for this letter").'
    ),
    s3_h=54.75,
    callout=(
        "ℹ  This is a manual clipboard/file exchange, not automatic syncing — changes made in one "
        "place don't appear in the other by themselves; you need to repeat the transfer."
    ),
    callout_h=43.5,
)

FR = dict(
    title="Letter Dispatcher ↔ Google Sheets — modèles de lettres",
    subtitle=(
        "Comment utiliser cette feuille comme ensemble de lettres prêtes à l'emploi pour "
        "l'application Letter Dispatcher."
    ),
    s1_head="1. Remplissez la feuille « Letters »",
    s1_body=(
        "Les colonnes doivent être exactement dans cet ordre : Subject, Body, Cc, Bcc, Personalize.\n"
        "Seuls Subject et Body sont obligatoires — Cc, Bcc et Personalize peuvent rester vides "
        "(un Personalize vide est traité comme « yes », c'est-à-dire personnalisé).\n"
        "Le texte de la lettre (Body) peut utiliser les balises {{name}} et {{email}} — "
        "l'application les remplace par les informations de chaque destinataire lors de l'envoi.\n"
        "Les lignes marquées « (example) » sont des exemples — supprimez-les ou remplacez-les par "
        "vos propres données."
    ),
    s1_h=109.5,
    s2_head="2. Transférer les lettres DE cette feuille VERS l'application",
    s2_body=(
        "1) Sélectionnez les lignes remplies dans Letters (vous pouvez inclure l'en-tête — "
        "l'application le reconnaît automatiquement).\n"
        "2) Copiez (Ctrl+C / ⌘+C).\n"
        "3) Dans Letter Dispatcher, ouvrez l'onglet Letters → « Import from Google Sheets ».\n"
        "4) Collez (Ctrl+V) dans le champ et cliquez sur « Import pasted rows »."
    ),
    s2_h=69.75,
    s3_head="3. Destinataires",
    s3_body=(
        "Les destinataires ne font pas partie de ce modèle — la même lettre est généralement "
        "envoyée à des personnes différentes à des moments différents, donc vous les choisissez "
        "séparément dans l'application, après avoir importé la lettre (onglet Letters → "
        "« Recipients for this letter »)."
    ),
    s3_h=64.5,
    callout=(
        "ℹ  Il s'agit d'un échange manuel (presse-papiers ou fichier), pas d'une synchronisation "
        "automatique — les changements faits d'un côté n'apparaissent pas de l'autre tout seuls ; "
        "il faut répéter le transfert."
    ),
    callout_h=43.5,
)

build_instructions_sheet(wb, "Instructions (EN)", EN)
build_instructions_sheet(wb, "Instructions (FR)", FR)
build_instructions_sheet(wb, "Инструкция (RU)", RU)

OUT = sys.argv[1] if len(sys.argv) > 1 else "Letter_Dispatcher_Letters_Template.xlsx"
wb.save(OUT)
print("saved", os.path.abspath(OUT))
