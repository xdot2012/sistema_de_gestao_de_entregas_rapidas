from .test_setup import TestSetUp


class TestApis(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_be_created(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'], self.user_data['email'].upper())
        self.assertEqual(res.data['username'], self.user_data['username'].upper())
        user = self.user_class.objects.get(pk=res.data['pk'])
        self.assertIsNotNone(user)

    def test_user_cant_login_with_no_data(self):
        self.create_test_user()
        user = self.user_class.objects.filter()
        self.assertTrue(user.exists())
        res = self.client.post(self.token_url, format='json')
        self.assertEqual(res.status_code, 400)

    def test_user_cant_login_with_wrong_password(self):
        self.create_test_user()
        user = self.user_class.objects.filter()
        self.assertTrue(user.exists())
        data = {
            'username': 'test',
            'password': 'wrongPassword'
        }
        res = self.client.post(self.token_url, data, format='json')
        self.assertEqual(res.status_code, 400)

    def test_user_can_login(self):
        register_res = self.client.post(self.register_url, self.user_data, format='json')
        token_res = self.client.post(self.token_url, self.user_data, format='json')
        self.assertEqual(token_res.status_code, 200)
        self.assertEqual(register_res.data['email'], token_res.data['email'].upper())
        self.assertEqual(register_res.data['username'], token_res.data['username'].upper())
        self.assertEqual(register_res.data['pk'], token_res.data['user_id'])
        self.assertIsNotNone(token_res.data['token'])
