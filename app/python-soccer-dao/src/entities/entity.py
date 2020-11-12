class Entity(object):

    def create(attributes, table, primaryKey):
        query = ''
        attribute_list = ['='.join([str(key), str(value)]) for (key,value) in attributes.items()]
        attribute_string = ','.join(attribute_list)
        query = "INSERT INTO {table} VALUES ({string});".format(table, attribute_string)
        return query

    def createMany(attributesList, table, primaryKey):
        query = ''
        for attributes in attributesList:
            attribute_list = ['='.join([str(key), str(value)]) for (key,value) in attributes.items()]
            attribute_string = ','.join(attribute_list)
            query += "INSERT INTO {table} VALUES ({string});".format(table, attribute_string)
        return query

    def update(attributes, table, primaryKey):
        query = ''
        attribute_list = ['='.join([str(key), str(value)]) for (key,value) in attribute.items()]
        attribute_string = ','.join(attribute_list)
        query = "UPDATE {table} SET {string} WHERE {id_name}={id_value};".format(table, attribute_string, self.primaryKey, attributes[self.primaryKey])
        return query

    def updateMany(attributesList, table, primaryKey):
        query = ''
        for attributes in attributesList:
            attribute_list = ['='.join([str(key), str(value)]) for (key,value) in attributes.items()]
            attribute_string = ','.join(attribute_list)
            query += "UPDATE {table} SET {string} WHERE {id_name}={id_value};".format(table, attribute_string, self.primaryKey, attributes[self.primaryKey])
        return query