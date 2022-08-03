from dash_spa_admin.synchronised_cache import SynchronisedTTLCache


def test_cache_send():
    cache = SynchronisedTTLCache(maxsize=1000, ttl=30*60)
    cache['test'] = {'test': 1234}
    assert 'test' in cache

def test_register_verification_cache(duo, test_app):
    login_manager = test_app.server.login_manager

    vrec1 = login_manager.create_verification_record("Steve", "steve@gmail.com", "1234")
    vrec2 = login_manager.get_verification_record("steve@gmail.com")

    assert vrec1.code == vrec2.code
