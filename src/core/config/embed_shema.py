import os
import json

def embed_schema_in_vscode(schema_path):
    vscode_folder = os.path.join(os.getcwd(), ".vscode")
    if not os.path.exists(vscode_folder):
        os.makedirs(vscode_folder)
    
    vscode_settings_path = os.path.join(vscode_folder, "settings.json")
    settings = {}
    
    if os.path.exists(vscode_settings_path):
        with open(vscode_settings_path, "r") as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                print("Failed to load settings.json")
                return
    
    json_schemas = settings.get("json.schemas", [])
    schema_entry = {
        "fileMatch": [".plang"],
        "url": schema_path
    }
    
    if schema_entry not in json_schemas:
        json_schemas.append(schema_entry)
        settings["json.schemas"] = json_schemas
    
    with open(vscode_settings_path, "w") as f:
        json.dump(settings, f, indent=4)
        
if __name__ == "__main__":
    embed_schema_in_vscode("./src/core/config/config_schema.json")
        