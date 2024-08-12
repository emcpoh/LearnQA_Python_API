class TestInput:
    @staticmethod
    def test_input():
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, 'Input phrase is more or equal than 15'