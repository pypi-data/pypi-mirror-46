from request import Request

class Resource:
    def __init__(self, Name, Methods, Session):
        self.Name = Name
        self.MethodDict = Methods[0]
        self.Session = Session
        self.generate_request(self.MethodDict)

    def get_name(self):
        return self.Name

    def generate_request(self, method_dict):
        for method in list(method_dict.keys()):
            if (method in ['list', 'getOne', 'getSchedule']):
                crud = 'GET'
            elif (method in ['create', 'clone', 'forceComplete', 'batchCreate', 'autoAssign']):
                crud = 'POST'
            elif (method in ['update, updateSchedule', 'insertTask']):
                crud = 'PUT'
            elif (method in ['deleteOne']):
                crud = 'DELETE'

            setattr(self, method, Request(crud, method_dict[method], self.Session))