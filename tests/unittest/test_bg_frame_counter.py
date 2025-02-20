import unittest
from src.avatar.algo.bg_frame_counter import BgFrameCounter


class TestBgFrameCounter(unittest.TestCase):

    def test_single_background(self):
        bg_counter = BgFrameCounter(total_bg_count=1)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)

    def test_multiple_backgrounds(self):
        bg_counter = BgFrameCounter(total_bg_count=3)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 1)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 2)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 1)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 1)

    def test_no_backgrounds(self):
        bg_counter = BgFrameCounter(total_bg_count=0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)

    def test_step_greater_than_one(self):
        BgFrameCounter.STEP = 2
        bg_counter = BgFrameCounter(total_bg_count=3)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 2)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 2)
        BgFrameCounter.STEP = 1  # Reset STEP to default

    def test_large_step(self):
        BgFrameCounter.STEP = 5
        bg_counter = BgFrameCounter(total_bg_count=10)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 5)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 8)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 3)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 2)
        BgFrameCounter.STEP = 1  # Reset STEP to default

    def test_large_step_with_small_bg_count(self):
        BgFrameCounter.STEP = 5
        bg_counter = BgFrameCounter(total_bg_count=4)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 0)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 1)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 2)
        self.assertEqual(bg_counter.get_and_update_bg_index(), 3)
        BgFrameCounter.STEP = 1  # Reset STEP to default


if __name__ == '__main__':
    unittest.main()
