USER_NAME = 'Big Joe'
USER_EMAIL = 'bigjoe@bigjoe.com'
USER_PASSWORD = 'bigjoe99'

def delete_user(login_manager, email):
    """Delete given user"""
    try:
        login_manager.delete_user(email=email)
    except Exception:
        pass

def css_id(prefix):
    class _convert:
        def __getattr__(self, name):
            return f"#spa_admin_{prefix}_view_{name}"
    return _convert()

