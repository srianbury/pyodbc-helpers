
CREATE PROCEDURE USP_UNITTEST_PASS (
    @ID INT = 1
    @NAME VARCHAR 32 = 'BOB',
    @NUMBER FLOAT = 3.4
)
AS

TRUNCATE TABLE UNITTEST_PYODBC_RUN_SP;

INSERT INTO UNITTEST_PYODBC_RUN_SP
([ID], [NAME], [NUMBER]) VALUES
(@ID, @NAME, @NUMBER);

