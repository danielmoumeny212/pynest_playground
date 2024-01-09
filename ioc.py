# 1. Créez un conteneur d'injection de dépendances
import importlib
import re
import inspect

class DIContainer:
    _instance = None  # Attribut de classe pour stocker l'unique instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DIContainer, cls).__new__(cls)
            cls._instance.services = {}
        return cls._instance

    def add_service(self, service_class):
        service_instance = analyse_constructor(service_class)
        service_key = self._class_name_to_service_key(service_class.__name__)
        self.services[service_key] = service_instance

    def get_service(self, service_class):
        service_key = self._class_name_to_service_key(service_class.__name__) 
        return self.services.get(service_key)

    def _class_name_to_service_key(self, class_name:str):
        service_key = ""
        for char in class_name:
           if char.islower():
            service_key += char
           else:
            service_key += f"_{char.lower()}"
        return service_key.lstrip("_")


def detect_injectables(module_name):
    module = importlib.import_module(module_name)
    for name, cls in inspect.getmembers(module):
        if inspect.isclass(cls) and hasattr(cls, '__injectable__'):
            yield cls


def register_injectables(container, module_name):
    injectables = detect_injectables(module_name)
    for injectable in injectables:
        container.add_service(injectable)


def get_di_container():
    return DIContainer()


def get_constructor_arguments(x):
    container = get_di_container()
    print(x) 
    return x
    
    
params = []
def extract_param_type(target_class, param_name):
    annotations = inspect.getfullargspec(target_class).annotations
    return annotations.get(param_name)

def map_param_names_to_p(target_class):
    param_names = extra_param_names(target_class)
    param_type_mapping = {}
    container = get_di_container()

    for name in param_names:
        p = extract_param_type(target_class, name)
        service = container.get_service(p)
        
        if service is  None: 
            raise Exception(f"{name} is not included in provider array ")
        
        param_type_mapping[name] = service

    return param_type_mapping

def analyse_constructor(target_class):
    has_constr = has_constructor(target_class)
    if not has_constr:
        return []
    dependencies = map_param_names_to_p(target_class)
    for key , value in dependencies.items(): 
         setattr(target_class, key, value)
    
    service_instance = target_class(**dependencies)

    return service_instance

   
    
    


def has_constructor(target):
    arg = inspect.getfullargspec(target.__init__)
    annotations = arg.annotations
    return len(annotations.items()) > 0
 

def extra_param_names(targeted_class):
    params = inspect.getfullargspec(targeted_class).args
    if not params:
        return []
    return [name for name in params if name != "self"]

def create_instance_from_provider(self, name):
    provider = next((p for p in self.providers if p.provide == name), None)
    if not provider:
        raise Exception("Aucun fournisseur n'existe pour le service " + name)
    instance = provider.construct()
    self.services.append({
        "name": name,
        "instance": instance
    })
    return instance

class ParamMapper:
    def __init__(self, container):
        self.container = container

    def map(self, target_class):
        param_names = self.extra_param_names(target_class)
        param_type_mapping = {}

        for name in param_names:
            p = ParamTypeExtractor.extract(target_class, name)
            service = self.container.get_service(p)

            if service is None:
                raise Exception(f"{name} is not included in provider array ")

            param_type_mapping[name] = service

        return param_type_mapping


class ConstructorAnalyzer:
    def __init__(self, container, param_mapper):
        self.container = container
        self.param_mapper = param_mapper

    def analyze(self, target_class):
        has_constr = self.has_constructor(target_class)
        if not has_constr:
            return None
        dependencies = self.param_mapper.map(target_class)

        for key, value in dependencies.items():
            setattr(target_class, key, value)

        service_instance = target_class(**dependencies)
        return service_instance
    
class ParamTypeExtractor:
    @staticmethod
    def extract(target_class, param_name):
        annotations = inspect.getfullargspec(target_class).annotations
        return annotations.get(param_name)


class ConstructorChecker:
    @staticmethod
    def has_constructor(target):
        arg = inspect.getfullargspec(target.__init__)
        annotations = arg.annotations
        return len(annotations.items()) > 0


class ParamNameExtractor:
    @staticmethod
    def extract(targeted_class):
        params = inspect.getfullargspec(targeted_class).args
        if not params:
            return []
        return [name for name in params if name != "self"]

class InstanceCreator:
    def __init__(self, container):
        self.container = container

    def create_from_provider(self, name):
        # À compléter selon vos besoins
        pass

class DependencyInjector:
    def __init__(self, container):
        self.param_type_extractor = ParamTypeExtractor()
        self.param_mapper = ParamMapper(container)
        self.constructor_analyzer = ConstructorAnalyzer(container, self.param_mapper)
        self.constructor_checker = ConstructorChecker()
        self.param_name_extractor = ParamNameExtractor()
        self.instance_creator = InstanceCreator(container)

    def analyse_constructor(self, target_class):
        return self.constructor_analyzer.analyze(target_class)
    

class ModuleScanner:
    def __init__(self, container):
        self.container = container

    def scan_module(self, module):
        # Logique pour scanner un module
        # - Détecter les imports
        # - Détecter les exports
        # - Détecter les providers
        # - Détecter les controllers

     def inject_dependencies(self, instance):
        # Logique pour injecter les dépendances dans le constructeur d'une classe
        pass
# dependency_analyzer.py

class DependencyAnalyzer:
    @staticmethod
    def analyse_constructor(target_class):
        arg = inspect.getfullargspec(target_class.__init__)
        annotations = arg.annotations
        return len(annotations.items()) > 0
    @staticmethod
    def has_constructor(target):
        arg = inspect.getfullargspec(target.__init__)
        annotations = arg.annotations
        return len(annotations.items()) > 0

    @staticmethod
    def map_param_names_to_p(target_class, container):
        pass 

# service_registry.py


class ServiceRegistry:
    @staticmethod
    def detect_injectables(module_name):
       pass
    @staticmethod
    def register_injectables(container, module_name):
          pass
      

class ParameterTypeResolver:
    @staticmethod
    def resolve_param_type(target_class, param_name):
        annotations = inspect.getfullargspec(target_class).annotations
        return annotations.get(param_name)

class ParameterMapper:
    @staticmethod
    def map_param_names_to_services(target_class):
        param_names = ParameterMapper.extract_param_names(target_class)
        param_type_mapping = {}
        container = get_di_container()

        for name in param_names:
            p = ParameterTypeResolver.resolve_param_type(target_class, name)
            service = container.get_service(p)

            if service is None:
                raise Exception(f"{name} is not included in the provider array ")

            param_type_mapping[name] = service

        return param_type_mapping

    @staticmethod
    def analyze_constructor(target_class):
        has_constr = ParameterMapper.has_constructor(target_class)
        if not has_constr:
            return []
        dependencies = ParameterMapper.map_param_names_to_services(target_class)
        for key, value in dependencies.items():
            setattr(target_class, key, value)

        service_instance = target_class(**dependencies)

        return service_instance

    @staticmethod
    def resolve_dependencies(target_class):
        has_constr = ParameterMapper.has_constructor(target_class)
        if not has_constr:
            return []
        dependencies = ParameterMapper.map_param_names_to_services(target_class)
        for key, value in dependencies.items():
            setattr(target_class, key, value)

        service_instance = target_class(**dependencies)

        return service_instance

class ServiceInstanceFactory:
    @staticmethod
    def create_instance_from_provider(self, name):
        provider = next((p for p in self.providers if p.provide == name), None)
        if not provider:
            raise Exception("Aucun fournisseur n'existe pour le service " + name)
        instance = provider.construct()
        self.services.append({
            "name": name,
            "instance": instance
        })
        return instance
