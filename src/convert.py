import xml.etree.ElementTree as ET
import fileutils
import json as jsonlib
import fileutils


types = {}
types["attack"] = "InteractionAttack"
types["takeitem"] = "InteractionTakeItem"
types["loot"] = "InteractionLoot"
types["destroy"] = "InteractionDestroySelf"
types["spawn"] = "InteractionSpawn"
types["move"] = "InteractionMove"
types["push_event"] = "InteractionPushEvent"
types["exit"] = "InteractionGoToNextDungeon"
types["enchant"] = "InteractionEnchant"
types["enchant_bonuses"] = "InteractionEnchantBonuses"
types["lever"] = "InteractionLever"
types["trigger"] = "InteractionShowLineStory"
types["addquest"] = "InteractionAddQuest"
types["userdata"] = "InteractionUserData"

#dir = "../../Resources/ini/templates/"
#files = fileutils.getFilesList(dir)
#for file in files:
#	tree = ET.parse(dir + file)
#	root = tree.getroot()
#	interactions_arr = root.findall("interactions")
#	for node in interactions_arr:
#		interactions = node.findall("interaction")
#		for interaction in interactions:
#			type = interaction.attrib["type"]
#			interaction.attrib.pop("type")
#			if "sequence" in interaction.attrib:
#				interaction.attrib.pop("sequence")
#			interaction.tag = types[type]
#	tree.write(dir + file)

def bool(value):
	if value == "true" or value == "yes":
		return True
	if value == "false" or value == "no":
		return False
	if value.isdigit():
		return int(value)
	return value

	
dir = "../../Resources/ini/units/"
files = fileutils.getFilesList(dir)
for file in files:
	tree = ET.parse(dir + file)
	root = tree.getroot()
	
	json = {}
	json["name"] = ""
	json["use_equipment"] = False
	json["can_be_blocked"] = True
	json["add_z_order"] = 0
	json["is_collisiable"] = True
	json["collisiable_cells"] = []
	json["interactions"] = []

	if "template" in root.attrib:
		print file, "->", root.attrib.pop("template") 
	
	if "name" in root.attrib:
		json["name"] = root.attrib.pop("name") 
	else:
		print "missing:", file
		continue

	if "collisiable" in root.attrib:
		json["is_collisiable"] = bool(root.attrib.pop("collisiable"))
	if "can_be_blocked" in root.attrib:
		json["can_be_blocked"] = bool(root.attrib.pop("can_be_blocked"))
	if "use_equip" in root.attrib:
		json["use_equipment"] = bool(root.attrib.pop("use_equip"))

	xmls = root.find("paramcollection")
	if xmls != None:
		for xml in xmls:
			if xml.tag == "add_z":
				json["add_z_order"] = xml.text
	
	add_zero_cell = json["is_collisiable"]
	xmls = root.find("cells")
	if xmls != None:
		for xml in xmls:
			if xml.tag == "cell":
				if "collisiable" in xml.attrib and xml.attrib["collisiable"] == "yes":
					cell = xml.attrib["offset"] if "offset" in xml.attrib else ""
					add_zero_cell = add_zero_cell and cell != "0x0"
					if cell == "":
						print "error! cell should have a value", file
						exit(-1)
					coords = cell.split("x");
					if len(coords) != 2:
						print "error! cell should be a point (XxY)", file
						exit(-1)
					cell = { "x" : coords[0], "y" : coords[1] }
					json["collisiable_cells"].append(cell)
	if add_zero_cell:
		json["collisiable_cells"].append({ "x" : 0, "y" :0 })
	xmls = root.find("interactions")
	if xmls != None:
		for xml in xmls:
			type = xml.tag
			interaction = {}
			for attr in xml.attrib:
				interaction[attr] = bool(xml.attrib[attr])
			json["interactions"].append({type:interaction})

	buffer = jsonlib.dumps(json, indent=2, sort_keys=False)
	fileutils.write("../../Resources/data/units/" + json["name"] + ".json", buffer)

