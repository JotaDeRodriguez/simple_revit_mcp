from pyrevit import routes, revit, DB

doc = revit.doc

api = routes.API('simple-mcp-api')


@api.route('/status/')
def api_status():
    """Return API status to check if it's registered"""
    return routes.make_response(data={
        "status": "active",
        "api_name": "simple-mcp-api"
    })

    
@api.route('/model/summary/')
def get_model_summary(doc):
    """Get summary information about the model"""

    # Create empty summary
    summary = {
        "name": doc.Title,
        "elements": [],
        "views": []
    }
    
    # Collect model data
    elements = DB.FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

    for element in elements:
        try:
            # Try to get name - different element types might store names differently
            name = element.Name
            if name:
                summary["elements"].append(name)
        except:
            # Skip elements without accessible names
            pass

    # Views
    views = DB.FilteredElementCollector(doc)\
        .OfCategory(DB.BuiltInCategory.OST_Views)\
        .ToElements()

    # Add view names to summary
    summary["views"] = [view.Name for view in views]
        
    
    return routes.make_response(data=summary)