from django.http import HttpResponse

# from .models import ALBUMS # commentez cette ligne

# Create your views here.

from django.template import loader

def index(request):
    template = loader.get_template('reviews/index.html')
    return HttpResponse(template.render(request=request))

def listing(request):
    '''     albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
        message = """<ul>{}</ul>""".format("\n".join(albums)) '''
    message = "listing"
    return HttpResponse(message)

def detail(request, album_id):
    ''' id = int(album_id) # make sure we have an integer.
    album = ALBUMS[id] # get the album with its id.
    artists = " ".join([artist['name'] for artist in album['artists']]) # grab artists name and create a string out of it.
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album['name'], artists) '''
    message = "detail"
    return HttpResponse(message)

def search(request):
    ''' query = request.GET.get('query')
    if not query:
        message = "Aucun artiste n'est demandé"
    else:
        albums = [
            album for album in ALBUMS
            if query in " ".join(artist['name'] for artist in album['artists'])
        ]

        if len(albums) == 0:
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            albums = ["<li>{}</li>".format(album['name']) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(albums))
    '''
    message = "search"
    return HttpResponse(message)
