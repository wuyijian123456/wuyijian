
from core.logger import log

def test_fixtrue(generate_intern_id,db_assert):
    log.info(generate_intern_id)
    assert db_assert.assert_row_exists("select * from intern_info where id =%s",params=generate_intern_id,msg="数据不存在")
