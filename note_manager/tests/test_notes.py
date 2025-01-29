import unittest
import os
from note_manager.data.file_operations import append_notes_to_file, save_notes_json
import yaml
import json

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileOperations)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print('\n\n')
    return result.wasSuccessful()

class TestFileOperations(unittest.TestCase):

    def test_append_notes_to_file(self):
        notes = [
            {
                "username": "test_user",
                "content": "test_content",
                "status": "в процессе",
                "created_date": "01-01-2025",
                "issue_date": "10-01-2025",
                "titles": ["Test Title"]
            }
        ]

        append_notes_to_file(notes, 'test_notes.yaml')

        with open('test_notes.yaml', 'r', encoding='utf-8') as file:
            loaded_notes = yaml.safe_load(file)

        self.assertEqual(loaded_notes, notes)

    def test_save_and_load_notes(self):
        test_notes = [
            {
                "username": "user1",
                "content": "content1",
                "status": "в процессе",
                "created_date": "01-01-2025",
                "issue_date": "10-01-2025",
                "titles": ["Title1"]
            },
            {
                "username": "user2",
                "content": "content2",
                "status": "в процессе",
                "created_date": "02-01-2025",
                "issue_date": "11-01-2025",
                "titles": ["Title2"]
            }
        ]

        save_notes_json(test_notes, 'test.json')

        with open('test.json', 'r', encoding='utf-8') as file:
            loaded_notes = json.load(file)

        expected_notes = [
            {
                "username": "user1",
                "title": "Title1",
                "content": "content1",
                "status": "в процессе",
                "created_date": "01-01-2025",
                "issue_date": "10-01-2025"
            },
            {
                "username": "user2",
                "title": "Title2",
                "content": "content2",
                "status": "в процессе",
                "created_date": "02-01-2025",
                "issue_date": "11-01-2025"
            }
        ]

        self.assertEqual(loaded_notes, expected_notes)

    def tearDown(self):
        if os.path.exists('test_notes.yaml'):
            os.remove('test_notes.yaml')
        if os.path.exists('test.json'):
            os.remove('test.json')

if __name__ == '__main__':
    unittest.main()
