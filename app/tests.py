import unittest
import identidock


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        identidock.app.config["TESTING"] = True
        self.app = identidock.app.test_client()

    def test_get_mainpage(self,
                          name: str = "Moby Dick"):
        page = self.app.post("/",
                             data=dict(name=name))
        assert page.status_code == 200
        assert "Hello" in str(page.data)
        assert name in str(page.data)

    def test_html_escaping(self, tag="b"):
        html = "'><{0}>TEST</{1}><!--'".format(tag, tag)
        page = self.app.post("/",
                             data=dict(name=html))
        assert "<{0}>".format(tag) not in str(page.data)


if __name__ == "__main__":
    unittest.main()
