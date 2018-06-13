class SingleOptionView(object):
    def __init__(self, playniteapi):
        self.playniteapi = playniteapi

    def render(self, options, **kwargs):
        intro = kwargs.get('intro', '')
        intro += '\n____________________________'
        intro += '\nEntering option number:'
        example = '\ne.g. {} for selecting "{}"'
        if len(options) > 1:
            intro += example.format(2, options[1])
        if len(options) == 1:
            intro += example.format(1, options[0])
        intro += '\n____________________________'
        kwargs['intro'] = intro
        message = _create_option_menus(options, **kwargs)
        caption = kwargs.get('caption', 'Dialog')
        caption += ' - vnimport'
        while True:
            try:
                input_result = self.playniteapi.Dialogs.SelectString(message, caption, '1')
                option = self._get_single_option(input_result, len(options))
                if input_result.Result == False:
                    return (input_result.Result, -1)
                    break
                return (input_result.Result, option)
            except ValueError:
                self.playniteapi.Dialogs.ShowErrorMessage('Please enter a valid option', 'Input Error')
    
    def _get_single_option(self, input_result, expected_range):
        if not input_result.SelectedString:
            option = -1
            return option
        option = int(input_result.SelectedString)-1
        if option < 0 or option > expected_range-1:
            raise ValueError('Not within possible options range')
        return option

class MultiOptionView(object):
    def __init__(self, playniteapi):
        self.playniteapi = playniteapi

    def render(self, options, **kwargs):
        intro = kwargs.get('intro', '')
        intro += '\n____________________________'
        intro += '\nEntering option numbers in comma seperated form:'
        example = '\ne.g. {},{} for selecting "{}" and "{}"'
        if len(options) > 2:
            intro += example.format(2,3, options[1], options[2])
        if len(options) == 2:
            intro += example.format(1,2, options[0], options[1])
        intro += '\n____________________________'
        kwargs['intro'] = intro
        message = _create_option_menus(options, **kwargs)
        caption = kwargs.get('caption', 'Dialog')
        caption += ' - vnimport'
        while True:
            try:
                input_result = self.playniteapi.Dialogs.SelectString(message, caption, '1')
                options = self._get_multi_options(input_result, len(options))
                if input_result.Result == False:
                    return (input_result.Result, [])
                    break
                return (input_result.Result, options)
            except ValueError:
                self.playniteapi.Dialogs.ShowErrorMessage('Please enter a valid option', 'Input Error')

    def _get_multi_options(self, input_result, expected_range):
        options = []
        if not input_result.SelectedString:
            return options
        options = [int(option)-1 for option in input_result.SelectedString.split(',')]
        for option in options:
            if option < 0 or option > expected_range-1:
                raise ValueError('Within possible options range'.format(option))
        return options

class MatchedGameSelectionDialog(SingleOptionView):
    def __init__(self, playniteapi, name, game_objs, is_roman=False):
        super(MatchedGameSelectionDialog, self).__init__(playniteapi)
        self.name = name
        self.game_objs = game_objs
        self.is_roman  = is_roman
        
    def view(self, caption='Select Matching Games'):
        intro = 'There are multiple matching games for "{}"'
        intro += '\nYou can press "Cancel" if no matches are found'
        intro = intro.format(self.name)
        option_format = '{} ({})'
        options = []
        if self.is_roman:
            options = [option_format.format(game_obj['roman_name'], game_obj['platform']) for game_obj in self.game_objs]
        else:
            options = [option_format.format(game_obj['kanji_name'], game_obj['platform']) for game_obj in self.game_objs]
        input_result = self.render(options, intro=intro, caption=caption)
        return input_result

class ErogetrailersImportOptionsDialog(MultiOptionView):
    def view(self, caption='Download Metadata'):
        options = ['ALL', 'Game Title', 'Developer', 'Release Date', 'Related Links', 'Cover Image']
        intro = 'Select desired metadata to import'
        input_result = self.render(options, intro=intro, caption=caption)
        if input_result[0] == False:
            return (input_result[0], [], None)
        answers = input_result[1]
        if 0 in answers or 1 in answers:
            roman_dialog = ConfirmRomanDialog(self.playniteapi)
            roman_result = roman_dialog.view()
            if roman_result[0] == False:
                return (roman_result[0], [], None)
            is_roman = roman_result[1]
        return (input_result[0], answers, is_roman)
        
class ConfirmRomanDialog(SingleOptionView):
    def view(self, caption='Download Metadata'):
        intro = 'Which charachers should the name of visual novel display?'
        options = ['Kanji', 'Roman']
        input_result = self.render(options, intro=intro, caption=caption)
        is_roman = True if input_result[1] == 1 else False
        return (input_result[0], is_roman)
        
class ImportScopeOptionsDialog(SingleOptionView):
    def view(self, caption='Download Metadata'):
        intro = 'Which games should be updated?'
        options = ['Selected games only', 'All games from database']
        input_result = self.render(options, intro=intro, caption=caption)
        is_all = True if input_result[1] == 1 else False
        return (input_result[0], is_all)

def _create_option_menus(options, **kwargs):
    intro = kwargs.get('intro', '')
    footer = kwargs.get('footer', '')
    message_format = '{}\n{}\n{}'
    options_menu = ''
    options_menu_format = '{}. {}'
    for i in range(len(options)):
        options_menu += options_menu_format.format(i+1, options[i])
        if i < len(options) - 1:
            options_menu += '\n'
    message = message_format.format(intro, options_menu, footer)
    return message