from django.test import TestCase


# Create your tests here.


class Article(TestCase):

    def test_demo(self):
        print("测试用例运行了")

    def test_article(self):
        print("测试首页")
        response = self.client.get('/')  # 测试首页
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/index")
        self.assertEqual(response.status_code, 200)

    def test_article_detail(self):
        print("测试详情页")
        response = self.client.get('/article/2020-05-13_test12312313')
        self.assertEqual(response.status_code, 200)
