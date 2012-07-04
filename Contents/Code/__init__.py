BASE_URL = "http://webservice.canal-plus.com/rest/bigplayer/"

def Start():
	Plugin.AddPrefixHandler("/video/canalplus", ListeCategories, "Canal Plus", "icon-default.png", "art-default.jpg")
	ObjectContainer.title1    = 'Canal Plus'
	ObjectContainer.art       = R("art-default.jpg")


#Root categories
def ListeCategories():
	oc = ObjectContainer()
	categories = XML.ElementFromURL(BASE_URL + 'initPlayer').xpath('//THEMATIQUE')
	for categorie in categories:
		nom = categorie.xpath("./NOM")[0].text.capitalize()
		idCategorie = categorie.xpath("./ID")[0].text
		icon = R("icon-folder"+idCategorie+".png")
		if icon == None:
			icon = R('icon-folder.png')

        oc.add(DirectoryObject(key=Callback(ListeSousCategories, idCategorie=idCategorie, nomCategorie=nom), title=nom, thumb=icon))

	return oc

#Sub-categories
def ListeSousCategories(idCategorie, nomCategorie):
	art = R("art-cat"+idCategorie+".png")
	if art == None:
		art = R("art-default.jpg")
	oc = ObjectContainer(title2 = nomCategorie, art = art)
	sousCategories = XML.ElementFromURL(BASE_URL + 'initPlayer').xpath("//THEMATIQUE[ID="+idCategorie+"]//SELECTIONS")[0]
	for sousCategorie in sousCategories:
		nom = sousCategorie.xpath("./NOM")[0].text.capitalize()
		idSousCategorie = sousCategorie.xpath("./ID")[0].text
		icon = R("icon-folder"+idCategorie+".png")
		if icon == None:
			icon = R('icon-folder.png')

        oc.add(DirectoryObject(key=Callback(ListeVidoes, idSousCategorie=idSousCategorie, nomSousCategorie=nom, art=art), title=nom, thumb=icon))

	return oc

#Chosen sub-category's videos
def ListeVideos(idSousCategorie, nomSousCategorie, art):
	oc = ObjectContainer(title2 = nomSousCategorie, art = art)
	videos = XML.ElementFromURL(BASE_URL + "getMEAs/" + idSousCategorie).xpath("//MEA[TYPE!='CHAINE LIVE']")
	for video in videos:
		idVideo = video.xpath('./ID')[0].text
		titre = video.xpath('./INFOS/TITRAGE/TITRE')[0].text
		soustitre = video.xpath('./INFOS/TITRAGE/SOUS_TITRE')[0].text
		if soustitre.strip() != "":
			titre =  titre + " - " + soustitre

		description = video.xpath('./INFOS/DESCRIPTION')[0].text
		thumb = video.xpath('./MEDIA/IMAGES/GRAND')[0].text
        oc.add(DirectoryObject(key=Callback(ListeVideosLiees, idVideo=idVideo, nomSousCategorie=nomSousCategorie, art=art), title=titre, summary=description,
            thumb=Resource.ContentsOfURLWithFallback(url=thumb, fallback="icon-default.png"))

	return oc

#Video chosen + related videos
def ListeVideosLiees(idVideo, nomSousCategorie, art):
	oc = ObjectContainer(title2 = nomSousCategorie, art = art)

	videosXml = XML.ElementFromURL(BASE_URL + "getVideosLiees/" + idVideo)
	videos = videosXml.xpath("//VIDEO[ID='"+idVideo+"']")

	videos.extend(videosXml.xpath("//VIDEO[ID!='"+idVideo+"']"))
	for video in videos:
		titre = video.xpath('./INFOS/TITRAGE/TITRE')[0].text
		soustitre = video.xpath('./INFOS/TITRAGE/SOUS_TITRE')[0].text
		if soustitre.strip() != "":
			titre =  titre + " - " + soustitre

		description = video.xpath('./INFOS/DESCRIPTION')[0].text
		thumb = video.xpath('.//MEDIA/IMAGES/GRAND')[0].text
        video_url = '' ##find the video url and pass it to the URL Service
        oc.add(VideoClipObject(url=video_url, title=titre, summary=description,
            thumb=Resource.ContentsOfURLWithFallback(url=thumb, fallback="icon-default.png")))

	return oc