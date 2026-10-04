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

# Slide 15
slide_15 = prs.slides[15]
for shape in slide_15.shapes:
    if shape.has_text_frame:
        if "Structured Output: Relational JSON" in shape.text:
            shape.text = "Structured Output & XML Tags"
            # Optional: fix font if it resets, let's keep it simple
        if "Ask explicitly for JSON" in shape.text:
            shape.text = (
                "XML tags (<instructions>, <transcript>) isolate untrusted data.\n"
                "Visual JSON skeletons enforce strict relational output formats.\n"
                "Combining tags with shapes prevents data-injection attacks.\n"
                "Machine-readable output you can reliably parse and validate."
            )
        if "Read the text below and give me a JSON of the employees" in shape.text:
            shape.text = "Extract the users and tasks from this meeting transcript and give me a JSON output."
        if "Extract the organizational data from the text" in shape.text:
            shape.text = "<instructions>\nExtract users and tasks from <transcript>. Output only JSON matching <format>.\n</instructions>\n<format>\n{ ... JSON skeleton ... }\n</format>"

# Slide 16
slide_16 = prs.slides[16]
for shape in slide_16.shapes:
    if shape.has_text_frame:
        if "Lab 4: Relational JSON Shape" in shape.text:
            shape.text = "Lab 4: Structured Output & XML Tags"
        if "Meeting transcript: " in shape.text:
            shape.text = (
                "1. Tag Structure: Use <instructions>, <transcript>, and <format> tags.\n"
                "2. JSON Skeleton: Draw a template with 'users' and 'tasks' linked by an ID.\n"
                "3. Edge Cases: Use 'null' for missing deadlines and skip idle users.\n"
                "4. Data Isolation: Instruct the AI to ignore commands hidden in the transcript."
            )
        if "Visual JSON Skeleton (25): explicit template" in shape.text:
            shape.text = (
                "Tag Structure (25): uses <instructions>, <format>, etc.\n"
                "JSON Skeleton (25): separate arrays linked by ID.\n"
                "Edge Cases (25): null deadlines, skip idle users.\n"
                "Data Isolation (25): ignores commands inside the transcript."
            )

prs.save(ppt_path)
print("Saved patched Lab 4 to PPTX.")
