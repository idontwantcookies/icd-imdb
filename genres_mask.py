from enum import IntFlag, auto


class Genre(IntFlag):
    SCI_FI = auto()
    BIOGRAPHY = auto()
    CRIME = auto()
    WAR = auto()
    FILM_NOIR = auto()
    WESTERN = auto()
    TALK_SHOW = auto()
    COMEDY = auto()
    ADULT = auto()
    FAMILY = auto()
    HISTORY = auto()
    FANTASY = auto()
    ACTION = auto()
    ANIMATION = auto()
    DOCUMENTARY = auto()
    GAME_SHOW = auto()
    THRILLER = auto()
    MYSTERY = auto()
    REALITY_TV = auto()
    NEWS = auto()
    HORROR = auto()
    ADVENTURE = auto()
    SPORT = auto()
    MUSIC = auto()
    ROMANCE = auto()
    MUSICAL = auto()
    DRAMA = auto()


GENRE_BY_NAME = {
    "Sci-Fi": Genre.SCI_FI,
    "Biography": Genre.BIOGRAPHY,
    "Crime": Genre.CRIME,
    "War": Genre.WAR,
    "Film-Noir": Genre.FILM_NOIR,
    "Western": Genre.WESTERN,
    "Talk-Show": Genre.TALK_SHOW,
    "Comedy": Genre.COMEDY,
    "Adult": Genre.ADULT,
    "Family": Genre.FAMILY,
    "History": Genre.HISTORY,
    "Fantasy": Genre.FANTASY,
    "Action": Genre.ACTION,
    "Animation": Genre.ANIMATION,
    "Documentary": Genre.DOCUMENTARY,
    "Game-Show": Genre.GAME_SHOW,
    "Thriller": Genre.THRILLER,
    "Mystery": Genre.MYSTERY,
    "Reality-TV": Genre.REALITY_TV,
    "News": Genre.NEWS,
    "Horror": Genre.HORROR,
    "Adventure": Genre.ADVENTURE,
    "Sport": Genre.SPORT,
    "Music": Genre.MUSIC,
    "Romance": Genre.ROMANCE,
    "Musical": Genre.MUSICAL,
    "Drama": Genre.DRAMA,
}
