from Homevee.Helper import Logger
from Homevee.testing import benchmark
from Homevee.testing.test_voice_assistant import run_voice_tests


def run_tests():
    print("running tests...")
    #run_benchmarks
    #benchmark.do_benchmarks()

    Logger.IS_DEBUG = False

    run_voice_tests()

if __name__ == "__main__":
    run_tests()