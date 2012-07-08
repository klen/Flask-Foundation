INSERT INTO users_group (created_at, updated_at, name, active) VALUES ('2012-01-01 00:00:00.000000', '2012-01-01 00:00:00.000000', 'admins', 1);
INSERT INTO users_group (created_at, updated_at, name, active) VALUES ('2012-01-01 00:00:00.000000', '2012-01-01 00:00:00.000000', 'staff', 1);
INSERT INTO users_user (created_at, updated_at, username, email, _pw_hash, active) VALUES ('2012-01-01 00:00:00.000000', '2012-01-01 00:00:00.000000', 'admin', 'admin@admin.com', 'sha1$ZqGOeT6K$9e2a13d36a7de7b410b4b676694d6c392863e908', 1);
INSERT INTO users_usergroups (user_id, group_id) VALUES (1, 1);
INSERT INTO users_usergroups (user_id, group_id) VALUES (1, 2);
