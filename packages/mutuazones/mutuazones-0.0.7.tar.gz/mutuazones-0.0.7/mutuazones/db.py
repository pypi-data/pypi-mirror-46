import os
import numpy as np
import pandas as pd
import pandas_profiling
import logging
import itertools

from sqlalchemy import create_engine, types
from base64 import b64decode

# importante para el tema de acentos y codificación
os.environ['NLS_LANG'] = 'SPANISH_SPAIN.WE8ISO8859P15'

class Zone(object):
    def __init__(self, schemaName):
        self.__con = None
        self.__schema = schemaName
        self.__logger = logging.getLogger(__name__)

    def __connect(self):
        if self.__con is not None:
            return
        user = os.getenv('DB_USER')
        if user is None or user == '':
            user = self.__schema
        password = os.getenv('DB_PASS')
        if password is None or password == '':
            raise ImportError('The DB_PASS has not been defined as an environment variable')
        password = b64decode(password).decode('utf-8')
        url = os.getenv('DB_URL')
        if url is None or url == '':
            url = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=mtcldb-scan.mutuatfe.local)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=DESA)))'

        self.__logger.debug(f'Connecting to "{url}" with user "{user}" and using schema "{self.__schema}" ')

        if "DESCRIPTION" in url:  # conexión vía SERVICE
            self.__engine = create_engine('oracle+cx_oracle://{0}:{1}@{2}'.format(user, password, url))
        else:  # conexíon vía SID
            self.__engine = create_engine('oracle://{0}:{1}@{2}'.format(user, password, url))

        self.__con = self.__engine.connect()

    @property
    def df_names(self):
        """Devuelve una tupla de los nombres lógicos de los dataframes almacenados"""
        self.__connect()
        names = self.__con.execute(f"SELECT lower(OBJECT_NAME) FROM USER_OBJECTS WHERE OBJECT_TYPE IN ('TABLE', 'VIEW')").fetchall()
        return tuple(itertools.chain.from_iterable(names))
        #return self.__engine.table_names(self.__schema, self.__con)

    def load_df(self, name):
        """Carga un dataframe en memoria, a partir de su nombre lógico"""
        self.__connect()
        return pd.read_sql_table(name, self.__con, schema=self.__schema)
 
    def load_df_sql(self, query):
        """Carga un dataframe utilizando una sentencia SQL. Sólo se permite en el esquema de la ZONA."""
        self.__connect()
        return pd.read_sql(query, self.__con)
 
    def save_df(self, df, name, if_exists='replace'):
        """Persiste un dataframe con un nombre lógico concreto. Si ya existe, lo borra y lo genera de nuevo (comportamiento por defecto)"""
        self.__connect()
        dtyp = {c: types.VARCHAR(int(df[c].str.len().max()))
                for c in df.columns[df.dtypes == 'object'].tolist() if np.isnan(df[c].str.len().max()) == False}
        df.to_sql(name, self.__con, schema=self.__schema, if_exists=if_exists, dtype=dtyp, index=False)
     
    def generate_profile(self, df):
        """Genera un perfil de un dataframe concreto. Si no se asigna a una variable lo imprime por pantalla"""
        return pandas_profiling.ProfileReport(df)
 
    def save_profile_to_file(self, pathFile, df=None, profile=None):
        """Persiste en un fichero el perfil. Se debe suministrar un dataframe (genera el perfil en el momento y lo almacena) o un perfil ya generado"""
        if df is None and profile is None:
            raise ValueError('One parameter is missing, df or profile parameter is required')
        if df is not None:
            profile = pandas_profiling.ProfileReport(df)
        profile.to_file(outputfile=pathFile)