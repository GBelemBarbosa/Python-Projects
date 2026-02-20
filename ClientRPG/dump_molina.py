import docx
import sys

def dump_docx():
    doc = docx.Document('Molina.docx')
    with open('molina_dump.txt', 'w', encoding='utf-8') as f:
        for p in doc.paragraphs:
            f.write(p.text + '\n')

if __name__ == "__main__":
    dump_docx()
