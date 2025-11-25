def sections_to_html(sections: list[dict], h1: str) -> str:
    html_parts = [f"<h1>{h1}</h1>"]
    
    for section in sections:
        level = section.get("level", 2)
        heading = section.get("heading", "")
        content = section.get("content", "")
        
        if heading:
            html_parts.append(f"<h{level}>{heading}</h{level}>")
        
        paragraphs = content.split("\n\n")
        for para in paragraphs:
            if para.strip():
                html_parts.append(f"<p>{para.strip()}</p>")
    
    return "\n".join(html_parts)


def sections_to_text(sections: list[dict], h1: str) -> str:
    text_parts = [h1 + "\n"]
    
    for section in sections:
        heading = section.get("heading", "")
        content = section.get("content", "")
        level = section.get("level", 2)
        
        if heading:
            prefix = "#" * level
            text_parts.append(f"\n{prefix} {heading}\n")
        
        text_parts.append(content)
    
    return "\n".join(text_parts)

