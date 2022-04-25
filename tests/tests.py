import os
import unittest
from emetapy import meta


class TestAuthAndConfigs(unittest.TestCase):
    def setUp(self) -> None:
        self.test_config_path = './test_token.env.test'
        self.test_config_expired_path = './test_token_expired.env.test'
        self.my_config_path = './my_most_private_parts.env'
        self.test_save_config = './test_save.env.test'

    def test_base_url_default(self):
        meta_client = meta.MetaClient()
        self.assertEqual(meta_client.base_url, 'https://rcraquery.epa.gov/metabase/')

    def test_token_is_none(self):
        meta_client = meta.MetaClient()
        self.assertIsNone(meta_client.token)

    def test_check_environment_for_var(self):
        meta_client = meta.MetaClient()
        set_dummy_username_and_password()
        meta_client.user_password_env_set()
        self.assertTrue(meta_client.u_and_p_env)

    def test_false_check_environment_for_var(self):
        strip_username_and_password()
        meta_client = meta.MetaClient()
        meta_client.user_password_env_set()
        self.assertFalse(meta_client.u_and_p_env)

    def test_read_token_from_file(self):
        meta_client = meta.MetaClient()
        meta_client.config_path = self.test_config_path
        meta_client.load_config_file()
        self.assertIsInstance(meta_client.token, str)

    def test_read_password_from_file(self):
        meta_client = meta.MetaClient()
        meta_client.config_path = self.test_config_path
        meta_client.load_config_file()
        self.assertIsInstance(meta_client.password, str)

    def test_read_username_from_file(self):
        meta_client = meta.MetaClient()
        meta_client.config_path = self.test_config_path
        meta_client.load_config_file()
        self.assertIsInstance(meta_client.username, str)

    def test_read_expiration_from_file(self):
        meta_client = meta.MetaClient()
        meta_client.config_path = self.test_config_path
        meta_client.load_config_file()
        self.assertIsInstance(meta_client.expiration, str)

    def test_expiration_check_catches_old_date(self):
        meta_client = meta.MetaClient()
        meta_client.config_path = self.test_config_expired_path
        meta_client.load_config_file()
        self.assertTrue(meta_client.is_token_expired())

    def test_expiration_check_date(self):
        meta_client = meta.MetaClient()
        meta_client.config_path = self.test_config_path
        meta_client.load_config_file()
        self.assertFalse(meta_client.is_token_expired())

    def test_save_configs_to_file(self):
        if os.path.exists(self.test_save_config):
            os.remove(self.test_save_config)
        meta_client = meta.MetaClient()
        meta_client.token = 'fake_token_string'
        meta_client.expiration = '2022-27-12T14:31:58.122010'
        meta_client.username = 'graham.david@epa.gov'
        meta_client.password = 'fake_password'
        meta_client.config_path = self.test_save_config
        meta_client.save()
        self.assertTrue(os.path.exists(self.test_save_config))

    def test_load_config_with_parameter(self):
        meta_client = meta.MetaClient()
        if os.path.exists(self.my_config_path):
            meta_client.load_config_file(self.my_config_path)
            self.assertIsInstance(meta_client.username, str)

    def test_auth_username_and_password(self):
        meta_client = meta.MetaClient()
        if os.path.exists(self.my_config_path):
            meta_client.load_config_file(self.my_config_path)
            if meta_client.username:
                if meta_client.password:
                    meta_client.authenticate()
                    self.assertIsNotNone(meta_client.token)


class TestQuerying(unittest.TestCase):
    def setUp(self) -> None:
        self.configs = './configs.env'

    def test_load_auth_and_save_configs(self):
        meta_client = meta.MetaClient()
        meta_client.load_config_file(self.configs)
        meta_client.authenticate()
        meta_client.save(self.configs)

    def test_simple_query(self):
        meta_client = meta.MetaClient()
        meta_client.load_config_file(self.configs)
        meta_client.authenticate()
        resp = meta_client.get_query('2946')
        self.assertIn('emails', resp.json()[0])

    def test_single_parameter_query(self):
        meta_client = meta.MetaClient()
        meta_client.load_config_file(self.configs)
        meta_client.authenticate()
        parameters = {'hand_id_var': 'INR000017301'}
        resp = meta_client.get_query('2946', 'json', parameters)
        self.assertIn('Woodmark', resp.json()[0]['emails'])


def set_dummy_username_and_password():
    if not os.getenv('META_USER'):
        os.environ['META_USER'] = 'username'
    if not os.getenv('META_PASSWORD'):
        os.environ['META_PASSWORD'] = 'password'


def strip_token_from_environment():
    if os.getenv('META_TOKEN'):
        os.environ.pop('META_TOKEN')
    if os.getenv('META_EXPIRATION'):
        os.environ.pop('META_EXPIRATION')


def strip_username_and_password():
    if os.getenv('META_USER'):
        os.environ.pop('META_USER')
    if os.getenv('META_PASSWORD'):
        os.environ.pop('META_PASSWORD')


if __name__ == '__main__':
    unittest.main()
