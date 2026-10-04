"""
Insert 2 beautifully styled dark slides on 'Order Sensitivity & Recency Bias'
right after slide 13 (index 12 in 0-based indexing) in Prompt_Engineering_Workshop_v2.pptx and v3.pptx.
"""
import sys, shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

FONT = 'Segoe UI'
CODE_FONT = 'Consolas'

# Theme Colors
BG_DARK = '0F172A'
CARD_BG = '16203A'
WHITE = 'FFFFFF'
BLUE = '38BDF8'
CYAN = '22D3EE'
GREEN = '4ADE80'
AMBER = 'FBBF24'
RED = 'F87171'
BODY = 'E2E8F0'
MUTED = '94A3B8'

SLIDE1_NOTES = """پدیده Recency Bias و Order Sensitivity در مدل‌های زبانی:

مشاهده تجربی:
وقتی ترتیب استدلال‌ها را عوض می‌کنیم و استدلال مثبت را در انتها می‌آوریم، خروجی مدل ممکن است کاملاً مثبت شود. در اکثر مواقع، مدل‌ها تمایل بیشتری دارند که گزینه دوم را انتخاب کنند.

چرا این اتفاق می‌افتد؟
۱. ماهیت خودبازگشتی (Autoregressive Attention):
مدل‌ها متن را توکن به توکن پردازش می‌کنند. توکن‌هایی که در انتهای کانتکست (نزدیک‌ترین نقطه به زمان تولید خروجی) قرار دارند، در لایه‌های Attention تازه‌تر هستند و بیشترین گرادیان توجه را دریافت می‌کنند (Recency Effect).

۲. سوگیری داده‌های آموزشی (Training Data Bias):
در متون وب، الگوی نگارش انسان‌ها معمولاً این است که ابتدا گزینه‌های ضعیف‌تر یا ردشده را مطرح می‌کنند و در پایان گزینه برنده و نهایی را به عنوان نتیجه‌گیری می‌آورند. در نتیجه وزن‌های مدل، موقعیت‌های پایانی را بیشتر با برچسب نتیجه مطلوب مرتبط کرده‌اند."""

SLIDE2_NOTES = """راهکارهای مقابله با سوگیری ترتیب (Order Sensitivity):

چالش در کاربردهای واقعی (به‌ویژه LLM-as-a-Judge):
در سیستم‌های ارزیابی خودکار و مقایسه‌های A/B یا رتبه‌بندی RAG، اگر صرفاً بپرسیم کدام پاسخ بهتر است، مدل در ۶۰٪ تا ۷۰٪ مواقع گزینه دوم را ترجیح می‌دهد، صرفاً به خاطر موقعیت مکانی آن!

۳ راهکار استاندارد تولیدی:
۱. ارزیابی دوطرفه (Position Swapping / Position Calibration):
پرامپت را یک‌بار با ترتیب (A, B) و بار دیگر با ترتیب (B, A) بفرستید. فقط در صورتی برنده را قطعی بدانید که در هر دو حالت یک گزینه مفهومی یکسان برنده شود. اگر با جابجایی نظرش عوض شد، این سیگنالِ یک مورد مرزی / تساوی (Tie) است.

۲. اجبار به استدلال قبل از رأی (Chain-of-Thought):
مدل را مجبور کنید ابتدا نقاط قوت و ضعف هر دو گزینه را تحلیل کند و سپس نتیجه را اعلام کند. کانتکست استدلال تولیدشده توسط خود مدل، اثر سوگیری آخرین ورودی را خنثی می‌کند.

۳. قالب‌های خنثی و تگ‌های XML:
استفاده از تگ‌های XML و اسامی خنثی مثل Candidate Alpha و Candidate Beta به جای گزینه‌های عددی (Option 1/2)، سوگیری ترتیب را کاهش می‌دهد."""

def rect(slide, x, y, w, h, color, rounded=True, border_color=None):
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

def text_box(slide, x, y, w, h, paras, spacing=250, align=PP_ALIGN.LEFT):
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

def build_slide1(slide):
    # Clear placeholders & set dark background
    for ph in list(slide.placeholders):
        try: ph._element.getparent().remove(ph._element)
        except Exception: pass
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(BG_DARK)

    # Header
    pill = rect(slide, 731520, 320040, 1400000, 480000, CYAN)
    p = pill.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = 'DEEP DIVE'; r.font.size = Pt(14); r.font.bold = True
    r.font.name = FONT; r.font.color.rgb = RGBColor.from_string('0F172A')

    text_box(slide, 2250000, 290000, 9200000, 548640, [
        ('Order Sensitivity & Recency Bias', 31, True, WHITE, FONT)
    ], spacing=0)

    rect(slide, 731520, 920000, 3657600, 45000, BLUE, rounded=False)

    text_box(slide, 731520, 1020000, 10881360, 380000, [
        ('LLMs are surprisingly sensitive to option ordering: swapping sequence can flip the model\'s final judgment.', 14, False, MUTED, FONT)
    ], spacing=0)

    # Section 1: Anthropic Observation Box (Top across)
    QUOTE_Y = 1480000
    QUOTE_H = 1680000
    TOTAL_W = 10881360
    rect(slide, 731520, QUOTE_Y, TOTAL_W, QUOTE_H, CARD_BG, border_color='334155')

    text_box(slide, 731520 + 180000, QUOTE_Y + 110000, TOTAL_W - 360000, 320000, [
        ('🔎  Anthropic Frontier Research Observation', 15.5, True, AMBER, FONT)
    ], spacing=0)

    quote_paras = [
        ('"Claude is sensitive to ordering. When we swap the order of the arguments so that negative is first and positive is second, this changes Claude\'s overall assessment to positive."', 12.5, False, GREEN, FONT),
        ('"In most situations, Claude is more likely to choose the second of two options, likely because in web training data, second options were more likely to be the winning argument."', 12, False, CYAN, FONT)
    ]
    text_box(slide, 731520 + 180000, QUOTE_Y + 520000, TOTAL_W - 360000, QUOTE_H - 600000, quote_paras, spacing=150)

    # Section 2: Two Root Causes (Side-by-Side Cards)
    ROW_Y = QUOTE_Y + QUOTE_H + 180000
    ROW_H = 3450000
    COL_W = (TOTAL_W - 365760) // 2
    RIGHT_X = 731520 + COL_W + 365760

    # Left: Architectural Cause
    rect(slide, 731520, ROW_Y, COL_W, ROW_H, CARD_BG, border_color='1E293B')
    text_box(slide, 731520 + 180000, ROW_Y + 120000, COL_W - 360000, 350000, [
        ('1. Autoregressive Attention Gradient', 16, True, BLUE, FONT)
    ], spacing=0)

    left_pts = [
        ('• Left-to-Right Processing:', 13, True, GREEN, FONT),
        ('  Tokens are processed sequentially; tokens near the output generation point remain fresher in attention memory.', 11.5, False, BODY, FONT),
        ('• Higher Recency Salience:', 13, True, GREEN, FONT),
        ('  The model begins output generation with the highest attention gradient focused on the final sentences it just read.', 11.5, False, BODY, FONT),
        ('• Momentum Effect:', 13, True, GREEN, FONT),
        ('  The final option dominates the initial sampled tokens, anchoring the rest of the response.', 11.5, False, CYAN, FONT),
    ]
    text_box(slide, 731520 + 180000, ROW_Y + 520000, COL_W - 360000, ROW_H - 600000, left_pts, spacing=100)

    # Right: Training Data Bias
    rect(slide, RIGHT_X, ROW_Y, COL_W, ROW_H, CARD_BG, border_color='1E293B')
    text_box(slide, RIGHT_X + 180000, ROW_Y + 120000, COL_W - 360000, 350000, [
        ('2. Human Rhetorical Training Bias', 16, True, BLUE, FONT)
    ], spacing=0)

    right_pts = [
        ('• Common Web Rhetorical Pattern:', 13, True, GREEN, FONT),
        ('  In human articles and essays, authors typically open with flawed ideas before presenting the preferred conclusion:', 11.5, False, BODY, FONT),
        ('  "You might consider Option A, but it has bugs... therefore we recommend Option B."', 11.5, True, AMBER, FONT),
        ('• Statistical Association:', 13, True, GREEN, FONT),
        ('  Model weights associate later text positions with "winning conclusions" and consensus.', 11.5, False, CYAN, FONT),
    ]
    text_box(slide, RIGHT_X + 180000, ROW_Y + 520000, COL_W - 360000, ROW_H - 600000, right_pts, spacing=100)

    slide.notes_slide.notes_text_frame.text = SLIDE1_NOTES


def build_slide2(slide):
    # Clear placeholders & set dark background
    for ph in list(slide.placeholders):
        try: ph._element.getparent().remove(ph._element)
        except Exception: pass
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(BG_DARK)

    # Header
    pill = rect(slide, 731520, 320040, 1600000, 480000, GREEN)
    p = pill.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = 'BEST PRACTICES'; r.font.size = Pt(13); r.font.bold = True
    r.font.name = FONT; r.font.color.rgb = RGBColor.from_string('0F172A')

    text_box(slide, 2450000, 290000, 9000000, 548640, [
        ('Mitigating Order Bias in Evaluations', 31, True, WHITE, FONT)
    ], spacing=0)

    rect(slide, 731520, 920000, 3657600, 45000, BLUE, rounded=False)

    text_box(slide, 731520, 1020000, 10881360, 380000, [
        ('Essential techniques for LLM-as-a-Judge, offline evaluations, and comparative A/B testing prompts.', 14, False, MUTED, FONT)
    ], spacing=0)

    TOTAL_W = 10881360

    # Risk Alert Banner
    BANNER_Y = 1480000
    BANNER_H = 1350000
    rect(slide, 731520, BANNER_Y, TOTAL_W, BANNER_H, '2D1515', border_color='7F1D1D')

    text_box(slide, 731520 + 180000, BANNER_Y + 90000, TOTAL_W - 360000, 300000, [
        ('⚠️  The Production Risk: 60%–70% Positional Skew', 15.5, True, RED, FONT)
    ], spacing=0)

    risk_text = [
        ('When asking an LLM "Which response is better: Option A or Option B?", the model often selects the second option purely due to its placement! This introduces systematic evaluation skew in RAG offline evaluations and A/B benchmarking.', 12, False, BODY, FONT)
    ]
    text_box(slide, 731520 + 180000, BANNER_Y + 450000, TOTAL_W - 360000, BANNER_H - 520000, risk_text, spacing=100)

    # 3 Fix Cards Across
    CARDS_Y = BANNER_Y + BANNER_H + 180000
    CARDS_H = 3750000
    GAP = 220000
    CARD_W = (TOTAL_W - 2 * GAP) // 3

    fixes = [
        ('🔄  1. Position Swapping', 'Bidirectional Calibration', [
            ('• Run Both Orderings:', 12.5, True, GREEN, FONT),
            ('  Evaluate prompt as (A, B), then invert to (B, A).', 11.5, False, BODY, FONT),
            ('• Consensus Scoring:', 12.5, True, GREEN, FONT),
            ('  Accept the decision only if the same conceptual candidate wins in both runs.', 11.5, False, BODY, FONT),
            ('• Catch Ambiguity:', 12.5, True, GREEN, FONT),
            ('  If order flips the choice, mark as an uncertain Borderline / Tie.', 11.5, True, CYAN, FONT),
        ]),
        ('⛓️  2. Enforce Reasoning', 'CoT Before Selection', [
            ('• Delay the Decision:', 12.5, True, GREEN, FONT),
            ('  Never ask the model to state the winner in the opening sentence.', 11.5, False, BODY, FONT),
            ('• Structured Analysis:', 12.5, True, GREEN, FONT),
            ('  "List pros/cons of Option A, then Option B. Compare on Criteria X & Y. Then decide."', 11.5, False, BODY, FONT),
            ('• Attention Balancing:', 12.5, True, GREEN, FONT),
            ('  Self-generated tokens balance out raw input recency bias.', 11.5, True, CYAN, FONT),
        ]),
        ('🏷️  3. Neutral XML Framing', 'Anonymize Options', [
            ('• Avoid Numbered Lists:', 12.5, True, GREEN, FONT),
            ('  Numbers (1, 2) carry strong implicit sequence and priority bias.', 11.5, False, BODY, FONT),
            ('• Anonymized Tags:', 12.5, True, GREEN, FONT),
            ('  Wrap options in neutral XML: <candidate_alpha> and <candidate_beta>.', 11.5, False, BODY, FONT),
            ('• Clean Data Isolation:', 12.5, True, GREEN, FONT),
            ('  Separates user content from the evaluation rubric cleanly.', 11.5, True, CYAN, FONT),
        ]),
    ]

    for i, (title, subtitle, pts) in enumerate(fixes):
        cx = 731520 + i * (CARD_W + GAP)
        rect(slide, cx, CARDS_Y, CARD_W, CARDS_H, CARD_BG, border_color='1E293B')
        text_box(slide, cx + 160000, CARDS_Y + 120000, CARD_W - 320000, 300000, [
            (title, 15, True, BLUE, FONT),
            (subtitle, 11.5, True, AMBER, FONT)
        ], spacing=40)
        text_box(slide, cx + 160000, CARDS_Y + 540000, CARD_W - 320000, CARDS_H - 620000, pts, spacing=100)

    slide.notes_slide.notes_text_frame.text = SLIDE2_NOTES


def process_deck(path):
    print(f"Opening {path}...")
    prs = Presentation(path)

    # Check if slides already exist to avoid duplicate insertion
    existing = []
    for i, s in enumerate(prs.slides):
        for sh in s.shapes:
            if sh.has_text_frame:
                t = sh.text_frame.text.strip()
                if t in ['Order Sensitivity & Recency Bias', 'Mitigating Order Bias in Evaluations']:
                    existing.append(i)
                    break
    
    if len(existing) >= 2:
        print(f"Slides already exist at indices {existing}. Re-styling...")
        build_slide1(prs.slides[existing[0]])
        build_slide2(prs.slides[existing[1]])
        prs.save(path)
        print(f"Saved {path} successfully.")
        return

    # Find Slide 13 (which is Exercise 2). In 0-based index:
    # Let's find the slide that mentions 'Exercise 2' or 'Content Moderation & PII'
    target_idx = None
    for i, s in enumerate(prs.slides):
        for sh in s.shapes:
            if sh.has_text_frame and ('Exercise 2' in sh.text or 'Content Moderation & PII' in sh.text):
                target_idx = i
                break
        if target_idx is not None:
            break

    if target_idx is None:
        target_idx = 12 # Fallback to 13th slide (index 12)

    insert_pos = target_idx + 1
    print(f"Found Slide 13 at index {target_idx}. Inserting 2 new slides after index {target_idx} (insert_pos = {insert_pos})...")

    # Add 2 slides
    layout = prs.slides[0].slide_layout
    s1 = prs.slides.add_slide(layout)
    build_slide1(s1)

    s2 = prs.slides.add_slide(layout)
    build_slide2(s2)

    # Move them to insert_pos and insert_pos + 1
    xml_slides = prs.slides._sldIdLst
    slides_list = list(xml_slides)
    
    # s1 was added at -2, s2 at -1
    # Move s1
    xml_slides.remove(slides_list[-2])
    xml_slides.insert(insert_pos, slides_list[-2])
    
    # Re-fetch list
    slides_list = list(xml_slides)
    # Move s2
    xml_slides.remove(slides_list[-1])
    xml_slides.insert(insert_pos + 1, slides_list[-1])

    prs.save(path)
    print(f"Successfully inserted and styled 2 slides in {path} at positions {insert_pos+1} and {insert_pos+2}!")

if __name__ == '__main__':
    v2_path = Path(r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v2.pptx")
    v3_path = Path(r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v3.pptx")

    if v2_path.exists():
        process_deck(v2_path)
    if v3_path.exists():
        process_deck(v3_path)
