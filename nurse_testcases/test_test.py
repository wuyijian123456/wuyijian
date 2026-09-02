
from core.logger import log

# def test_fixtrue(generate_intern_id,db_assert):
#     log.info(generate_intern_id)
#     assert db_assert.assert_row_exists("select * from intern_info where id =%s",params=generate_intern_id,msg="数据不存在")


def test_upload(api_client):
    log.info("文件上传测试")

    path = r"D:\test\test38\4.png"

    resp = api_client.upload(url="/api/upload",file_path=path)
    log.info(resp.request.headers.get("Content-Type"))
    log.info(resp.content[:1000])
    assert resp.status_code == 200

