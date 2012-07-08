from flask.ext.principal import RoleNeed, Permission


admin = Permission(RoleNeed('admins'))
staff = Permission(RoleNeed('staff'))
