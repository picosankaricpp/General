import xml.etree.ElementTree as ET
import json

def parse_modbus_mapping_file(filepath, device_name):
    with open(filepath, 'r') as file:
        content = file.read()

    # Wrap the content so it's valid XML for parsing
    wrapped = f"<root>{content}</root>"

    try:
        root = ET.fromstring(wrapped)
    except ET.ParseError as e:
        print("XML Parse Error:", e)
        return []

    tags = []

    # Search all modbusRegister blocks at any depth
    for register_block in root.findall(".//modbusRegister"):
        register_name = register_block.attrib.get("name")

        if register_name == "COILS":
            prefix = "C"
        elif register_name == "HOLDING_REGISTERS":
            prefix = "HRUI"

        else:
            continue

        mappings = register_block.findall("mapping")
        print(f"Register Block: {register_name} → {len(mappings)} mappings")

        for mapping in mappings:
            variable = mapping.attrib.get("variable")
            parent = mapping.attrib.get("parent")
            raw_address = mapping.attrib.get("address").lstrip("0") or "0"
            data_type = mapping.attrib.get("dataType", "").lower()

            if not variable or not parent or not data_type:
                print(f"Skipping incomplete mapping: {mapping.attrib}")
                continue

            if register_name == "HOLDING_REGISTERS":
                try:
                    address = str(int(raw_address) - 40000)
                except ValueError:
                    print(f"Invalid holding register address: {raw_address}")
                    continue
            else:
                address = raw_address  # Use as-is for COILS

            tag_type = "Boolean" if data_type == "bool" else "Int4"

            tag = {
                "name": variable,
                "tagType": "AtomicTag",
                "valueSource": "opc",
                "opcServer": "Ignition OPC UA Server",
                "opcItemPath": f"[{device_name}]{prefix}{address}",
                "dataType": tag_type,
                "enabled": True
            }
            tags.append(tag)

    return {"tags": tags}

input_path = r"your_path.txt"  # Replace with your file
tags = parse_modbus_mapping_file(input_path, 'Invest: Water Wash PLC')


# Output as JSON for pasting or saving
with open("ignition_tags.json", "w") as outfile:
    json.dump(tags, outfile, indent=2)

    try:        root = ET.fromstring(wrapped)    except ET.ParseError as e:        print("XML Parse Error:", e)        return []    tags = []    # Search all modbusRegister blocks at any depth    for register_block in root.findall(".//modbusRegister"):        register_name = register_block.attrib.get("name")        if register_name == "COILS":            prefix = "C"        elif register_name == "HOLDING_REGISTERS":            prefix = "HRUI"        else:            continue        mappings = register_block.findall("mapping")        print(f"Register Block: {register_name} → {len(mappings)} mappings")        for mapping in mappings:            variable = mapping.attrib.get("variable")            parent = mapping.attrib.get("parent")            raw_address = mapping.attrib.get("address").lstrip("0") or "0"            data_type = mapping.attrib.get("dataType", "").lower()            if not variable or not parent or not data_type:                print(f"Skipping incomplete mapping: {mapping.attrib}")                continue            if register_name == "HOLDING_REGISTERS":                try:                    address = str(int(raw_address) - 40000)                except ValueError:                    print(f"Invalid holding register address: {raw_address}")                    continue            else:                address = raw_address  # Use as-is for COILS            tag_type = "Boolean" if data_type == "bool" else "Int4"            tag = {                "name": variable,                "tagType": "AtomicTag",                "valueSource": "opc",                "opcServer": "Ignition OPC UA Server",                "opcItemPath": f"[{device_name}]{prefix}{address}",                "dataType": tag_type,                "enabled": True            }            tags.append(tag)    return {"tags": tags}input_path = r"C:\Users\PSankari\OneDrive - Consolidated Precision Products-cppcorp\Projects\Water Wash Upgrade\ModBus Map.txt"  # Replace with your filetags = parse_modbus_mapping_file(input_path, 'Invest: Water Wash PLC')# Output as JSON for pasting or savingwith open("ignition_tags.json", "w") as outfile:    json.dump(tags, outfile, indent=2)

