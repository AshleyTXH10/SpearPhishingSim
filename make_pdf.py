from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.actions import JavaScript
from pypdf.generic import DictionaryObject, NameObject, TextStringObject

base_dir = Path(__file__).parent
input_pdf = base_dir / "Game On, Dreamers!.pdf"
output_pdf = base_dir / "output_with_js.pdf"

if not input_pdf.exists():
    raise FileNotFoundError(f"Could not find input PDF: {input_pdf}")

writer = PdfWriter(clone_from=str(input_pdf))

js_code = (
    'console.println("[SIMULATION] Document JavaScript triggered.");'
    'app.alert("SIMULATED PHISHING ALERT: Automatic PDF JavaScript triggered.");'
)

js_action = JavaScript(js_code)
writer.add_open_action(js_action)

# Fallback: ensure /OpenAction is explicitly attached to the root catalog
if NameObject("/OpenAction") not in writer._root_object:
    action_ref = writer._add_object(
        DictionaryObject({
            NameObject("/S"): NameObject("/JavaScript"),
            NameObject("/JS"): TextStringObject(js_code),
        })
    )
    writer._root_object[NameObject("/OpenAction")] = action_ref

with open(output_pdf, "wb") as f:
    writer.write(f)

reader = PdfReader(str(output_pdf))
root = reader.trailer["/Root"]
print("Root keys:", list(root.keys()))
if "/OpenAction" in root:
    print("OpenAction:", root["/OpenAction"].get_object())
else:
    print("Warning: /OpenAction still missing")