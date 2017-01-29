import unittest
from test import generatedboardtest
from test import binaryboarditemsgettertest
from test import tagsystemtest
from test import gamesystemtest
from test import menusystemtest
from test import drawsystemtest
from test import playerprogresssystemtest

def createSuite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(generatedboardtest.TestGeneratedBoard))
    test_suite.addTest(unittest.makeSuite(binaryboarditemsgettertest.TestBinaryBoardItemsGetter))
    test_suite.addTest(unittest.makeSuite(tagsystemtest.TestTagSystem))
    test_suite.addTest(unittest.makeSuite(gamesystemtest.TestGameSystem))
    test_suite.addTest(unittest.makeSuite(menusystemtest.TestMenuSystem))
    test_suite.addTest(unittest.makeSuite(drawsystemtest.TestDrawSystem))
    test_suite.addTest(unittest.makeSuite(playerprogresssystemtest.TestPlayerProgressSystem))
    return test_suite

if __name__ == '__main__':
    suite = createSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)