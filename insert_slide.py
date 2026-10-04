import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Fix for pptx collections issue
setattr(collections, 'Mapping', collections.abc.Mapping)
setattr(collections, 'Sequence', collections.abc.Sequence)
setattr(collections, 'Container', collections.abc.Container)

ppt_path = r"d:\My work\workshop\prompt-engineering-workshop\materials\Prompt_Engineering_Workshop_v2.pptx"
prs = Presentation(ppt_path)

# Determine the layout to use. Blank or Title and Content.
# Index 1 usually is "Title and Content", let's check layouts.
layout = prs.slide_layouts[1] # Usually title and content

# Create the new slide at the end
new_slide = prs.slides.add_slide(layout)

# 1. Set Title
if new_slide.shapes.title:
    new_slide.shapes.title.text = "API Parameter: stop_sequences"

# 2. Set Content
for shape in new_slide.shapes:
    if shape.has_text_frame and shape != new_slide.shapes.title:
        tf = shape.text_frame
        tf.clear()
        
        p = tf.paragraphs[0]
        p.text = "A parameter (array of strings) that tells the model: 'Stop generating text immediately if you hit any of these words.'"
        p.font.size = Pt(24)
        p.font.bold = True
        
        p2 = tf.add_paragraph()
        p2.text = "Top Use Cases:"
        p2.font.size = Pt(22)
        p2.level = 0
        
        p3 = tf.add_paragraph()
        p3.text = "1. Extracting Structured Data: Stop at </result> or } to prevent the model from adding chit-chat after the data."
        p3.font.size = Pt(20)
        p3.level = 1
        
        p4 = tf.add_paragraph()
        p4.text = "2. Limiting Formats: Stop at ``` to ensure the model only outputs a single code block."
        p4.font.size = Pt(20)
        p4.level = 1
        
        p5 = tf.add_paragraph()
        p5.text = "3. Controlling Length: If you want exactly 5 items, use \"6.\" as a stop sequence."
        p5.font.size = Pt(20)
        p5.level = 1

        p6 = tf.add_paragraph()
        p6.text = "Example Payload (Claude API):"
        p6.font.size = Pt(22)
        p6.level = 0

# Add a text box for the code snippet to make it stand out like a code block
txBox = new_slide.shapes.add_textbox(Inches(1), Inches(5), Inches(8), Inches(2))
tf = txBox.text_frame
tf.word_wrap = True

p_code = tf.paragraphs[0]
p_code.text = (
    "{\n"
    "  \"model\": \"claude-3-opus-20240229\",\n"
    "  \"messages\": [{\"role\": \"user\", \"content\": \"List 5 planets:\"}],\n"
    "  \"stop_sequences\": [\"6.\", \"</list>\"]\n"
    "}"
)
p_code.font.size = Pt(18)
p_code.font.name = 'Courier New'

# Now move the slide to index 17 (right after slide 16)
xml_slides = prs.slides._sldIdLst
slides = list(xml_slides)
xml_slides.remove(slides[-1])
xml_slides.insert(17, slides[-1])

prs.save(ppt_path.replace("v2", "v3"))
print("Slide inserted successfully as v3!")
