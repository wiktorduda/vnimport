import pytest
import mock

from vnimport import resource

class MockTime:
    def __init__(self):
        self.time_epoch = -1
    def now(self):
        self.time_epoch += 1
        return self.time_epoch
    def sleep(self, second):
        self.time_epoch += second
        return self.time_epoch

class TestRateLimit:
    def setup(self):
        mock_time = MockTime()
        mock_sleep = mock.MagicMock(side_effect=mock_time.sleep)
        self.func = mock.Mock()
        self.mocks = {
            'now_func': mock_time.now,
            'sleep_func': mock_sleep
        }
        self.rate = 2
        self.per_second = 13.0

    def test_call_decorated_function_within_rate_limit(self):
        decorated_func = resource.rate_limit(self.rate, self.per_second, **self.mocks)(self.func)
        for i in range(self.rate):
            decorated_func()
        assert self.mocks['sleep_func'].call_count == 0
        
    def test_call_decorated_function_out_of_rate_limit(self):
        decorated_func = resource.rate_limit(self.rate, self.per_second, **self.mocks)(self.func)
        for i in range(self.rate + 10):
            decorated_func()
        self.mocks['sleep_func'].assert_called_with(self.per_second/self.rate - 1.0)