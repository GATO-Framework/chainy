import asyncio
import pathlib
import time
import unittest

import chainy.config


class MyTestCase(unittest.TestCase):
    def test_something(self):
        chain_path = pathlib.Path("chains/example-2.yml")
        chain = chainy.config.parse_config(chain_path)
        t = time.perf_counter()
        asyncio.run(chain.start("hey", "bud"))
        total_time = time.perf_counter() - t
        self.assertLess(total_time, 4.1)


if __name__ == '__main__':
    unittest.main()