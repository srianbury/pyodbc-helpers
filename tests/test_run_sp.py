from unittest import TestCase, skipIf
import os
from dotenv import load_dotenv
import pyodbc
from pyodbch import run_sp
from pyodbch.run_sp import get_query, StoredProcedureError

class RunSp(TestCase):
    def setUp(self):
        load_dotenv()
        self.sp_name = 'USP_MY_STORED_PROCEDURE'
        self.list_params = [1, 'bob', 3.4]
        self.real_sp_name = 'USP_UNITTEST_PASS'
        self.fail_sp = 'USP_UNITTEST_FAIL'

    def test_get_query_without_params(self):
        sql_expected = 'SET NOCOUNT ON; DECLARE @RET int; EXEC @RET = ?; SELECT @RET;'
        param_expected = [self.sp_name]
        sql_actual, param_actual = get_query(self.sp_name)
        self.assertEqual(sql_expected, sql_actual)
        self.assertEqual(param_expected, param_actual)

    def test_get_query_with_params(self):
        sql_expected = 'SET NOCOUNT ON; DECLARE @RET int; EXEC @RET = ? ?, ?, ?; SELECT @RET;'
        param_expected = [self.sp_name] + self.list_params
        sql_actual, param_actual = get_query(self.sp_name, self.list_params)
        self.assertEqual(sql_expected, sql_actual)
        self.assertEqual(param_expected, param_actual)

    @skipIf(not os.getenv('HAS_DB_ACCESS'), 'No database access.')
    def test_run_without_params_should_pass(self):
        with pyodbc.connect(os.getenv('CNXN_STRING')) as cnxn:
            with cnxn.cursor() as cursor:
                try:
                    run_sp(cursor, self.real_sp_name)
                except Exception:
                    self.fail('run_sp() failed.')
                
                # make sure one record exists in the table
                sql = 'SELECT * FROM UNITTEST_PYODBC_RUN_SP;'
                cursor.execute(sql)
                results = cursor.fetchall()
                self.assertEqual(1, len(results))

                # make sure the data is correct
                result = results[0]
                actual = (result.ID, result.NAME, result.NUMBER)
                expected = (1, 'BOB', 3.4)
                self.assertEqual(expected, actual)

    @skipIf(not os.getenv('HAS_DB_ACCESS'), 'No database access.')
    def test_run_with_params_should_pass(self):
        PARAM_ID = 7
        PARAM_NAME = 'STEVE'

        with pyodbc.connect(os.getenv('CNXN_STRING')) as cnxn:
            with cnxn.cursor() as cursor:
                try:
                    run_sp(cursor, self.real_sp_name, [PARAM_ID, PARAM_NAME])
                except Exception:
                    self.fail('run_sp() failed.')
                
                # make sure one record exists in the table
                sql = 'SELECT * FROM UNITTEST_PYODBC_RUN_SP;'
                cursor.execute(sql)
                results = cursor.fetchall()
                self.assertEqual(1, len(results))

                # make sure the data is correct
                result = results[0]
                actual = (result.ID, result.NAME, result.NUMBER)
                expected = (PARAM_ID, PARAM_NAME, 3.4)
                self.assertEqual(expected, actual)

    @skipIf(not os.getenv('HAS_DB_ACCESS'), 'No database access.')
    def test_run_should_raise_stored_procedure_error(self):
        with pyodbc.connect(os.getenv('CNXN_STRING')) as cnxn:
            with cnxn.cursor() as cursor:
                with self.assertRaises(StoredProcedureError):
                    run_sp(cursor, self.fail_sp)
