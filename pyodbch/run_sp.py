
PARAMETERIZED_VALUE = '?'

class StoredProcedureError(Exception):
    def __init__(self):
        self.message = "Stored Procedure return value != 0"

def run_sp(cursor, stored_procedure, params = []):
    '''
    Run a stored procedure and expect it to succeed.

    :param pyodbc.Cursor cursor: pyodbc cursor
    :param str stored_procedure: Name of the stored procedure
    :param list params: Parameters to pass to the stored procedure
    '''
    sql, sql_params = get_query(stored_procedure, params)
    cursor.execute(sql, sql_params)
    status = cursor.fetchval()
    if(status != 0):
        raise StoredProcedureError() 

def get_query(stored_procedure, params = []):
    '''
    Get the sql and a parameter bindings for the stored procedure

    :param str stored_procedure: Name of the stored procedure
    :param list params: Parameters to pass to the stored procedure
    '''
    start = 'SET NOCOUNT ON; DECLARE @RET int;'
    end = 'SELECT @RET;'
    formatted_params = format_params(params)
    middle = get_middle(stored_procedure, formatted_params)
    sql = f'{start} EXEC @RET = {middle}; {end}'
    sql_params = get_sql_params(stored_procedure, params)
    return sql, sql_params

def format_params(params):
    parameterized_params = [PARAMETERIZED_VALUE]*len(params) 
    return ', '.join(parameterized_params)

def get_middle(stored_procedure, formatted_params):
    if(len(formatted_params) == 0):
        return PARAMETERIZED_VALUE
    return f'{PARAMETERIZED_VALUE} {formatted_params}'

def get_sql_params(stored_procedure, params):
    ret = [stored_procedure]
    if(len(params) == 0):
        return ret
    for val in params:
        ret.append(val)
    return ret
    