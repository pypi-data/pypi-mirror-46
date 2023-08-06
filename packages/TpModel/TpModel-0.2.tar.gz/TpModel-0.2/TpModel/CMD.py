import argparse,os
import json
import codecs
import pymysql
import logging
from Config import config
class Parser():
    parser = argparse.ArgumentParser()



    def __init__(self):
        self._project_path = ''
        self._basepath = ''
        self._model = ''
        self._basemodel = ''
        self._template_parameter = {}

    @property
    def template_parameter(self):
        return self._template_parameter

    @template_parameter.setter
    def template_parameter(self, template_parameter):
        self._template_parameter = template_parameter


    @property
    def model(self):
        return self._model

    @model.setter
    def model(self,model):
        self._model = model
        self._template_parameter['template_file'] = self._model

    @property
    def basemodel(self):
        return self._basemodel

    @basemodel.setter
    def basemodel(self, basemodel):
        self._basemodel = basemodel
        self._template_parameter['template_base_file'] = self._basemodel

    @property
    def project(self):
        return self._project_path

    @project.setter
    def project(self,project_path):
        try:
            self._project_path = project_path
            self._basepath = os.getcwd().split(self._project_path)[0] + self._project_path + '/'
        except Exception as e:
            logging.ERROR('Please enter the correct project name or the project name in the import path')


    def list_col(self,pro_db_config, tables_name):
        db = pymysql.connect(**pro_db_config)
        cursor = db.cursor()
        cursor.execute("show full columns from %s" % tables_name)
        result = cursor.fetchall()
        db.close()
        return result


    def cmd(self):
        self.parser.add_argument('-m','--model', nargs = 1, type = str, required = True,help = 'name of model')
        self.parser.add_argument('-t','--table', nargs = 1, type = str,required = True, help = 'name of table')
        self.parser.add_argument('-f','--file', nargs = 1, type = str, required = True, help = 'name of file')
        self.parser.add_argument('-d','--database', nargs = 1, type = str, default=None,help = 'name of database')
        self.parser.add_argument('-p','--path', nargs = 1, type = str,required = True,help = 'path of model')
        args = self.parser.parse_args()
        self._template_parameter['file_name'] = args.file[0]
        self._template_parameter['class_name'] = args.model[0]
        self._template_parameter['table'] = args.table[0]
        self._template_parameter['database'] = "'{}'".format(args.database[0]) if args.database else None
        config.set_basepath(self._basepath)
        if self._template_parameter['database']:
            _config = self.getconfig(args.database[0])
        else:
            _config = self.getconfig('default')
        cc = self.list_col(_config, args.table[0])

        columns = ["'{}'".format(i[0]) for i in cc]
        self._template_parameter['columns'] = ''' {} '''.format(',\n\t\t\t\t'.join(columns))
        self.create_template(args.path[0],args.file[0],args.path[0].split('/')[-1])


    def create_template(self,path,filename,dir):
        path = path if path.endswith('/') else path + '/'
        fn = self._basepath + path
        if not os.path.exists(fn):
            os.makedirs(fn)
            self.template(fn, 'BaseModel.py', 'template_base_file','')
        self.template(fn,filename,'template_file',dir)



    def template(self,path,filename,model,dir):
        self._template_parameter['module'] = dir
        _template = self._template_parameter.get(model, "default.txt")
        with codecs.open(_template, "rb", "UTF-8") as f:
            s = f.read()
        if not s:
            return
        s = s % self._template_parameter
        with codecs.open(path + filename, "wb", "UTF-8") as f:
            f.write(s)
            f.flush()

    def getconfig(self,database):
        data = config.items(database)
        return {
            'host': data.get('DB_HOST', ''),
            'port': int(data.get('DB_PORT', '')),
            'user': data.get('DB_USER', ''),
            'password': data.get('DB_PASSWORD', ''),
            'db': data.get('DB_NAME', ''),
            'charset': data.get('DB_CHARSET', ''),
        }

