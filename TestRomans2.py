from unittest import main, TestCase
from Romans2 import Person, Law
import sys, io

class TestRomans2(TestCase):

    # Jack did murder, and he knows the law. 
    # According to the 10 commandments in the Bible,
    # Jack is not righteous, and he is a hypocrite, 
    # because he knows the law and violates the law 
    # TODO: Possibly: change the definition so that "hypocrite"
    # Only gets registered when one judges? 
    def testBiblicalRighteous1(self):
        Jack = Person(name = "Jack", 
                      log = {"2025.12.16 12:55:23 UTC": "murder"}, 
                      knows_law = True)
        law = Law(name = "Biblical")
        law.check_against(Jack, print_report = False)
        self.assertEqual(Jack.righteous["Biblical"], False)
        self.assertEqual(Jack.hypocrite["Biblical"], True)
    
    # def assertPrint(self, printed, expected):
    #     captured = io.StringIO()
    #     sys_stdout_backup = sys.stdout
    #     sys.stdout = captured
    #     sys.stdout = sys_stdout_backup
    #     self.assertEqual(captured.getvalue(), expected)

    def testPrintReport1(self):
        Jack = Person(name = "Jack", 
                      log = {"2025.12.16 12:55:23 UTC": "murder"}, 
                      knows_law = True)
        law = Law(name = "Biblical")
        # TODO: Improve output format. 
        self.assertEqual(law.check_against(Jack, print_report = True, print_test = True), 
                         'According to the Law named Biblical, Jack has violated:\n6: You shall not murder. because Jack did murder.')

    

if __name__ == "__main__":
    main()