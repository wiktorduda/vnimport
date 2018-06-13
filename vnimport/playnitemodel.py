import System
import clr

class UpdateGameModel:
    def __init__(self, playnite, is_roman=False):
        self.playnite = playnite
        self.is_roman = is_roman

    def update_all(self, game_obj, model):
        self.update_name(game_obj, model)
        self.update_developers(game_obj, model)
        self.update_release_date(game_obj, model)
        self.update_links(game_obj, model)
        self.update_cover_image(game_obj, model)

    def update_name(self, game_obj, model):
        if self.is_roman:
            self.update_roman_name(game_obj, model)
        else:
            self.update_kanji_name(game_obj, model)

    def update_kanji_name(self, game_obj, model):
        name = game_obj['kanji_name']
        model.Name = name

    def update_roman_name(self, game_obj, model):
        roman_name = game_obj['roman_name']
        model.Name = roman_name

    def update_developers(self, game_obj, model):
        developers = game_obj['developers']
        model.Developers = System.Collections.Generic.ComparableList[str](developers)

    def update_release_date(self, game_obj, model):
        release_date = game_obj['release_date']
        if release_date:
            model.ReleaseDate = clr.Convert(release_date, System.DateTime)

    def update_links(self, game_obj, model):
        links = game_obj['links']
        model.Links = System.Collections.ObjectModel.ObservableCollection[self.playnite.SDK.Models.Link](links)

    def update_cover_image(self, game_obj, model):
        if 'image_id' in game_obj:
            model.Image = game_obj['image_id']