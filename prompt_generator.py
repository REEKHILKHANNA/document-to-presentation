class PromptGenerator:
    """Convert document content into Gemini prompts for infographic generation"""
    
    def __init__(self):
        self.slide_templates = {
            2: "systems_landscape",
            3: "process_flow",
            4: "risk_matrix",
            8: "future_vision",
            9: "comparison",
            12: "transformation_summary"
        }
    
    def generate_prompts(self, content, num_slides=5):
        """Generate slide prompts from PDF content"""
        slides = []
        
        for i, page in enumerate(content[:num_slides]):
            page_num = page['page_num']
            content_text = page['content'][:1000]
            
            template = self.slide_templates.get(page_num, "generic_infographic")
            
            infographic_data = self._create_infographic_prompt(
                page_num,
                content_text,
                template,
                slide_number=i+1
            )
            
            slides.append(infographic_data)
        
        return slides
    
    def _create_infographic_prompt(self, page_num, content, template, slide_number):
        """Create infographic data structure for Gemini generation"""
        
        templates = {
            "systems_landscape": {
                "title": "Current Landscape: Disparate Systems",
                "type": "diagram",
                "description": content,
                "special_notes": "Show 4 system boxes: OSN/S-NET, I-NET, MCC, Standalone with icons and tools"
            },
            "process_flow": {
                "title": "The AS-IS Process: 9-Stage Journey",
                "type": "swimlane",
                "description": content,
                "special_notes": "Create swimlane diagram with 7 roles and 9 process steps"
            },
            "risk_matrix": {
                "title": "Complexity Creates Friction and Risk",
                "type": "risk_visualization",
                "description": content,
                "special_notes": "Show risk matrix with stages and indicators"
            },
            "future_vision": {
                "title": "The Future State: Integrated Ecosystem",
                "type": "diagram",
                "description": content,
                "special_notes": "Create 5-stage flow with icons"
            },
            "comparison": {
                "title": "From Drag to Efficiency",
                "type": "comparison",
                "description": content,
                "special_notes": "Show before vs after"
            },
            "transformation_summary": {
                "title": "The Transformation",
                "type": "transformation",
                "description": content,
                "special_notes": "Show transformation arrows"
            }
        }
        
        template_data = templates.get(template, templates["future_vision"])
        
        return {
            "title": template_data["title"],
            "type": template_data["type"],
            "content": template_data["description"],
            "special_instructions": template_data["special_notes"],
            "page_number": page_num,
            "slide_number": slide_number,
            "colors": "professional blue, green, red, orange",
            "design_level": "PREMIUM - Kimi-quality professional",
            "resolution": "2K (2752x1536)",
        }
