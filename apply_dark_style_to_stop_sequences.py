"""
Apply matching dark theme to the 'API Parameter: stop_sequences' slide in both v2 and v3 PPTX files.
"""
import sys, shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

FONT = 'Segoe UI'
CODE_FONT = 'Consolas'

# Colors from workshop dark theme
BG_DARK = '0F172A'
CARD_BG = '16203A'
CODE_BG = '0B1120'
WHITE = 'FFFFFF'
BLUE = '38BDF8'
CYAN = '22D3EE'
GREEN = '4ADE80'
AMBER = 'FBBF24'
RED = 'F87171'
BODY = 'E2E8F0'
MUTED = '94A3B8'

PERSIAN_NOTES = """توضیحات و کاربردهای پارامتر stop_sequences:

پارامتر stop_sequences در API مدل‌ها (به‌ویژه کلاد/Anthropic و OpenAI) به مدل می‌گوید: «هر زمان در حین تولید متن به هر یک از این رشته‌ها رسیدی، بلافاصله تولید را متوقف کن.»

چهار کاربرد کلیدی:
۱. استخراج داده‌های ساختاریافته (JSON / XML): برای مثال تنظیم توالی توقف روی </result> یا } باعث می‌شود مدل بعد از پایان داده‌ها، جملات اضافی و تعارفی ننویسد.
۲. ممانعت از جعل نقش کاربر: در چت‌ها با تنظیم stop روی \\n\\nHuman: جلوی ادامه‌دادن گفتگو از طرف کاربر توسط مدل گرفته می‌شود.
۳. قالب‌های فقط کد: با تنظیم stop روی ``` مطمئن می‌شوید مدل بلافاصله بعد از بلوک کد متوقف می‌شود و هیچ متن توضیحی اضافه نمی‌کند.
۴. کنترل تعداد آیتم‌ها و صرفه‌جویی هزینه: مثلاً توقف روی "6." برای تولید دقیقاً ۵ آیتم لیست و جلوگیری از هدررفت توکن‌ها.

مزیت مهندسی:
دستورات پرامپتی (مثل "لطفاً بعد از خروجی حرف نزن") ماهیت آماری دارند و گاهی نادیده گرفته می‌شوند؛ اما stop_sequences در لایه انجین سمپلر مستقیماً تولید توکن را قطع می‌کند و ریسک خروجی اضافه را به صفر می‌رساند."""

def style_slide(slide):
    # Clear all existing shapes on this slide
    for ph in list(slide.placeholders):
        try:
            ph._element.getparent().remove(ph._element)
        except Exception:
            pass
    for shp in list(slide.shapes):
        try:
            shp._element.getparent().remove(shp._element)
        except Exception:
            pass
            
    # Set dark background
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(BG_DARK)

    def rect(x, y, w, h, color, rounded=True, border_color=None):
        shp = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
            Emu(x), Emu(y), Emu(w), Emu(h)
        )
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor.from_string(color)
        if border_color:
            shp.line.color.rgb = RGBColor.from_string(border_color)
            shp.line.width = Pt(1)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        if rounded:
            shp.adjustments[0] = 0.05
        return shp

    def text_box(x, y, w, h, paras, spacing=250, align=PP_ALIGN.LEFT):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, (t, size, bold, color, font_name) in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_before = Pt(spacing / 100)
            p.space_after = Pt(spacing / 100)
            p.alignment = align
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.name = font_name
            r.font.color.rgb = RGBColor.from_string(color)
        return tb

    # 1. Header (Pill, Title, Underline, Subtitle)
    # Badge Pill
    pill = rect(731520, 320040, 1097280, 480000, CYAN)
    p = pill.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = 'API TOOL'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.name = FONT
    r.font.color.rgb = RGBColor.from_string('0F172A')

    # Title
    text_box(1950000, 290000, 9500000, 548640, [
        ('API Parameter: stop_sequences', 32, True, WHITE, FONT)
    ], spacing=0)

    # Accent Underline
    rect(731520, 920000, 3657600, 45000, BLUE, rounded=False)

    # Subtitle
    text_box(731520, 1020000, 10881360, 380000, [
        ('Halt token generation immediately when a pattern matches — zero conversational filler, 100% deterministic cutoffs.', 14, False, MUTED, FONT)
    ], spacing=0)

    # Layout dimensions
    LEFT_X = 731520
    COL_W = 5250000
    GAP = 381360
    RIGHT_X = LEFT_X + COL_W + GAP
    TOP_Y = 1480000

    # ================= LEFT COLUMN =================
    # Card 1: 4 Key Production Use Cases
    C1_H = 4050000
    rect(LEFT_X, TOP_Y, COL_W, C1_H, CARD_BG, border_color='1E293B')
    
    text_box(LEFT_X + 180000, TOP_Y + 120000, COL_W - 360000, 350000, [
        ('🎯  Key Production Use Cases', 17, True, BLUE, FONT)
    ], spacing=0)

    use_cases = [
        ('1. Structured Output Isolation', 13, True, GREEN, FONT),
        ('    Stop at "</result>" or "}" so the model never adds trailing fluff ("Hope this helps!").', 11.5, False, BODY, FONT),
        ('2. Code-Only Blocks', 13, True, GREEN, FONT),
        ('    Set stop sequence to "```" to terminate the response instantly after the code snippet.', 11.5, False, BODY, FONT),
        ('3. Role & Chat Boundaries', 13, True, GREEN, FONT),
        ('    Stop at "\\n\\nHuman:" to prevent the model from impersonating the user in turn-based chat.', 11.5, False, BODY, FONT),
        ('4. Strict Item Counts & Cost Control', 13, True, GREEN, FONT),
        ('    Want exactly 5 items? Stop at "6." to save latency and token charges automatically.', 11.5, False, BODY, FONT),
    ]
    text_box(LEFT_X + 180000, TOP_Y + 520000, COL_W - 360000, C1_H - 600000, use_cases, spacing=140)

    # Card 2 (Bottom Left): Hard Engine Stop vs Soft Prompting
    C2_Y = TOP_Y + C1_H + 160000
    C2_H = 1400000
    rect(LEFT_X, C2_Y, COL_W, C2_H, '1C1917', border_color='78350F') # Amber-tinted dark card
    
    text_box(LEFT_X + 180000, C2_Y + 90000, COL_W - 360000, 300000, [
        ('⚡  Why stop_sequences Beats Prompt Instructions', 14.5, True, AMBER, FONT)
    ], spacing=0)

    takeaways = [
        ('• Prompts like "do not say anything else" are probabilistic (~5-10% failure rate).', 11.5, False, BODY, FONT),
        ('• stop_sequences is enforced directly by the sampler engine — 100% guaranteed cutoff.', 11.5, True, CYAN, FONT)
    ]
    text_box(LEFT_X + 180000, C2_Y + 450000, COL_W - 360000, C2_H - 520000, takeaways, spacing=180)

    # ================= RIGHT COLUMN =================
    # Card 3: Code / Payload Box (Dark IDE Style)
    C3_H = 5610000
    rect(RIGHT_X, TOP_Y, COL_W, C3_H, CODE_BG, border_color='334155')

    # Code header tab
    tab = rect(RIGHT_X, TOP_Y, COL_W, 400000, '1E293B', rounded=False)
    p_tab = tab.text_frame.paragraphs[0]
    p_tab.alignment = PP_ALIGN.LEFT
    r_tab = p_tab.add_run()
    r_tab.text = '   API Request Payload (Claude Messages API)'
    r_tab.font.size = Pt(12)
    r_tab.font.name = FONT
    r_tab.font.bold = True
    r_tab.font.color.rgb = RGBColor.from_string(MUTED)

    code_lines = [
        ('POST /v1/messages', 12, True, CYAN, CODE_FONT),
        ('{', 12, False, WHITE, CODE_FONT),
        ('  "model": "claude-3-opus-20240229",', 12, False, GREEN, CODE_FONT),
        ('  "max_tokens": 1000,', 12, False, BODY, CODE_FONT),
        ('  "messages": [', 12, False, WHITE, CODE_FONT),
        ('    {', 12, False, WHITE, CODE_FONT),
        ('      "role": "user",', 12, False, BLUE, CODE_FONT),
        ('      "content": "List 5 planets with key facts."', 12, False, GREEN, CODE_FONT),
        ('    }', 12, False, WHITE, CODE_FONT),
        ('  ],', 12, False, WHITE, CODE_FONT),
        ('  "stop_sequences": [', 12, True, AMBER, CODE_FONT),
        ('    "6.",', 12, True, AMBER, CODE_FONT),
        ('    "</list>"', 12, True, AMBER, CODE_FONT),
        ('  ]', 12, True, AMBER, CODE_FONT),
        ('}', 12, False, WHITE, CODE_FONT),
        ('', 10, False, BODY, CODE_FONT),
        ('// Result: Model stops the moment it prints "6."', 11, False, MUTED, CODE_FONT),
        ('// Stop Reason: "stop_sequence"', 11, True, CYAN, CODE_FONT),
    ]
    text_box(RIGHT_X + 220000, TOP_Y + 500000, COL_W - 440000, C3_H - 600000, code_lines, spacing=80)

    # Add Speaker notes in Persian
    slide.notes_slide.notes_text_frame.text = PERSIAN_NOTES


def process_presentation(path):
    print(f"Processing {path}...")
    prs = Presentation(path)
    
    # Search for existing stop_sequences slide
    target_slide = None
    target_idx = None
    for i, s in enumerate(prs.slides):
        for shp in s.shapes:
            if shp.has_text_frame and "stop_sequences" in shp.text:
                target_slide = s
                target_idx = i
                break
        if target_slide:
            break

    if target_slide:
        print(f"Found existing slide at index {target_idx}, re-styling...")
        style_slide(target_slide)
    else:
        print("Slide not found, creating new slide after Lab 4...")
        # Find Lab 4 Exercise slide (usually around index 16 or 17)
        insert_pos = 17
        for i, s in enumerate(prs.slides):
            for shp in s.shapes:
                if shp.has_text_frame and ("Exercise 4" in shp.text or "Relational JSON" in shp.text):
                    insert_pos = i + 1
                    break
        
        # Add slide
        layout = prs.slides[0].slide_layout
        new_slide = prs.slides.add_slide(layout)
        style_slide(new_slide)
        
        # Reorder slide to insert_pos
        xml_slides = prs.slides._sldIdLst
        slides = list(xml_slides)
        xml_slides.remove(slides[-1])
        xml_slides.insert(insert_pos, slides[-1])
        print(f"Inserted and styled slide at index {insert_pos}.")

    prs.save(path)
    print(f"Saved {path} successfully!")

if __name__ == '__main__':
    v2_path = Path(r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v2.pptx")
    v3_path = Path(r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v3.pptx")
    
    if v2_path.exists():
        process_presentation(v2_path)
    if v3_path.exists():
        process_presentation(v3_path)
