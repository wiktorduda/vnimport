import os, sys
pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd)

import urllib2
import urllib
import Playnite
import view
import resource
import resourcemapper
import api
import playnitemodel

__attributes = {
    'Author': 'vnimport',
    'Version': '0.1'
}

__exports = [
    {
        'Name': 'Download Metadata - vnimport',
        'Function' : 'erogetrailers_main'
    }
]

def erogetrailers_main():
	client = api.VNImportClient(resource.search_erogetrailers, 
								resourcemapper.ErogetrailersResourceMapper(Playnite), 
								resource.dowload_getchu_cover_image, 
								PlayniteApi)
	scope_dialog = view.ImportScopeOptionsDialog(PlayniteApi)
	import_dialog = view.ErogetrailersImportOptionsDialog(PlayniteApi)
	scope_result = scope_dialog.view()
	if not scope_result[0]:
		return None
	import_result = import_dialog.view()
	if not import_result[0]:
		return None
	import_answers = import_result[1]
	is_roman = import_result[2]
	updater = playnitemodel.UpdateGameModel(Playnite, is_roman)
	import_actions = [
		updater.update_all,
		updater.update_name,
		updater.update_developers,
		updater.update_release_date,
		updater.update_links,
		updater.update_cover_image
	]
	scope = PlayniteApi.Database.GetGames() if scope_result[1] else PlayniteApi.MainView.SelectedGames
	for model in scope:
		ignore_image = False
		game_objs = client.search_metadata(model)
		game_selection_dialog = view.MatchedGameSelectionDialog(PlayniteApi, model.Name, game_objs, is_roman)
		select_result = client.select_game_obj(game_objs, model, game_selection_dialog)
		game_obj = select_result[1]
		if not select_result[0]:
			continue
		if not game_obj:
			message = 'No Metadata Found for "{}"'
			PlayniteApi.Dialogs.ShowMessage(message.format(model.Name), 'Download Metadata From Erogetrailers')
			continue
		try:
			if not game_obj['getchu_id']:
				message = 'No Cover Image Found for "{}"'.format(model.Name)
				PlayniteApi.Dialogs.ShowMessage(message, 'Download Metadata From Erogetrailers')
				ignore_image = True
			if not ignore_image:
				client.update_game_image(game_obj, model, [game_obj['getchu_id']])
		except urllib2.HTTPError as err:
			message = 'Error when downloading cover image from getchu.com'
			message += '\n{}'.format(err)
			ignore_image = True
			PlayniteApi.Dialogs.ShowMessage(message, 'Download Metadata From Erogetrailers')
			pass
		client.update_metadata(import_answers, import_actions, game_obj, model)
		PlayniteApi.Database.UpdateGame(model)