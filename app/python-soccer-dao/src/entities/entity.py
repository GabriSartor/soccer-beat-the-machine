class Entity(object):

    def create(self, attributes, table, primaryKey):
        query = ''
        column_list = ["{}{}{}".format('"', key, '"') for (key,value) in attributes.items()]
        column_string = ','.join(column_list)
        attribute_list = ["{}{}{}".format("'", str(value).replace("'", " "), "'") for (key,value) in attributes.items()]
        attribute_string = ','.join(attribute_list)
        attribute_string = attribute_string.replace("'None'", "NULL")
        query = "INSERT INTO {table} ({columns}) VALUES ({attributes});".format(table = table, columns = column_string, attributes = attribute_string)
        return query

    def createMany(self, attributesList, table, primaryKey):
        query = ''
        for attributes in attributesList:
            column_list = ["{}{}{}".format('"', key, '"') for (key,value) in attributes.items()]
            column_string = ','.join(column_list)
            attribute_list = ["{}{}{}".format("'", str(value).replace("'", " "), "'") for (key,value) in attributes.items()]
            attribute_string = ','.join(attribute_list)
            attribute_string = attribute_string.replace("'None'", "NULL")
            query += "INSERT INTO {table} ({columns}) VALUES ({attributes});".format(table = table, columns = column_string, attributes = attribute_string)
        return query

    def update(self, attributes, table, primaryKey):
        query = ''
        attribute_list = ['='.join(["{}{}{}".format('"', key, '"'), "{}{}{}".format("'", str(value).replace("'", " "), "'")]) for (key,value) in attributes.items() if key != primaryKey]
        attribute_string = ','.join(attribute_list)
        attribute_string = attribute_string.replace("'None'", "NULL")
        query = "UPDATE {} SET {} WHERE {}={};".format(table, attribute_string, primaryKey, attributes[primaryKey])
        return query

    def updateMany(self, attributesList, table, primaryKey):
        query = ''
        for attributes in attributesList:
            attribute_list = ['='.join(["{}{}{}".format('"', key, '"'), "{}{}{}".format("'", str(value).replace("'", " "), "'")]) for (key,value) in attributes.items() if key != primaryKey]
            attribute_string = ','.join(attribute_list)
            attribute_string = attribute_string.replace("'None'", "NULL")
            query += "UPDATE {} SET {} WHERE {}={};".format(table, attribute_string, primaryKey, attributes[primaryKey])
        return query