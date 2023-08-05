from enum import Enum


class DataTypeEnum(Enum):
    STRING = "''"
    INTEGER = "0"
    LONG = "0"
    FLOAT = "0"
    DOUBLE = "0"
    BOOLEAN = "''"
    DATE = "CURRENT_TIMESTAMP()"
    CHAR = "''"
    BYTE = "''"
    MODEL = "NULL"


class MetaModelField:
    def __init__(self, id=None, modelId=None, fieldName=None, alias=None, description=None,
                 dataType=None,
                 primaryKey=None, minLength=None, maxLength=None,
                 nullable=True, refModel=None, multiple=None, indexNames=None, fixItems=None, params=None):
        self.id = id
        self.modelId = modelId
        self.fieldName = fieldName
        self.alias = alias
        self.description = description
        self.dataType: DataTypeEnum = DataTypeEnum(dataType)
        self.primaryKey = primaryKey
        self.minLength = minLength
        self.maxLength = maxLength
        self.nullable = nullable
        self.refModel = refModel
        self.multiple = multiple
        self.indexNames = indexNames
        self.fixItems = fixItems
        self.params = params
