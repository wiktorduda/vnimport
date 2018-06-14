import pytest
import mock
from vnimport import view

class ErrorAfter(object):
    def __init__(self, limit):
        self.limit = limit
        self.calls = 0

    def __call__(self, *args):
        self.calls += 1
        if self.calls > self.limit:
            raise CallableExhausted

class CallableExhausted(Exception):
    pass

class TestSingleOptionView:
    def setup(self):
        self.range = 3
        self.mock_playniteapi = mock.Mock()
        self.mock_playniteapi.Dialogs.ShowErrorMessage = mock.Mock(side_effect=ErrorAfter(1))

    def test_enter_option_within_range(self):
        input_str = '2'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.SingleOptionView(self.mock_playniteapi)
        answer = v.render([i for i in range(self.range)])
        assert answer[1] == int(input_str) - 1
        
    def test_enter_invalid_string_input(self):
        input_str = 'random_string'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.SingleOptionView(self.mock_playniteapi)
        message = '"random_string" is not a option number.'
        with pytest.raises(CallableExhausted):
            v.render([i for i in range(self.range)])
        assert self.mock_playniteapi.Dialogs.ShowErrorMessage.call_args[0][0] == message
    
    def test_enter_option_out_of_range(self):
        input_str = '5'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.SingleOptionView(self.mock_playniteapi)
        message = '"5" is not within possible options range.'
        with pytest.raises(CallableExhausted):
            v.render([i for i in range(self.range)])
        assert self.mock_playniteapi.Dialogs.ShowErrorMessage.call_args[0][0] == message
        
        
class TestMultiOptionView:
    def setup(self):
        self.range = 3
        self.mock_playniteapi = mock.Mock()
        self.mock_playniteapi.Dialogs.ShowErrorMessage = mock.Mock(side_effect=ErrorAfter(1))
        
    def test_enter_multiple_option_within_range(self):
        input_str = '2,3'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.MultiOptionView(self.mock_playniteapi)
        answer = v.render([i for i in range(self.range)])
        assert answer[1] == [1, 2]

    def test_enter_single_option_within_range(self):
        input_str = '2'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.MultiOptionView(self.mock_playniteapi)
        answer = v.render([i for i in range(self.range)])
        assert answer[1] == [1]

    def test_enter_multiple_option_out_of_range(self):
        input_str = '5,2'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.MultiOptionView(self.mock_playniteapi)
        message = 'In "5,2", at least one of the option is not within possible options range.'
        with pytest.raises(CallableExhausted):
            v.render([i for i in range(self.range)])
        assert self.mock_playniteapi.Dialogs.ShowErrorMessage.call_args[0][0] == message  

    def test_enter_single_option_out_of_range(self):
        input_str = '5'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.MultiOptionView(self.mock_playniteapi)
        message = '"5" is not within possible options range.'
        with pytest.raises(CallableExhausted):
            v.render([i for i in range(self.range)])
        assert self.mock_playniteapi.Dialogs.ShowErrorMessage.call_args[0][0] == message

    def test_enter_invalid_string_input(self):
        input_str = 'random_string'
        mock_dialog_output = mock.Mock(Result = True, 
                                       SelectedString=input_str)
        self.mock_playniteapi.Dialogs.SelectString = mock.Mock(return_value=mock_dialog_output)
        v = view.MultiOptionView(self.mock_playniteapi)
        message = '"random_string" is not a option numbers in comma seperated form.'
        with pytest.raises(CallableExhausted):
            v.render([i for i in range(self.range)])
        assert self.mock_playniteapi.Dialogs.ShowErrorMessage.call_args[0][0] == message