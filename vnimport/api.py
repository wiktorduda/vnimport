class VNImportClient:
    def __init__(self, metadata_search_fn, metadata_search_mapper, image_download_fn, playniteapi):
        self.metadata_search_fn = metadata_search_fn
        self.metadata_search_mapper = metadata_search_mapper
        self.image_download_fn = image_download_fn
        self.playniteapi = playniteapi

    def search_metadata(self, model):
        keyword = ''.join([c if self._is_cjk(c) or c.isalnum() or c.isspace() else ' ' for c in model.Name])
        game_objs = self.search_keyword(keyword)
        if not game_objs:
            keyword = keyword.split(' ')[0]
            game_objs = self.search_keyword(keyword)
        return game_objs

    def search_keyword(self, keyword):
        response = self.metadata_search_fn(keyword)
        game_objs = self.metadata_search_mapper.map(response)
        return game_objs

    def select_game_obj(self, game_objs, model, dialog_view):
        game_obj = None
        is_selected = True
        if len(game_objs) == 1:
            game_obj = game_objs[0]
        if len(game_objs) > 1:
            select_result = dialog_view.view()
            if not select_result[0]:
                is_selected = False
            game_obj = game_objs[select_result[1]]
        return (is_selected, game_obj)

    def update_metadata(self, answers, actions, game_obj, model):
        for answer in answers:
            actions[answer](game_obj, model)

    def update_game_image(self, game_obj, model, image_api_args):
        self.playniteapi.Database.RemoveImage(model.Image, model)
        file_id = None
        with self.image_download_fn(*image_api_args) as payload:
            file_id_format = 'images/custom/{}.jpg'
            file_id = self.playniteapi.Database.AddFile(file_id_format.format(payload[0]), payload[1])
        game_obj['image_id'] = file_id

    def _is_cjk(self, character):
        return any([start <= ord(character) <= end for start, end in 
                [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215), 
                (63744, 64255), (65072, 65103), (65381, 65500), 
                (131072, 196607)]
                ])