# from django.http import JsonResponse
# from django.views.decorators.cache import cache_page
# from .models import Property

# @cache_page(60 * 15)
# def property_list(request):
#     properties = Property.objects.all()
#     data = [
#         {
#             "id": prop.id,
#             "title": prop.title,
#             "description": prop.description,
#             "price": float(prop.price),
#             "location": prop.location,
#             "created_at": prop.created_at.isoformat(),
#         }
#         for prop in properties
#     ]
#     return JsonResponse({"properties": data})
# # properties/views.py

from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties()
    data = [
        {
            "id": prop.id,
            "title": prop.title,
            "description": prop.description,
            "price": float(prop.price),
            "location": prop.location,
            "created_at": prop.created_at.isoformat(),
        }
        for prop in properties
    ]
    return JsonResponse({"properties": data})
