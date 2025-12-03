import os
from pathlib import Path

class PromptGenerator:
    """Generate prompts for creating infographics using templates"""
    
    def __init__(self, template_name='professional'):
        self.template_name = template_name
        self.template_content = self.load_template(template_name)
    
    def load_template(self, template_name):
        template_path = Path('templates') / f'{template_name}.txt'
        
        if not template_path.exists():
            print(f"WARNING: Template '{template_name}' not found!")
            return self.get_default_template()
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"ERROR reading template: {e}")
            return self.get_default_template()
    
    def get_default_template(self):
        return "Professional consulting style slide"
    
    def generate_prompts(self, content, num_slides=None):
        """Generate prompts using the selected template"""
        
        if num_slides is None:
            num_slides = len(content)
        
        prompts = []
        
        for slide in content[:num_slides]:
            slide_num = slide.get('page_num', 1)
            title = slide.get('title', 'Slide')
            slide_content = slide.get('content', '')
            
            # DIFFERENT prompts based on template
            if self.template_name == 'professional':
                prompt = f"""
You are a professional consulting slide designer (McKinsey/BCG style).

Create a SINGLE professional slide image with EXACTLY these requirements:

COLORS TO USE (MANDATORY):
- Navy Blue (#1F4E78) for title and headers
- Charcoal Gray (#4A4A4A) for body text
- White (#FFFFFF) for background
- Light Gray (#E8E8E8) for subtle elements
- Teal (#2E8B9E) for accents ONLY
- ABSOLUTELY NO OTHER COLORS

STYLE (MANDATORY):
✓ Flat design (NO 3D, NO shadows, NO gradients)
✓ Minimal text, MAXIMUM white space
✓ Professional sans-serif font
✓ Clean geometric shapes only
✓ Executive appearance
✓ Similar to McKinsey/BCG presentations

SLIDE LAYOUT:
Title: {title}
Content: {slide_content}

Create a clean, professional slide with navy blue title, gray text, white background, and lots of empty space.
Resolution: 2752x1536 (2K, 16:9)
"""
            
            elif self.template_name == 'colorful':
                prompt = f"""
You are a modern, vibrant slide designer (Airbnb/Startup style).

Create a SINGLE colorful slide image with EXACTLY these requirements:

COLORS TO USE (MANDATORY - USE MANY COLORS):
- Electric Blue (#0066FF)
- Hot Pink (#FF1493)
- Bright Green (#00CC00)
- Sunny Yellow (#FFD700)
- Orange (#FF6600)
- Purple (#9900FF)
- MIX MULTIPLE COLORS - NOT MONOTONE!

STYLE (MANDATORY):
✓ Bold and vibrant design
✓ Modern and trendy
✓ Dynamic layouts
✓ Colorful shapes and icons
✓ Large, impactful text
✓ Fun and energetic
✓ Similar to Airbnb or modern startups

SLIDE LAYOUT:
Title: {title}
Content: {slide_content}

Create a BRIGHT, COLORFUL slide with multiple vibrant colors, bold fonts, and energetic design.
Resolution: 2752x1536 (2K, 16:9)
"""
            
            elif self.template_name == 'minimal':
                prompt = f"""
You are a minimalist slide designer (Apple/Google style).

Create a SINGLE minimal slide image with EXACTLY these requirements:

COLORS TO USE (MANDATORY - MINIMAL COLORS ONLY):
- Black (#000000) for text and essential elements
- White (#FFFFFF) for background
- Light Gray (#F5F5F5) for subtle elements
- ONE accent color ONLY: Blue (#0066CC)
- NO OTHER COLORS ALLOWED

STYLE (MANDATORY):
✓ Maximum white space (50%+ of slide)
✓ Minimal text - only essential information
✓ Clean lines and simple shapes
✓ NO decorations or unnecessary elements
✓ Sophisticated simplicity
✓ Similar to Apple or Google design

SLIDE LAYOUT:
Title: {title}
Content: {slide_content}

Create a CLEAN, MINIMAL slide with mostly white space, black text, simple design, and one accent color.
Resolution: 2752x1536 (2K, 16:9)
"""
            
            else:
                prompt = f"""
Create a professional slide:
Title: {title}
Content: {slide_content}
Resolution: 2752x1536 (2K, 16:9)
"""
            
            # DEBUG: Print what we're sending
            print(f"\n{'='*80}")
            print(f"SLIDE {slide_num} - {self.template_name.upper()} STYLE")
            print(f"{'='*80}")
            print(f"Title: {title}")
            print(f"\nPrompt being sent to Gemini:")
            print(f"{prompt[:300]}...")
            print(f"{'='*80}\n")
            
            prompts.append({
                'slide_number': slide_num,
                'title': title,
                'type': self.template_name,
                'content': slide_content,
                'prompt': prompt,
                'template': self.template_name,
                'design_level': f'Professional - {self.template_name.capitalize()} style'
            })
        
        return prompts
