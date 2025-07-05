
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponseRedirect,HttpResponse,HttpResponseNotFound
from django.shortcuts import get_object_or_404,render,redirect
from .models import URL
from .serializers import URLSerializer
from .models import URL as ShortenedURL
from django.shortcuts import render
from .utils import generate_shortcode
import os
BASE_URL = os.getenv("BASE_URL")  # fallback if not found

def home(request):
    context = {}
    if request.method == 'POST':
        url = request.POST.get('url')
        obj = ShortenedURL.objects.filter(url=url).first()
        if obj is None:
            obj = ShortenedURL.objects.create(
                url=url,
                shortCode=generate_shortcode()
            )
            message = 'Short URL generated!'
        else:
            message = 'Short URL already exists!'

        context = {
            'message': message,
            'url': url,
         
            'short_url': f"{BASE_URL}{obj.shortCode}",
            'shortCode': obj.shortCode,
            'access_count': obj.accessCount
        }
    return render(request, 'shortener/shorturl.html', context)


# TO CREATE A SHORT URL
class CreateShortURL(APIView):
    def post(self, request):
        original_url = request.data.get("url")

        if not original_url:
            return Response({"error": "URL is required"}, status=400)

        # Check if URL already exists
        existing = ShortenedURL.objects.filter(url=original_url).first()
        if existing:
            serializer = URLSerializer(existing)
            return Response(
                {
                    "message": "Short URL already exists!",
                    **serializer.data
                },
                status=200
            )

        # f not, create new one
        short_code = generate_shortcode()
        new_obj = ShortenedURL.objects.create(
            url=original_url,
            shortCode=short_code
        )
        serializer = URLSerializer(new_obj)
        return Response(
            {
                "message": "Short URL created!",
                **serializer.data
            },
            status=201
        )

    
from django.shortcuts import render
from django.views import View
from urllib.parse import urlparse
# TO RETRIVE ORIGINAL ONE
class RetrieveOriginalURLView(View):
    def get(self, request):
        short_url = request.GET.get('short_url')
        original_url = None
        error = None

        if short_url:
            try:
                # Extract shortcode from full short URL
                path = urlparse(short_url).path.strip('/')  # e.g., /iZLv1h → iZLv1h
                url_obj = URL.objects.get(shortCode=path)
                url_obj.accessCount += 1
                url_obj.save()
                original_url = url_obj.url
            except URL.DoesNotExist:
                error = "Short URL not found."

        return render(request, 'shortener/shorturl.html', {
            'original_url': original_url,
            'error': error,
        })
    
# TO UPDATE THE SHORT URL
from django.utils.timezone import now
class UpdateShortURL(APIView):
    def post(self, request):
        # Simulate PUT
        if request.POST.get('_method') != 'PUT':
            return render(request, 'shortener/shorturl.html', {"update_error": "Invalid method. Use PUT."})

        short_url = request.POST.get('short_url')
        new_url = request.POST.get('new_url')

        updated = False
        update_error = None
        data = {}

        if short_url and new_url:
            try:
                # Extract shortCode from full short URL
                short_code = urlparse(short_url).path.strip('/')  # e.g., from /abc123

                # Find and update the object
                url_obj = URL.objects.get(shortCode=short_code)
                url_obj.url = new_url
                url_obj.updatedAt = now()
                url_obj.save()

                updated = True
                data = {
                    "shortCode": url_obj.shortCode,
                    "url": url_obj.url,
                    "accessCount": url_obj.accessCount,
                    "updatedAt": url_obj.updatedAt
                }

            except URL.DoesNotExist:
                update_error = "Short URL not found."

        return render(request, 'shortener/shorturl.html', {
            "updated": updated,
            "data": data,
            "update_error": update_error,
            "short_url": short_url,
            "new_url": new_url
        })

    def get(self, request):
        return render(request, 'shortener/shorturl.html')

# TO DELETE THE SHORT URL

class DeleteShortURL(View):
    def post(self, request, shortCode):  
        method = request.POST.get("_method")
        delete_msg = ""

        if method != "DELETE":
            delete_msg = "Invalid method. Use DELETE."
        else:
            try:
                obj = URL.objects.get(shortCode=shortCode)
                obj.delete()
                delete_msg = "Short URL deleted successfully."
            except URL.DoesNotExist:
                delete_msg = "Short URL not found."

        return render(request, "shortener/shorturl.html", {
            "delete_msg": delete_msg,
            "short_url": f"{BASE_URL}{shortCode}",
        })


# TO GET STATS OF THE SHORT URL
class GetStats(View):
    def get(self, request, shortCode=None):
        try:
            url_obj = URL.objects.get(shortCode=shortCode)
            serializer = URLSerializer(url_obj)
            return render(request, 'shortener/shorturl.html', {
                "stats_data": serializer.data,
                "stats_error": None
            })
        except URL.DoesNotExist:
            return render(request, 'shortener/shorturl.html', {
                "stats_data": None,
                "stats_error": "Short URL not found."
            })


    
class RedirectToOriginal(APIView):
    def get(self, request, shortCode):
        url = get_object_or_404(URL, shortCode=shortCode)
        url.accessCount += 1
        url.save()
        return HttpResponseRedirect(url.url)  # ← redirects to google.com or any stored URL