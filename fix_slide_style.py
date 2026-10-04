import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# Fix for pptx collections issue
setattr(collections, 'Mapping', collections.abc.Mapping)
setattr(collections, 'Sequence', collections.abc.Sequence)
setattr(collections, 'Container', collections.abc.Container)

# Load v2 instead to start fresh and avoid the duplicate warning
ppt_path_src = r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v2.pptx"
ppt_path_dst = r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v3.pptx"

prs = Presentation(ppt_path_src)

# Add a Blank Slide
blank_layout = prs.slide_layouts[6]
new_slide = prs.slides.add_slide(blank_layout)

# 1. Title Box
title_box = new_slide.shapes.add_textbox(Emu(731520), Emu(365760), Emu(10058400), Emu(640080))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = "API Parameter: stop_sequences"
p.font.name = "Segoe UI"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = RGBColor(0, 0, 0)

# 2. Title Line
# Slide 28 had T: 1005840
line = new_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(731520), Emu(1005840), Emu(4572000), Emu(50800))
line.fill.solid()
line.fill.fore_color.rgb = RGBColor(166, 166, 166) # nice gray line
line.line.fill.background()

# 3. Content Text
content_box = new_slide.shapes.add_textbox(Emu(731520), Emu(1200000), Emu(10058400), Emu(3000000))
tf = content_box.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "A parameter (array of strings) that tells the model: 'Stop generating text immediately if you hit any of these words.'"
p1.font.name = "Segoe UI"
p1.font.size = Pt(24)
p1.font.bold = True
p1.font.color.rgb = RGBColor(0, 0, 0)

p2 = tf.add_paragraph()
p2.text = "Top Use Cases:"
p2.font.name = "Segoe UI"
p2.font.size = Pt(22)
p2.font.color.rgb = RGBColor(0, 0, 0)
p2.space_before = Pt(14)

p3 = tf.add_paragraph()
p3.text = "1. Extracting Structured Data: Stop at </result> or } to prevent the model from adding chit-chat after the data."
p3.font.name = "Segoe UI"
p3.font.size = Pt(20)
p3.font.color.rgb = RGBColor(50, 50, 50)
p3.level = 1
p3.space_before = Pt(6)

p4 = tf.add_paragraph()
p4.text = "2. Limiting Formats: Stop at ``` to ensure the model only outputs a single code block."
p4.font.name = "Segoe UI"
p4.font.size = Pt(20)
p4.font.color.rgb = RGBColor(50, 50, 50)
p4.level = 1
p4.space_before = Pt(6)

p5 = tf.add_paragraph()
p5.text = "3. Controlling Length: If you want exactly 5 items, use \"6.\" as a stop sequence."
p5.font.name = "Segoe UI"
p5.font.size = Pt(20)
p5.font.color.rgb = RGBColor(50, 50, 50)
p5.level = 1
p5.space_before = Pt(6)

p6 = tf.add_paragraph()
p6.text = "Example Payload (Claude API):"
p6.font.name = "Segoe UI"
p6.font.size = Pt(22)
p6.font.color.rgb = RGBColor(0, 0, 0)
p6.space_before = Pt(14)


# 4. Code Block Box
code_box = new_slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(731520), Emu(4200000), Emu(7000000), Emu(1600000))
code_box.fill.solid()
code_box.fill.fore_color.rgb = RGBColor(245, 245, 245) # light gray
code_box.line.color.rgb = RGBColor(200, 200, 200)

tf2 = code_box.text_frame
tf2.word_wrap = True
tf2.margin_left = Inches(0.2)
tf2.margin_top = Inches(0.2)

code_p = tf2.paragraphs[0]
code_p.text = (
    "{\n"
    "  \"model\": \"claude-3-opus-20240229\",\n"
    "  \"messages\": [{\"role\": \"user\", \"content\": \"List 5 planets:\"}],\n"
    "  \"stop_sequences\": [\"6.\", \"</list>\"]\n"
    "}"
)
code_p.font.name = "Courier New"
code_p.font.size = Pt(16)
code_p.font.color.rgb = RGBColor(50, 50, 50)
code_p.alignment = PP_ALIGN.LEFT

# Move slide to index 17
xml_slides = prs.slides._sldIdLst
slides = list(xml_slides)
xml_slides.remove(slides[-1])
xml_slides.insert(17, slides[-1])

prs.save(ppt_path_dst)
print("Fresh v3 created successfully with better styles!")
