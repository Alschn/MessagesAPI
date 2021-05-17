from django.test import TestCase


class APIViewsTests(TestCase):
    def setUp(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_list_or_create_wrong_method(self):
        pass

    def test_list_no_messages(self):
        pass

    def test_list_all_messages(self):
        pass

    def test_create_new_message(self):
        pass

    def test_create_new_message_same_content(self):
        pass

    def test_create_new_message_no_content(self):
        pass

    def test_get_message_not_exists(self):
        pass

    def test_get_message(self):
        pass

    def test_update_message(self):
        pass

    def test_delete_message(self):
        pass

    def test_get_message_no_id_given(self):
        pass

    def test_update_message_no_id_given(self):
        pass

    def test_delete_message_no_id_given(self):
        pass
