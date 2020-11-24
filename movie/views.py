import json

from django.views   import View
from django.http    import JsonResponse

from .models        import (
    Movie,
    Picture,
    Staff,
    MovieStaffPosition,
    Genre,
    MovieGenre
)

from users.models   import User
from users.utils    import login_decorator

class MovieInfoView(View):
    @login_decorator
    def get(self, request, movie_id):

        movie_info = Movie.objects.prefetch_related('moviegenre_set',
                                                    'picture_set',
                                                    'moviestaffposition_set').get(id=movie_id)

        feedback = {
            "id"          : movie_info.pk,
            "name"        : movie_info.name,
            "country"     : movie_info.country,
            "description" : movie_info.description,
            "mainImage"   : movie_info.main_image,
            "openDate"    : movie_info.opening_at.year,
            "showTime"    : movie_info.show_time,
            "genre"       :[{"name": genre.genre.name
                            }for genre in movie_info.moviegenre_set.select_related('genre')],
            "staff"       :[{"name": staff.staff.name,
                             "image": staff.staff.proflie_image,
                             "position": staff.position.name
                            }for staff in movie_info.moviestaffposition_set.select_related('staff', 'position')],
            "subImage"    :[{"url": image.url
                            }for image in movie_info.picture_set.all()]
        }
        return JsonResponse({"data":feedback}, status=200)
