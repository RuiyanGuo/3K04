from users import Users

def test_right_login():
    users = Users()
    user = {
        "-USERNAME-" : "admin",
        "-PASSWORD-" : "admin"
    }
    assert users.login(user) == True

def test_wrong_login_password():
    users = Users()
    user = {
        "-USERNAME-" : "admin",
        "-PASSWORD-" : "a"
    }
    assert users.login(user) == False

def test_wrong_login_name():
    users = Users()
    user = {
        "-USERNAME-" : "",
        "-PASSWORD-" : "a"
    }
    assert users.login(user) == False

def test_right_register():
    users = Users()
    entry = {
        "-USERNAME-" : "test1",
        "-PASSWORD-" : "test",
        "-CPASSWORD-" : "test"
    }
    assert not users.register(entry) == False

def test_wrong_register_name():
    users = Users()
    entry = {
        "-USERNAME-" : "admin",
        "-PASSWORD-" : "test",
        "-CPASSWORD-" : "test"
    }
    assert not users.register(entry) == True

def test_register_max():
    users = Users()
    entry = {
        "-USERNAME-" : "test10",
        "-PASSWORD-" : "test",
        "-CPASSWORD-" : "test"
    }
    assert not users.register(entry) == True

