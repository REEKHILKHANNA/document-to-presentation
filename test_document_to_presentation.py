"""
TEST: Document-to-Presentation Converter
Reads from: input/ folder
Writes to: output/ folder
Supports both PDF and TXT files
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Import our modules
from document_processor import DocumentProcessor
from prompt_generator import PromptGenerator
from nano_banana_infographic_generator import GeminiInfographicGenerator

def main():
    print(f"\n{'='*80}")
    print("📊 DOCUMENT-TO-PRESENTATION CONVERTER")
    print(f"{'='*80}\n")
    
    # Create input and output folders if they don't exist
    input_folder = Path("input")
    output_folder = Path("output")
    
    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)
    
    print(f"Input folder:  {input_folder.absolute()}")
    print(f"Output folder: {output_folder.absolute()}\n")
    
    # Check API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not set!")
        print("   Please set your API key: export GEMINI_API_KEY=your_key")
        return False
    
    print("✓ API Key found\n")
    
    # Step 1: Find Input File (PDF or TXT)
    print(f"{'─'*80}")
    print("STEP 1: Looking for document in 'input/' folder")
    print(f"{'─'*80}\n")
    
    # Look for PDF or TXT files in input folder
    pdf_files = list(input_folder.glob("*.pdf"))
    txt_files = list(input_folder.glob("*.txt"))
    
    input_file = None
    
    if pdf_files:
        input_file = pdf_files[0]
        print(f"✓ Found PDF: {input_file.name}")
    elif txt_files:
        input_file = txt_files[0]
        print(f"✓ Found TXT: {input_file.name}")
    else:
        print("❌ ERROR: No PDF or TXT files found in 'input/' folder!")
        print(f"   Please add a document to: {input_folder.absolute()}/")
        return False
    
    print()
    
    # Step 2: Extract Content
    print(f"{'─'*80}")
    print("STEP 2: Extracting content from document")
    print(f"{'─'*80}\n")
    
    processor = DocumentProcessor()
    all_content = processor.extract_content(str(input_file))
    
    if not all_content:
        print("❌ ERROR: Could not extract content from document")
        return False
    
    print()
    
    # Get all content
    key_content = processor.get_key_pages(all_content)
    
    if not key_content:
        print("❌ ERROR: Could not find key sections")
        return False
    
    print(f"\n✓ Extracted {len(key_content)} slides/sections\n")
    
    # Step 3: Generate Slide Prompts
    print(f"{'─'*80}")
    print("STEP 3: Generating slide prompts from content")
    print(f"{'─'*80}\n")
    
    prompt_gen = PromptGenerator()
    slide_prompts = prompt_gen.generate_prompts(key_content, num_slides=len(key_content))
    
    print(f"✓ Generated {len(slide_prompts)} slide prompts:\n")
    
    for slide in slide_prompts:
        print(f"   Slide {slide['slide_number']}: {slide['title']}")
    
    print(f"\n✓ Ready for Gemini generation\n")
    
    # Step 4: Generate Infographics
    print(f"{'─'*80}")
    print("STEP 4: Generating infographics with Gemini")
    print(f"{'─'*80}\n")
    
    cost_per_slide = 0.07
    total_estimated_cost = len(slide_prompts) * cost_per_slide
    
    print(f"Number of slides: {len(slide_prompts)}")
    print(f"Cost per slide: ${cost_per_slide:.2f}")
    print(f"Estimated total cost: ${total_estimated_cost:.2f}\n")
    print("Generating slides...\n")
    
    # Initialize generator
    generator = GeminiInfographicGenerator()
    
    # Convert prompts to infographic format
    infographics = []
    for slide in slide_prompts:
        infographic = {
            "title": slide['title'],
            "type": slide['type'],
            "content": slide['content'],
            "colors": slide['colors'],
            "special_instructions": slide['special_instructions'],
        }
        infographics.append(infographic)
    
    # Generate output filename
    output_filename = f"Generated_from_{input_file.stem}.pptx"
    output_path = output_folder / output_filename
    
    # Generate presentation
    result_path = generator.process(
        infographics=infographics,
        output_path=str(output_path),
        use_cache=True
    )
    
    if not result_path or not os.path.exists(result_path):
        print("\n❌ ERROR: Failed to generate presentation")
        return False
    
    # Step 5: Summary
    print(f"\n{'='*80}")
    print("✅ SUCCESS! Presentation generated!")
    print(f"{'='*80}\n")
    
    file_size_mb = os.path.getsize(result_path) / (1024 * 1024)
    
    print(f"Input file:  {input_file.name}")
    print(f"Output file: {output_path.name}")
    print(f"Location:    {output_path.absolute()}")
    print(f"File size:   {file_size_mb:.2f} MB")
    print(f"Total slides: {len(slide_prompts)}")
    print(f"Estimated cost: ${total_estimated_cost:.2f}")
    print(f"Resolution: 2K (2752×1536)")
    print(f"Quality: Gemini 3 Pro Image Preview")
    print(f"\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'='*80}\n")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)