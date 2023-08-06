import asyncpg
import asyncio
import click
from pganonymizer.helper import (makeDSN, 
                                QUERY_FOR_CHECKING_CONSTRAINT, 
                                convert_byte_to_int, 
                                get_foreign_tables, 
                                has_foreign, 
                                hash_month_date, 
                                hash_phone_number, 
                                hashRecord, 
                                loadcsj)


async def run_anonymizer(dsn, schemafile):
    conn = await asyncpg.connect(dsn)
    schema = await loadcsj(schemafile)
    async with conn.transaction(isolation='serializable'):
        foreign_table_records = await conn.fetch(QUERY_FOR_CHECKING_CONSTRAINT)
        list_of_foreign_tables = await get_foreign_tables(foreign_table_records)
        for each_row in schema:
            table_name = each_row.get('table')
            column_name = each_row.get('column')
            rule = each_row.get('rule')
            foreign_flag = await has_foreign(list_of_foreign_tables, table_name, column_name)
            if foreign_flag:
                print(foreign_flag + " skipping...")
                continue
            print("Hashing", column_name, "in", table_name)
            try:
                records = await conn.fetch("SELECT {} FROM {}".format(column_name, table_name))    
                for each_record in records:
                    if not each_record.get(column_name):
                        continue             
                    hashed_record = await hashRecord(each_record.get(column_name), rule)
                    await conn.execute("UPDATE {} SET {} = '{}' WHERE {} = $1".format(table_name, column_name, hashed_record, column_name), each_record.get(column_name))
            except TypeError as e:
                return "Column name and hash type mismatched"

@click.command()
@click.option('-h', nargs=1, required=False, help="Postgres host")
@click.option('-d', nargs=1, required=False, help="Database name")
@click.option('-u', '-U', nargs=1, required=False, help="Database username (role)")
@click.option('-p', nargs=1, required=False, help="Database port")
@click.option('-password', '-P', nargs=1, required=False, help="Database password (Not recommended, use environment variable PGPASSWORD instead)")
@click.option('--schema', nargs=1, required=False, help="Path to yml file")
def main(h, d, u, p, password, schema):
    cnx_destination = {
        '-h': h,
        '-d': d,
        '-U': u,
        '-p': p,
        '-P': password
    }
    dsn = makeDSN(cnx_destination)
    if schema:
        asyncio.get_event_loop().run_until_complete(run_anonymizer(dsn, schema))


if __name__ == "__main__":
    main()