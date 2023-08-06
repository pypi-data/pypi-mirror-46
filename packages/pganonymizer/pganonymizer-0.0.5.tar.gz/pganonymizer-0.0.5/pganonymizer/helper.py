import os
import hashlib
from csj_parser.csj import Csj
import base64

QUERY_FOR_CHECKING_CONSTRAINT = '''
SELECT conrelid::regclass AS foreign_table, ta.attname AS fk_column,
       confrelid::regclass AS primary_table, fa.attname AS pk_column
  FROM (
   SELECT conname, conrelid, confrelid,
          unnest(conkey) AS conkey, unnest(confkey) AS confkey
     FROM pg_constraint
    WHERE conname like '%fkey%'
  ) as pgc
  JOIN pg_attribute AS ta ON ta.attrelid = conrelid AND ta.attnum = conkey
  JOIN pg_attribute AS fa ON fa.attrelid = confrelid AND fa.attnum = confkey
'''

class TypeMismatchedException(Exception):
    pass

# Dictionary of possible options
PGOPTMAP = {
    "-d": ("dbname", "PGDATABASE", "/dbname"), 
    "-h": ("host", "PGHOST", "@host"), 
    "-p": ("port", "PGPORT", ":port"), 
    "-U": ("user", "PGUSER", "user"),
    "-P": ("password", "PGPASSWORD", ":password")
}

# Create a string of "mapped_filed = value"
def makeDSN(destination):
    template = "postgresql://user:password@host:port/dbname"
    for option, (field, env, placeholder) in PGOPTMAP.items():
        if destination[option]:
            template = template.replace(field, destination[option])
        elif os.getenv(env):
            template = template.replace(field, os.getenv(env))
        else:
            template = template.replace(placeholder, "")
    return template

async def convert_byte_to_int(input):
    return int.from_bytes(input, byteorder='big')

async def hash_month_date(date, hasher):
    date_array = str(date).split("-")
    hasher.update(date_array[1].encode("utf-8"))
    month = int.from_bytes(hasher.digest()[28:], byteorder='big') % 13
    hasher.update(date_array[2].encode("utf-8"))
    date = int.from_bytes(hasher.digest()[28:], byteorder='big') % 29
    return "{}-{}-{}".format(date_array[0], month if month else month + 1, date if date else date + 1)

async def hash_phone_number(phone_number, hasher):
    country_code = phone_number[:3]
    pure_number = phone_number[3:]
    len_to_be_hashed = len(pure_number)
    hasher.update(pure_number.encode("utf-8"))
    result = await convert_byte_to_int(hasher.digest()[31-len_to_be_hashed:]) % int("9"*len_to_be_hashed)
    result = country_code + (str(result) if len(str(result)) == len_to_be_hashed else str(result) + "0" * (len_to_be_hashed - len(str(result))))
    return result

async def check_valid_type(record, rule):
    if rule == "date":
        date_array = str(record).split("-")
        if len(date_array) is not 3 and False in [each_number.isdigit() for each_number in date_array]:
            return False

    elif rule == "phone":
        phone_number_array = str(record).split("+")
        if len(phone_number_array) is not 2 or not phone_number_array[1].isdigit():
            return False

    return True

async def hashRecord(record, rule):
    hasher = hashlib.sha256()
    if not await check_valid_type(record, rule):
        raise TypeMismatchedException()
    if rule == "hash":
        hasher.update(record.encode("utf-8"))
        result = base64.b32encode(hasher.digest()).decode()[:16]

    elif rule == "date": #YMD
        result = await hash_month_date(record, hasher)

    elif rule == "phone": #+CCX~ 
        result = await hash_phone_number(record, hasher)

    return result

async def loadcsj(filename):
    with open(filename) as f:
        lines = f.read()
        json_dict = Csj.to_dict(lines)
        return json_dict

async def get_foreign_tables(records):
    list_of_foreign_tables = []
    for each_foreign_record in records:
        dict_of_foreign_table = {}
        dict_of_foreign_table['foreign_table'] = each_foreign_record.get('foreign_table')
        dict_of_foreign_table['primary_table'] = each_foreign_record.get('primary_table')
        dict_of_foreign_table['fk_column'] = each_foreign_record.get('fk_column')
        dict_of_foreign_table['pk_column'] = each_foreign_record.get('pk_column')
        list_of_foreign_tables.append(dict_of_foreign_table)
    return list_of_foreign_tables

async def has_foreign(list_of_foreign_tables, table_name, column_name):
    for each_record in list_of_foreign_tables:
        if table_name.replace('public.', '') == each_record['foreign_table'] and column_name  == each_record['fk_column']:
            return table_name + " with column " + column_name + " is referencing column " + each_record['pk_column'] + " from table " + each_record['primary_table']
    return None