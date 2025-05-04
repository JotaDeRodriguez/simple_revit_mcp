

def sanitize_name(name):
    """Sanitize element name to ensure it can be encoded properly in JSON"""
    if not name:
        return ""
    
    # Replace problematic characters or convert to ASCII only if needed
    try:
        # Try to encode and decode as UTF-8 to catch any encoding issues
        return name.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
    except Exception:
        # If all else fails, remove non-ASCII characters
        return ''.join(c for c in name if ord(c) < 128)