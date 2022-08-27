
from dash_spa.session.backends.redis import RedisSessionBackend


SESSION_ID ='791b95982fbd2cb5a4b47a6509e38c0bc812ecda94683ff908f1c290176724b0'
TEST_KEY = 'test1'

def xtest_redis_backend():
    session = RedisSessionBackend(SESSION_ID)

    session.remove(TEST_KEY)

    test1 = session.get(TEST_KEY)

    assert test1 == {}

    session.set(TEST_KEY, {'hello': 1234})

    test1 = session.get(TEST_KEY)

    assert test1 == {'hello': 1234}
