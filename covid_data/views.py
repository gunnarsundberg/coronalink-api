from django.conf import settings
from django.http import HttpResponse
import mimetypes

...

def download_county_data(request):
    # fill these variables with real values
    fl_path = settings.BASE_DIR + '/data/county_data.csv'
    filename = 'county_data.csv'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response