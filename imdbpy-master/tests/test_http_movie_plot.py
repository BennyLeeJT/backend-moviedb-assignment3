import re


def test_movie_summary_should_be_some_text_with_author(ia):
    movie = ia.get_movie('0133093', info=['plot'])  # Matrix
    plots = movie.get('plot', [])
    assert 5 <= len(plots) <= 10
    kc_plot = ''
    for plot in plots:
        if plot.endswith('Kenneth Chisholm'):
            kc_plot = plot
            break
    assert re.match('^A computer hacker .*controllers\.::Kenneth Chisholm$', kc_plot)


def test_movie_summary_if_none_should_be_excluded(ia):
    movie = ia.get_movie('1863157', info=['plot'])  # Ates Parcasi
    assert 'plot' not in movie


def test_movie_synopsis_should_be_some_text(ia):
    movie = ia.get_movie('0133093', info=['plot'])  # Matrix
    synopsis = movie.get('synopsis')
    assert len(synopsis) == 1
    assert re.match('^The screen is filled with .* three Matrix movies\.$', synopsis[0])


def test_movie_synopsis_if_none_should_be_excluded(ia):
    movie = ia.get_movie('1863157', info=['plot'])  # Ates Parcasi
    assert 'synopsis' not in movie
