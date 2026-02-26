import docx
doc = docx.Document('Cantrips.docx')
with open('guidance_dump.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(doc.paragraphs[1360:1400]):
        f.write(f"{i+1360} {repr(p.text)}\n")
