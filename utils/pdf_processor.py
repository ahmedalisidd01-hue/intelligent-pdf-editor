
import fitz  # PyMuPDF
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
from PIL import Image
import tempfile

class PDFProcessor:
    def __init__(self):
        self.doc = None
        
    def extract_text_with_positions(self, pdf_path):
        """Extract text with positions and formatting information"""
        try:
            doc = fitz.open(pdf_path)
            text_data = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_instances = page.get_text("dict")
                
                for block in text_instances["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text_data.append({
                                    "text": span["text"],
                                    "page": page_num,
                                    "bbox": span["bbox"],
                                    "font": span["font"],
                                    "size": span["size"],
                                    "color": span["color"]
                                })
            
            doc.close()
            return text_data
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    def find_text_position(self, text_data, target_text):
        """Find the position of specific text in the document"""
        matches = []
        for item in text_data:
            if target_text.lower() in item["text"].lower():
                matches.append(item)
        return matches
    
    def replace_text(self, pdf_path, output_path, old_text, new_text):
        """Replace specific text in the PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_instances = page.search_for(old_text)
                
                for inst in text_instances:
                    # Add redaction and then add new text
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()
                    
                    # Add new text in similar position
                    rect = fitz.Rect(inst.x0, inst.y0, inst.x1, inst.y1)
                    page.insert_text(rect.bl, new_text, fontsize=11)
            
            doc.save(output_path)
            doc.close()
            return True
        except Exception as e:
            raise Exception(f"Error replacing text: {str(e)}")
    
    def highlight_text(self, pdf_path, output_path, text_to_highlight):
        """Highlight specific text in the PDF"""
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_instances = page.search_for(text_to_highlight)
                
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors({"stroke": (1, 1, 0)})  # Yellow highlight
                    highlight.update()
            
            doc.save(output_path)
            doc.close()
            return True
        except Exception as e:
            raise Exception(f"Error highlighting text: {str(e)}")
    
    def extract_full_text(self, pdf_path):
        """Extract all text from PDF for LLM processing"""
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_text += page.get_text() + "\\n\\n"
            
            doc.close()
            return full_text
        except Exception as e:
            raise Exception(f"Error extracting full text: {str(e)}")
EOL