

import pickle,os,asyncio

class TableOpener:
    def __init__(self):
        pass
    def open(self,tpath,mode='l',primary_key=None,searchable_keys=None,all_keys=None):
        tpath=self._stadardPath(tpath)
        if mode=='l':
            if not self._exists(tpath):
                raise Exception('Table not found at %s'%tpath)
            return self._load(tpath)
        elif mode=='c':
            if self._exists(tpath):
                raise Exception('A table already exists at %s'%tpath)
            elif os.path.exists(tpath) and len(os.listdir(tpath)): ## path already exists and is not empty.
                raise Exception('''A directory already exists at %s  , and it's not empty'''%tpath)
            return self._create(tpath,primary_key,searchable_keys,all_keys)
        elif mode=='a':
            if self._exists(tpath):
                return self._load(tpath)
            elif os.path.exists(tpath) and len(os.listdir(tpath)): ## path already exists and is not empty.
                raise Exception('''A directory already exists at %s  , and it's not empty'''%tpath)
            return self._create(tpath,primary_key,searchable_keys,all_keys)
        else:
            raise Exception('Argument mode: invalid value %s'%mode)
    def _load(self,tpath):
        tb=Table(tpath)
        self._log('load table at %s'%tpath)
        return tb
    def _create(self,tpath,primary_key,searchable_keys=[],all_keys=[]):
        if not primary_key:
            raise Exception('Argument primary_key cannot be None.')
        if not searchable_keys:
            searchable_keys=[primary_key]
        table=Table._create_whatever(tpath,primary_key,searchable_keys,all_keys)
        self._log('create table at %s successfully.'%tpath)
        return table
    def _exists(self, tpath):
       return Table._existsATable(tpath)
    def _warning(self,text,type='warning'):
        print('****{}****==>: {}'.format(type,text))
    def _log(self,text,type='Info'):
        print('***** {} ==>: {}'.format(type,text))
    def _stadardPath(self,path):
        return path.strip('/').strip('\\')
    def _formMapfilePath(self,tpath):
        return self._stadardPath(tpath)+'/'+self.mapfilename




class Table:
    '''
        Like a database,doesn't store records, but store objects directly .
        apis:
           find, findAll, insert, update, delete,exist:  => Record object
           select: =>InfoBody
        Record: primary_key(:str), searchable_keys(:[str]), keys(i.e. "id","name")
    '''

    mapfilename='mapfile.map'
    confiurefilename='configure.cfg'
    records_dirname='records'
    def __init__(self,tpath):
        '''  A table was created under the assumption of : an existed dir ; a map file;'''
        self.tpath=tpath
        self.mpath=self._joinPath(Table.mapfilename)
        self.cpath=self._joinPath(Table.confiurefilename)
        self.rpath=self._joinPath(Table.records_dirname)
        self.map=Map()
        self._load()
        self._addErrors()
    async def select(self,selected_keys=[],**kws):
        pks=self.map.findAll(**kws)
        objs=[self.map.dic[pk] for pk in pks]
        ibs=[InfoBody.formObj(obj) for obj in objs]
        return ibs
    async def delete(self,pk):
        obj=await self.findByPK(pk)
        if not obj:
            raise Exception('Record not found with %s = %s'%(self.primary_key,pk))
        os.remove(self._getRecordPath(pk))
        self.map.delete(pk)
        self._log('Successfully delete record width %s = %s'%(self.primary_key,pk))
        return obj
    async def update(self,pk,**kws):
        if not self.map.existsPK(pk):
            raise Exception('no record width %s = %s'%(self.primary_key,pk))
        obj=await self.findByPK(pk)
        for k,v in kws.items():
            setattr(obj,k,v)
        writeObjectFile(obj,self._getRecordPath(pk))
        self.map.update(pk,**kws)
        return obj
    async def insert(self,obj):
        pk=getattr(obj,self.primary_key)
        if self.map.existsPK(pk):
            raise Exception('A record with %s = %s already exists.'%(self.primary_key,pk))

        ib=InfoBody.fromObj(obj,self.searchable_keys)
        self.map.insert(pk,ib)
        writeObjectFile(obj,self._getRecordPath(pk))
        return ib
    async def findAll(self,**kws):
        pks=self.map.findAll(**kws)
        return [readObjectFile(self._getRecordPath(pk)) for pk in pks]
    async def find(self,**kws):
        pk=self.map.find(**kws)
        return readObjectFile(self._getRecordPath(pk))
    async def findByPK(self,pk):
        if self.map.existsPK(pk):
            return readObjectFile(self._getRecordPath(pk))
        return None
    async def existsPK(self,pk):
        return self.map.existsPK(pk)
    async def exists(self,**kws):
        return self._exists(**kws)
    def _exists(self,**kws):
        '''
            Assume that only one map object is running at one time ,
            which assures the map obj is always identical width the mapfile.
        '''
        self._verifySearchableKeys(kws)
        return self.map.exists(**kws)
    def _load(self):
        self._loadMap()
        self.configure=readObjectFile(self.cpath)
        self.primary_key=self.configure.primary_key
        self.searchable_keys=self.configure.searchable_keys
        self.keys=self.configure.keys
    def _loadMap(self):
        self.map=readObjectFile(self.mpath)
        self.map.mpath=self.mpath
    def _saveMap(self):
        return writeObjectFile(self.map,self.mpath)
    def _verifySearchableKeys(self,dic):
        for k in dic.keys():
            if not (k in self.searchable_keys):
                raise Exception('Contains unsearchable key: %s'%k)
        return True
    def _joinPath(self,fname):
        return self.tpath+'/'+fname
    def _joinRecordPath(self,fname):
        return self.rpath+'/'+fname
    def _getRecordFileName(self,pk):
        return pk+'.rcd'
    def _getRecordPath(self,pk):
        return self.rpath+'/'+pk+'.rcd'
    def _log(self,text,type='Info'):
        print('***** {} ==>: {}'.format(type,text))
    def _warning(self,text,type='warning'):
        print('****Table {}****==>: {}'.format(type,text))
    def _addErrors(self):
        self.ErrorNotFound=Exception('not found.')
    @classmethod
    def _create_whatever(cls,tpath,primary_key,searchable_keys,keys=[]):
        if not os.path.exists(tpath):
            os.mkdir(tpath)
        rpath=tpath+'/'+cls.records_dirname
        if not os.path.exists(rpath):
            os.mkdir(rpath)
        mpath=tpath+'/'+cls.mapfilename
        map=Map()
        writeObjectFile(map,mpath)
        cpath=tpath+'/'+cls.confiurefilename
        configure=Configure(primary_key,searchable_keys,keys)
        writeObjectFile(configure,cpath)
        return cls(tpath=tpath)
    @classmethod
    def _existsATable(cls,tpath):
        ''' This is not perfect , needs to be fixed. '''
        mpath=tpath+'/'+cls.mapfilename
        if (not os.path.exists(tpath)) or (not os.path.exists(mpath)):
            return False
        return True

class InfoBody(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
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
            dic[k]=getattr(obj,k)
        return cls(dic)
class Map:
    def __init__(self,mpath=None):
        self.dic=InfoBody()
        if mpath:
            self.mpath=mpath
    def delete(self,pk):
        del self.dic[pk]
        self.save()
    def insert(self,pk,obj):
        self.dic[pk]= obj
        self.save()
    def update(self,pk,**kws):
        self.dic[pk].update(**kws)
        self.save()
    def findAll(self,**kws):
        ibs=[]
        pks=[]
        for pk,ib in self.dic.items():
            if pk=='__dict__':
                continue
            found=True
            for k,v in kws:
                if ib.get(k)!=v:
                    found=False
                    break
            if found:
                ibs.append(ib)
                pks.append(pk)
        return pks
    def find(self,**kws):
        for pk,ib in self.dic.items():
            found=True
            for k,v in kws:
                if ib.get(k)!=v:
                    found=False
                    break
            if found:
                return pk
        return None
    def existsPK(self,pk):
        if self.dic.get(pk,'notfound')!='notfound':
            return True
        return False

    def exists(self,**kws):
        for ib in self.dic.values():
            found=True
            for k,v in kws:
                if ib.get(k)!=v:
                    found=False
                    break
            if found:
                return True
        return False
    def getRecordFileName(self,pk):
        if isinstance(pk,list):
            return [r+'.rcd' for r in pk]
        return pk+'.rcd'
    def load(self):
        self=readObjectFile(self.mpath)
    def save(self):
        writeObjectFile(self,self.mpath)

class Configure(InfoBody):
    def __init__(self,primary_key,searchable_keys=[],all_keys=[]):
        if not len(searchable_keys):
            searchable_keys=[primary_key]
        self.primary_key=primary_key
        self.searchable_keys=searchable_keys
        self.keys=all_keys


def log(*args, num=20, str='*'):
    print(str * num, end='')
    print(*args, end='')
    print(str * num)


##---------------------------------- Supportive functions---------------------
def writeObjectFile(obj,fpath):
    f=open(fpath,'wb')
    pickle.dump(obj,f)
    f.close()
def readObjectFile(fpath):
    f=open(fpath,'rb')
    try:
        obj=pickle.load(f)
    except:
        print(fpath)
        raise
    return obj
def test1():
    fn='db/test_table/records/湖南人，离不开的槟榔.rcd'
    f=open(fn,'rb')
    try:
        obj=pickle.load(f)
    except:
        print(f.read())
        print(os.listdir('/'.join(fn.split('/')[0:3])))
        raise
    print(obj.title)
async def test2():
    opener = TableOpener()
    tb = opener.open('db/test_table', mode='a', primary_key='title', searchable_keys=['title', 'info', 'intro'])
    all = await tb.findAll()
    [print(o.title) for o in all]
if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test2())