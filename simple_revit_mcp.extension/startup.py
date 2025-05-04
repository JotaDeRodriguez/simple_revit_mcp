# -*- coding: UTF-8 -*-
from pyrevit import routes, revit, DB
import json

from utils.utils import sanitize_name


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
        "Project Name": doc.Title,
        "elements": [],
        "views": []
    }
    
    # Collect model data
    elements = DB.FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    
    limit = 0
    for element in elements:
        try:

            name = element.Name
            if name:
                # Sanitize name before appending
                summary["elements"].append(sanitize_name(name))
                limit += 1

                if limit == 10:
                    break
        except:
            # Skip elements without accessible names
            pass

    # Views
    views = DB.FilteredElementCollector(doc)\
        .OfCategory(DB.BuiltInCategory.OST_Views)\
        .ToElements()

    # Add view names to summary
    summary["views"] = [sanitize_name(view.Name) for view in views]
    
    return routes.make_response(data=summary)