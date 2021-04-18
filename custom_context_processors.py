from movie_app.forms import SearchForm


def add_search_form(request):
    return {'search_form': SearchForm()}
