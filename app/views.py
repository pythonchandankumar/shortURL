# Create your views here.
from django.db.models import F
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import URLMapping
from .serializer import URLMappingSerializer


class URLMappingView(APIView):
    def post(self, request):
        serializer = URLMappingSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, short_url=None):
        if short_url:
            try:
                url_mapping = URLMapping.objects.get(short_url=short_url)
                if url_mapping.expired_at and url_mapping.expired_at <= timezone.now():
                    return Response(
                        {"success": False, "message": "Short URL has expired"},
                        status=status.HTTP_410_GONE,
                    )
                url_mapping.click_count = F("click_count") + 1
                url_mapping.save(update_fields=["click_count"])
                return redirect(url_mapping.original_url)

            except URLMapping.DoesNotExist:
                return Response(
                    {"success": False, "message": "Short URL not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            urls = URLMapping.objects.all().order_by("created_at")
            serializer = URLMappingSerializer(urls, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
