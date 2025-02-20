import ast
import fnmatch
import json
import os
import sys

def parse_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    result = {
        "classes": {},
        "functions": {},
        "variables": []
    }
    
    def set_parents(node, parent=None):
        node.parent = parent
        for child in ast.iter_child_nodes(node):
            set_parents(child, node)
    
    set_parents(tree)

    def get_value_info(value):
        """Determine the value and type of a variable"""
        if isinstance(value, ast.Constant):  # Handles literals (str, int, float, bool, None)
            if isinstance(value.value, bool):  # Explicit bool check
                return value.value, "bool"
            return value.value, type(value.value).__name__
        
        elif isinstance(value, ast.Name):  # Variable assigned from another variable
            return value.id, "unknown (assigned from another variable)"  # Mark as unknown instead of "variable"
        
        elif isinstance(value, ast.List):
            return "List", "list"
        
        elif isinstance(value, ast.Tuple):
            return "Tuple", "tuple"
        
        elif isinstance(value, ast.Dict):
            return "Dict", "dict"
        
        elif isinstance(value, ast.Set):
            return "Set", "set"
        
        elif isinstance(value, ast.Call):  # Function or class instantiation
            if isinstance(value.func, ast.Name):
                return f"Instance of {value.func.id}", value.func.id  # Class instantiation
            elif isinstance(value.func, ast.Attribute):
                return f"Method call {value.func.attr}", "Unknown"
        
        return "Unknown", "Unknown"




    def get_param_info(args, kwonlyargs, defaults, kw_defaults):
        """Extract parameter names and their types"""
        param_info = []

        def extract_params(param_list, default_list):
            for i, arg in enumerate(param_list):
                param_name = arg.arg
                param_type = "Unknown"
                if arg.annotation:
                    param_type = ast.unparse(arg.annotation)  # Get type annotation if present
                param_info.append({"name": param_name, "type": param_type})

        extract_params(args, defaults)  # Positional arguments
        extract_params(kwonlyargs, kw_defaults)  # Keyword-only arguments

        return param_info



    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            docstring = ast.get_docstring(node)
            methods = {}
            
            for f in node.body:
                if isinstance(f, ast.FunctionDef):
                    params = get_param_info(f.args.args, f.args.kwonlyargs, f.args.defaults, f.args.kw_defaults)
                    
                    if f.name[0] == "_" and f.name != "__init__":
                        continue

                    return_type = ast.unparse(f.returns) if f.returns else "Unknown"
                    methods[f.name] = {
                        "docstring": ast.get_docstring(f),
                        "params": params,
                        "return": return_type
                    }
                    
                    # Special handling for __init__ method
                    if f.name == "__init__":
                        init_variables = []
                        for stmt in f.body:
                            if isinstance(stmt, ast.Assign):
                                for target in stmt.targets:
                                    if isinstance(target, ast.Attribute):  # self.variable
                                        var_name = target.attr
                                        if var_name[0] == "_":
                                            continue
                                        is_constant = var_name.isupper()
                                        initial_value, value_type = get_value_info(stmt.value)
                                        
                                        init_variables.append({
                                            "name": var_name,
                                            "constant": is_constant,
                                            "initial_value": initial_value,
                                            "type": value_type
                                        })
                            elif isinstance(stmt, ast.AnnAssign):
                                target = stmt.target
                                if isinstance(target, ast.Attribute):  # self.variable
                                    var_name = target.attr
                                    if var_name[0] == "_":
                                        continue
                                    is_constant = var_name.isupper()
                                    value, var_type = get_value_info(stmt.value)
                                    annotated_type = ast.unparse(stmt.annotation) if stmt.annotation else "Unknown"
                                    
                                    init_variables.append({
                                        "name": var_name,
                                        "constant": is_constant,
                                        "initial_value": value,
                                        "type": annotated_type if annotated_type != "Unknown" else var_type,  # Prefer annotation type
                                    })
                              
                        methods[f.name]["init_variables"] = init_variables
            
            result["classes"][class_name] = {
                "docstring": docstring,
                "methods": methods
            }
        
        elif isinstance(node, ast.FunctionDef):
            if not isinstance(getattr(node, "parent", None), ast.ClassDef):  # Exclude class methods
                params = get_param_info(node.args.args, node.args.kwonlyargs, node.args.defaults, node.args.kw_defaults)
                if node.name[0] == "_":
                    continue

                return_type = ast.unparse(node.returns) if node.returns else "Unknown"
                result["functions"][node.name] = {
                    "docstring": ast.get_docstring(node),
                    "params": params,
                    "return": return_type
                }
        
        elif isinstance(node, ast.Assign):
            if isinstance(getattr(node, "parent", None), ast.FunctionDef):
                continue  # Skip function-local variables

            for target in node.targets:
                if isinstance(target, ast.Name):  # Normal variable
                    value, var_type = get_value_info(node.value)
                    if target.id[0] == "_":
                        continue

                    result["variables"].append({
                        "name": target.id,
                        "value": value,
                        "type": var_type,
                        "constant": target.id.isupper()
                    })
                    
        elif isinstance(node, ast.AnnAssign):
            if isinstance(getattr(node, "parent", None), ast.FunctionDef):
                continue  # Skip function-local annotated variables

            if isinstance(node.target, ast.Name):  # Normal variable with annotation
                value, var_type = get_value_info(node.value)
                annotated_type = ast.unparse(node.annotation) if node.annotation else "Unknown"
                if node.target.id[0] == "_":
                    continue

                result["variables"].append({
                    "name": node.target.id,
                    "value": value,
                    "type": annotated_type if annotated_type != "Unknown" else var_type,  # Prefer annotation type
                    "constant": node.target.id.isupper()
                })

    return result

def parse_data_to_html(parsed_data, path, file_name):
    html_content = ""
    with open("doc_generator/static/static.html") as template_file:
        html_content: str = template_file.read()
    html_content += file_name + "</title>"
    html_content += "</head>\n<body>"
    html_content += f"<h1>{file_name}</h1>\n"
    html_content += f"<p id='path'>{path}</p>\n"
    
    for class_name, content in parsed_data["classes"].items():
        html_content += f"<h2 class=\"class\">{class_name}</h2>\n"
        html_content += f"<p class=\"documentation\">{content["docstring"]}\n</p>"
        for method_name, method in content["methods"].items():
            if method_name == "__init__":
                
                        
                html_content += f"<h3 class=\"constructor\">constructor -> {class_name}("
                for param in method["params"]:
                    if param["name"] != "self":
                        html_content += f"<span class=\"variable\">{param["name"]}</span> : <span class=\"type\">{param["type"] if param["type"] != "Unknown" else "any"}</span>, "
                html_content = html_content.rstrip(", ")
                html_content += ")</h3>\n"
                if method["docstring"] != None:  
                    html_content += f"<p class=\"documentation\">{method["docstring"]}</p>\n"
                html_content += f"<h4>class variables</h4>"
                html_content += "<table><thead>\n<tr>\n<th>Name</th>\n<th>Type</th>\n<th>Constant</th>\n<th>Initial Value</th>\n</tr>\n</thead>\n"
                html_content += "<tbody>\n"
                for var in method["init_variables"]:
                    html_content += f"<tr>\t<td class=\"variable\">{var["name"]}</td>\n<td class=\"type\">{var["type"]}</td>\n<td class=\"const{var["constant"]}\"></td>\n<td>{var["initial_value"]}</td>\n</tr>\n"
                html_content += "</tbody></table>\n"
            else:
                html_content += f"<h3 class=\"method\">"
                if any(d["name"] == "self" for d in method["params"]):
                    html_content += "<span class=\"cls_method\">class"
                else:
                    html_content += "<span class=\"static_method\">static"

                html_content += f" method </span> -> {method_name}("
                for param in method["params"]:
                    if param["name"] != "self":
                        html_content += f"<span class=\"variable\">{param["name"]}</span> : <span class=\"type\">{param["type"] if param["type"] != "Unknown" else "any"}</span>, "
                html_content = html_content.rstrip(", ")
                html_content += ")</h3>\n"
                html_content += f"<span class=\"return\">returns {method["return"]}</span>"

                if method["docstring"] != None:  
                    html_content += f"<p class=\"documentation\">{method["docstring"]}</p>\n"
                
                
        
    for func_name, content in parsed_data["functions"].items():
        html_content += f"<h2 class=\"function\">{func_name}</h2>\n"
        html_content += f" function </span> -> {func_name}("
        for param in content["params"]:
            if param["name"] != "self":
                html_content += f" {param["name"]} : {param["type"] if param["type"] != "Unknown" else "any"},"
        html_content.rstrip(",")
        html_content += ")</h3>\n"
        html_content += f"<span class=\"return\">returns {content["return"]}</span>"

        if content["docstring"] != None:  
            html_content += f"<p class=\"documentation\">{content["docstring"]}</p>\n"

    if len(parsed_data["variables"]) != 0:
        html_content += "<h2 class=\"variable\">variables</h2>\n"
        html_content += f"<h4>class variables</h4>"
        html_content += "<table><thead>\n<tr>\n<th>Name</th>\n<th>Type</th>\n<th>Constant</th>\n<th>Initial Value</th>\n</tr>\n</thead>\n"
        html_content += "<tbody>\n"
        for var in parsed_data["variables"]:
            html_content += f"<tr>\t<td class=\"variable\">{var["name"]}</td>\n<td class=\"type\">{var["type"]}</td>\n<td class=\"const{var["constant"]}\"></td>\n<td>{var["value"]}</td>\n</tr>\n"
        html_content += "</tbody>\n</table>\n"
    
    html_content += "</body>\n</html>"
    
    return html_content 
    

if __name__ == "__main__":
    with open("doc_generator/static/rules.json") as rules_files:
        rules = json.load(rules_files)
        
    PATH = rules["path"]
    DOC_PATH = rules["docPath"]
    SKIP_FILE_NAMES: list[str] = ["__init__.py", "*.pyc"]

    for path, dirs, files in os.walk(PATH):
        doc_path = os.path.join(path.replace(PATH, DOC_PATH))
        for file in files:
            if any(fnmatch.fnmatch(file, pattern) for pattern in SKIP_FILE_NAMES):
                continue

            parsed_data = parse_python_file(os.path.join(path, file))
            # print(file)
            # print(parsed_data)

            html_content = parse_data_to_html(parsed_data, path, file)
            if not os.path.isdir(path.replace(PATH, DOC_PATH)):
                os.mkdir(path.replace(PATH, DOC_PATH))
            with open(os.path.join(os.path.join(path.replace(PATH, DOC_PATH), f"{file.split(".")[0]}.html") ), "w") as f:
                f.write(html_content)
