PY_XML = '''

#int
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = int(float(xml.get("$(FIELD)", default=$(DEFAULT_VALUE))))
#without default value:
$(OWNER)$(FIELD) = int(float(xml.get("$(FIELD)")))

#bool
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", "yes" if $(OWNER)$(FIELD) else "no")
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
value = xml.get("$(FIELD)", default="$(DEFAULT_VALUE)")
        value = value.lower()[0] in ['t', 'y'] if value else False
        $(OWNER)$(FIELD) = value
#without default value:
value = xml.get("$(FIELD)")
        value = value.lower()[0] in ['t', 'y'] if value else False
        $(OWNER)$(FIELD) = value

#float
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = float(xml.get("$(FIELD)", default=$(DEFAULT_VALUE)))
#without default value:
$(OWNER)$(FIELD) = float(xml.get("$(FIELD)"))

#string
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = str(xml.get("$(FIELD)", default=$(DEFAULT_VALUE)))
#without default value:
$(OWNER)$(FIELD) = str(xml.get("$(FIELD)"))





#pointer
#serialize:
if $(OWNER)$(FIELD):
            xml_pointer = ET.SubElement(xml, '$(FIELD)')
            xml_pointer.set('type', $(OWNER)$(FIELD).get_type())
            $(OWNER)$(FIELD).serialize_$(FORMAT)(xml_pointer)
#deserialize:
xml_pointer = xml.find('$(FIELD)')
        if xml_pointer is not None:
            type = xml_pointer.get('type')
            $(OWNER)$(FIELD) = Factory.build(type)
            $(OWNER)$(FIELD).deserialize_$(FORMAT)(xml_pointer)


#list<int>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                $(OWNER)$(FIELD).append(int(float(obj.get('value'))))

#list<bool>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                value = obj.get('value')
                value = value.lower()[0] in ['t', 'y'] if value else False
                $(OWNER)$(FIELD).append(value)

#list<float>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                $(OWNER)$(FIELD).append(float(obj.get('value')))

#list<string>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            ET.SubElement(arr, 'item').set('value', str(obj))
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for obj in arr:
                $(OWNER)$(FIELD).append(str(obj.get('value')))


#list<serialized>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, 'item')
            obj.serialize_$(FORMAT)(item)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            from .$(TYPE) import $(TYPE)
            for xml_child in arr:
                obj = $(TYPE)()
                obj.deserialize_$(FORMAT)(xml_child)
                $(OWNER)$(FIELD).append(obj)


#serialized
#serialize:
if $(OWNER)$(FIELD):
            xml_child = ET.SubElement(xml, '$(FIELD)')
            $(OWNER)$(FIELD).serialize_$(FORMAT)(xml_child)
#deserialize:
xml_child = xml.find('$(FIELD)')
        from .$(TYPE) import $(TYPE)
        if xml_child is not None:
            $(OWNER)$(FIELD) = $(TYPE)()
            $(OWNER)$(FIELD).deserialize_$(FORMAT)(xml_child)


#list<pointer>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for t in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, t.get_type())
            t.serialize_$(FORMAT)(item)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for xml_item in arr:
                type = xml_item.tag
                obj = Factory.build(type)
                obj.deserialize_$(FORMAT)(xml_item)
                $(OWNER)$(FIELD).append(obj)

#link
#serialize:
from .$(TYPE) import $(TYPE)
        xml.set("$(FIELD)", $(OWNER)$(FIELD).name)
#deserialize:
name_$(FIELD) = xml.get("$(FIELD)")
        from .$(TYPE) import $(TYPE)
        $(OWNER)$(FIELD) = DataStorage.shared().get$(TYPE)(name_$(FIELD))

#list<link>
#serialize:
arr_$(FIELD) = ET.SubElement(xml, '$(FIELD)')
        for t in $(OWNER)$(FIELD):
            item = ET.SubElement(arr_$(FIELD), 'item')
            item.set("value", t.name)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = xml.find('$(FIELD)')
        if arr is not None:
            for xml_item in arr:
                name = xml_item.get('value')
                data = DataStorage.shared().get$(ARG_0)(name)
                $(OWNER)$(FIELD).append(data)

#map
#serialize
        xml_cache = xml
        map = ET.SubElement(xml, '$(FIELD)')
        for key, value in $(OWNER)$(FIELD).iteritems():
            xml = ET.SubElement(map, 'pair')
$(KEY_SERIALIZE)
$(VALUE_SERIALIZE)
        xml = xml_cache
#deserialize
        xml_cache = xml
        map = xml.find('$(FIELD)')
        for xml_child in (map if map is not None else []):
            xml = xml_child
$(KEY_SERIALIZE)
            map_key = key
$(VALUE_SERIALIZE)
            $(OWNER)$(FIELD)[map_key] = value
        xml = xml_cache

#enum
#serialize:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
$(OWNER)$(FIELD) = xml.get("$(FIELD)")
'''

PY_JSON = '''
#int, bool, float, string
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE):
            dictionary["$(FIELD)"] = $(OWNER)$(FIELD)
#without default value:
dictionary["$(FIELD)"] = $(OWNER)$(FIELD)
#deserialize
#with default value:
if "$(FIELD)" in dictionary:
            $(OWNER)$(FIELD) = dictionary["$(FIELD)"]
#without default value:
$(OWNER)$(FIELD) = dictionary["$(FIELD)"]


#pointer
#serialize
if $(OWNER)$(FIELD):
            dictionary['$(FIELD)'] = $({})
            dictionary['$(FIELD)'][$(OWNER)$(FIELD).get_type()] = $({})
            $(OWNER)$(FIELD).serialize_$(FORMAT)(dictionary['$(FIELD)'][$(OWNER)$(FIELD).get_type()])
#deserialize
if '$(FIELD)' in dictionary:
            for key, value_ in dictionary['$(FIELD)'].iteritems():
                $(OWNER)$(FIELD) = Factory.build(key)
                $(OWNER)$(FIELD).deserialize_$(FORMAT)(value_)
                break

#list<int>, list<float>, list<bool>, list<string>
#serialize
arr_$(FIELD) = []
        for obj in $(OWNER)$(FIELD):
            arr_$(FIELD).append(obj)
        dictionary['$(FIELD)'] = arr_$(FIELD)
#deserialize
$(OWNER)$(FIELD) = list()
        arr_$(FIELD) = dictionary['$(FIELD)']
        for obj in arr_$(FIELD):
            $(OWNER)$(FIELD).append(obj)

#list<serialized>
#serialize
arr_$(FIELD) = []
        for obj in $(OWNER)$(FIELD):
            dict = $({})
            obj.serialize_$(FORMAT)(dict)
            arr_$(FIELD).append(dict)
        dictionary['$(FIELD)'] = arr_$(FIELD)
#deserialize
$(OWNER)$(FIELD) = list()
        from .$(TYPE) import $(TYPE)
        arr_$(FIELD) = dictionary['$(FIELD)']
        for dict in arr_$(FIELD):
            obj = $(TYPE)()
            obj.deserialize_$(FORMAT)(dict)
            $(OWNER)$(FIELD).append(obj)

#serialized
#serialize
if $(OWNER)$(FIELD):
            dict = $({})
            $(OWNER)$(FIELD).serialize_$(FORMAT)(dict)
            dictionary["$(FIELD)"] = dict
#deserialize
if '$(FIELD)' in dictionary:
            from .$(TYPE) import $(TYPE)
            $(OWNER)$(FIELD) = $(TYPE)()
            $(OWNER)$(FIELD).deserialize_$(FORMAT)(dictionary['$(FIELD)'])

#list<pointer>
#serialize
dictionary['$(FIELD)'] = []
        arr = dictionary['$(FIELD)']
        for t in $(OWNER)$(FIELD):
            arr.append($({}))
            arr[-1][t.get_type()] = $({})
            t.serialize_$(FORMAT)(arr[-1][t.get_type()])
#deserialize
$(OWNER)$(FIELD) = list()
        arr = dictionary['$(FIELD)']
        size = len(arr)
        for index in range(size):
            for key, value in arr[index].iteritems():
                obj = Factory.build(key)
                $(OWNER)$(FIELD).append(obj)
                $(OWNER)$(FIELD)[-1].deserialize_$(FORMAT)(arr[index][key])
                break


#link
#serialize:
from .$(TYPE) import $(TYPE)
        from .$(TYPE) import $(TYPE)
        dictionary['$(FIELD)'] = $(OWNER)$(FIELD).name
#deserialize:
name = dictionary["$(FIELD)"]
        $(OWNER)$(FIELD) = DataStorage.shared().get$(TYPE)(name)


#list<link>
#serialize:
dictionary['$(FIELD)'] = []
        arr = dictionary['$(FIELD)']
        for t in $(OWNER)$(FIELD):
            arr.append(t.name)
#deserialize:
$(OWNER)$(FIELD) = list()
        arr = dictionary['$(FIELD)']
        for name in arr:
            data = DataStorage.shared().get$(ARG_0)(name)
            $(OWNER)$(FIELD).append(data)


#map
#serialize
        dict_cach = dictionary
        arr = []
        dictionary['$(FIELD)'] = arr
        for key, value in $(OWNER)$(FIELD).iteritems():
            arr.append($({}))
            dictionary = arr[-1]
$(KEY_SERIALIZE)
$(VALUE_SERIALIZE)
        dictionary = dict_cach
#deserialize
        dict_cach = dictionary
        arr = dictionary['$(FIELD)']
        for dict in arr:
            key = dict['key']
            type = key
            dictionary = dict
$(VALUE_SERIALIZE)
            $(OWNER)$(FIELD)[type] = value
        dictionary = dict_cach


#enum
#serialize:
dictionary["$(FIELD)"] = $(OWNER)$(FIELD)
#deserialize
$(OWNER)$(FIELD) = dictionary["$(FIELD)"]
'''
