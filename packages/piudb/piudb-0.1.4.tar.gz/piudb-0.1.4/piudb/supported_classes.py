class DBError:
    def __init__(self):
        pass
    def NotFound(self,msg):
        self.log('NotFoundError',msg)
    def ExistedPK(self,msg):
        self.log('PrimaryKeyAlreadyExisted',msg)
    def TypeError(self,msg):
        self.log('TypeError',msg)
    def NotFoundPK(self,msg):
        self.log('NotFoundPrimaryKey',msg)
    def FieldError(self,msg):
        self.log('FieldError','Field not exists or unsearchable: %s'%msg)
    def Error(self,msg):
        self.log('Error',msg)
    def log(self,error_name,info):
        return Exception('%s  : %s'%(error_name,info))
class InfoBody(dict):
    def __getattr__(self, key,default='DEFAULT'):
        try:
            value=self[key]
            return value
        except KeyError as k:
            if not default=="DEFAULT":
                return default
            raise Exception('No attribute %s'%key)
    def __setattr__(self, key, value):
        self[key]=value
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, state):
        self.__dict__=state
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            return None
    def met(self,**kws):
        for k,v in kws.items():
            if self.get(k,'notfound')=='notfound':
                return False
            if self[k] != v:
                return False
        return True
    def gets(self,keys):
        assert isinstance(keys,list)
        dic={}
        for k in keys:
            dic[k]=self[k]
        return InfoBody(dic)
    @classmethod
    def fromObj(cls,obj,keys=None):
        dic={}
        if not keys:
            for k in obj.__dict__:
                v=getattr(obj,k)
                if not callable(v):
                    dic[k]=v
            return cls(dic)
        for k in keys:
            dic[k]=obj.get(k,None)
        return cls(dic)
