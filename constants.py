from enum import Enum

class ModuleMetadata(Enum):
    CONTROLLERS  = "controllers"
    IMPORT  = "imports"
    PROVIDER  = "providers"
    EXPORTS = "exports"
    
INJECTABLE_TOKEN = "__injectable__" 
CONTROLLERS_TOKEN =  ModuleMetadata.CONTROLLERS.value
IMPORTS_TOKEN = ModuleMetadata.IMPORT.value
PROVIDER_TOKEN = ModuleMetadata.PROVIDER.value 
EXPORT_TOKEN = ModuleMetadata.EXPORTS.value 
STATUS_CODE_TOKEN = "status_code"
MODULE_METADATA_PARAMS = [
    CONTROLLERS_TOKEN,
    IMPORTS_TOKEN,
    PROVIDER_TOKEN,
    EXPORT_TOKEN
]