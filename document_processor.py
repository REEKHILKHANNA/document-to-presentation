from PyPDF2 import PdfReader
from pathlib import Path
import re

class DocumentProcessor:
    """Extract text and content from PDF and TXT documents"""
    
    def __init__(self, max_pages=12):
        self.max_pages = max_pages
    
    def extract_content(self, file_path):
        """Auto-detect file type and extract content"""
        file_path = Path(file_path)
        
        print(f"   Reading: {file_path.name}")
        print(f"   Full path: {file_path.absolute()}\n")
        
        if not file_path.exists():
            print(f"   ERROR: File not found!")
            return []
        
        if file_path.suffix.lower() == '.pdf':
            print(f"   File type: PDF")
            return self.extract_from_pdf(str(file_path))
        elif file_path.suffix.lower() == '.txt':
            print(f"   File type: Text (TXT)")
            return self.extract_from_txt(str(file_path))
        else:
            print(f"   ERROR: Unsupported file type: {file_path.suffix}")
            return []
    
    def extract_from_pdf(self, pdf_path):
        """Extract text content from PDF"""
        pages_content = []
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                total_pages = len(reader.pages)
                
                print(f"   Total pages in PDF: {total_pages}")
                
                for page_num, page in enumerate(reader.pages[:self.max_pages]):
                    try:
                        text = page.extract_text()
                        pages_content.append({
                            "page_num": page_num + 1,
                            "content": text if text else "[No text content]"
                        })
                        print(f"   OK Extracted page {page_num + 1}/{min(total_pages, self.max_pages)}")
                    except Exception as e:
                        pages_content.append({
                            "page_num": page_num + 1,
                            "content": "[Error extracting text]"
                        })
        
        except FileNotFoundError:
            print(f"   ERROR: File not found: {pdf_path}")
            return []
        except Exception as e:
            print(f"   ERROR: {str(e)}")
            return []
        
        return pages_content
    
    def extract_from_txt(self, txt_path):
        """Extract TXT file and parse SLIDE sections"""
        pages_content = []
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                full_text = file.read()
            
            print(f"   File size: {len(full_text)} characters")
            
            slide_pattern = r'SLIDE\s+(\d+)\s*[-–—]\s*([^\n]+)'
            
            slides = re.finditer(slide_pattern, full_text, re.IGNORECASE)
            slide_list = list(slides)
            
            if slide_list:
                print(f"   Found {len(slide_list)} SLIDE sections")
                
                for idx, match in enumerate(slide_list):
                    slide_num = int(match.group(1))
                    slide_title = match.group(2).strip()
                    
                    start_pos = match.end()
                    
                    if idx + 1 < len(slide_list):
                        end_pos = slide_list[idx + 1].start()
                    else:
                        end_pos = len(full_text)
                    
                    slide_content = full_text[start_pos:end_pos].strip()
                    
                    pages_content.append({
                        "page_num": slide_num,
                        "title": slide_title,
                        "content": slide_content[:10000]
                    })
                    
                    print(f"   OK Extracted SLIDE {slide_num}: {slide_title}")
            else:
                print(f"   No SLIDE sections found, treating entire file as content")
                pages_content.append({
                    "page_num": 1,
                    "title": "Document Content",
                    "content": full_text[:10000]
                })
        
        except FileNotFoundError:
            print(f"   ERROR: File not found: {txt_path}")
            return []
        except Exception as e:
            print(f"   ERROR: {str(e)}")
            return []
        
        return pages_content
    
    def get_key_pages(self, content, key_page_numbers=None):
        """Get specific pages for slide generation"""
        if key_page_numbers is None:
            key_page_numbers = [page['page_num'] for page in content]
        
        key_content = []
        
        for page in content:
            if page['page_num'] in key_page_numbers:
                key_content.append(page)
        
        print(f"   OK Selected {len(key_content)} slides for generation")
        return key_content