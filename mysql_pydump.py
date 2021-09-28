import os
import subprocess as sb
import sys
import argparse
import configparser

class MyDump:

    def __init__(self,**kwargs):
        # Config
        self.basedir = os.path.dirname(os.path.abspath(__file__))

        # config MySQL
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        self.mysql_user = conf['mysql']['USER']
        self.mysql_pass = conf['mysql']['PASSWORD']
        self.mysql_host = conf['mysql']['HOST']
        self.mysql_port = conf['mysql']['PORT']
        if kwargs['database'] == None:
            print("Erro: database parameter not found!")
            sys.exit(1)
        else:
            self.mysql_db   = kwargs['database']
        

    def dump(self):
        mysql_dump = f'mysqldump -u {self.mysql_user} --password={self.mysql_pass} \
            -P {self.mysql_port} -h {self.mysql_host} {self.mysql_db}'
        ps = sb.Popen(mysql_dump, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
        ret_code = ps.wait()
        if ret_code == 0:
            data = ps.communicate()[0].decode('utf-8')
            df = open('{}/dump.sql'.format(self.basedir), 'w')
            df.write(data)
            df.close()
            sys.exit(0)
        else:
            data = ps.communicate()[1].decode('utf-8')
            print(data)
            sys.exit(1)
        


    def restore(self):
        pass

    def drop(self):
        mysql_cmd = f'echo "drop database {self.mysql_db}" | \
                    mysql -u {self.mysql_user} --password={self.mysql_pass} \
                    -h {self.mysql_host} -P {self.mysql_port} '
        ps = sb.Popen(mysql_cmd, shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
        ret_code = ps.wait()
        if ret_code == 0:
            data = ps.communicate()[0].decode('utf-8')
            sys.exit(0)
        else:
            data = ps.communicate()[1].decode('utf-8')
            print(data)
            sys.exit(1)


if __name__ == '__main__':
    parse = argparse.ArgumentParser("Simple Python script to Dump and Restore data from MySQL")
    parse.add_argument('-d', '--dump' , help='Create a database dump', action='store_true')
    parse.add_argument('-r', '--restore' , help='Restore a database', action='store_true')
    parse.add_argument('-X', '--drop-database' , help='Drop a database', action='store_true')
    parse.add_argument('-D', '--database' , help='Database name')

    args = vars(parse.parse_args())

    if len(sys.argv) == 1:
        print(parse.format_help())
        sys.exit(0)
    elif (args['dump'] and args['restore']) and args['drop_database']:
        print('You need choise only one action: Dump, Restore or Drop')
        sys.exit(1)
    elif args['dump']:
        m = MyDump(database=args['database'])
        dump = m.dump()
    elif args['restore']:
        m = MyDump(database=args['database'])
        restore = m.restore()
    elif args['drop_database']:
        m = MyDump(database=args['database'])
        drop = m.drop()