import re

from server.utils.cache import patch_vary_headers
from server.utils.deprecation import MiddlewareMixin
from server.utils.text import compress_sequence, compress_string

re_accepts_gzip = re.compile(r'\bgzip\b')


class GZipMiddleware(MiddlewareMixin):
    """
    Compress content if the browser allows gzip compression.
    Set the Vary header accordingly, so that caches will base their storage
    on the Accept-Encoding header.
    """
    def process_response(self, request, response):
        # It's not worth attempting to compress really short responses.
        if not response.streaming and len(response.content) < 200:
            return response

        # Avoid gzipping if we've already got a content-encoding.
        if response.has_header('Content-Encoding'):
            return response

        patch_vary_headers(response, ('Accept-Encoding',))

        ae = request.META.get('HTTP_ACCEPT_ENCODING', '')
        if not re_accepts_gzip.search(ae):
            return response

        if response.streaming:
            # Delete the `Content-Length` header for streaming content, because
            # we won't know the compressed size until we stream it.
            response.streaming_content = compress_sequence(response.streaming_content)
            del response['Content-Length']
        else:
            # Return the compressed content only if it's actually shorter.
            compressed_content = compress_string(response.content)
            if len(compressed_content) >= len(response.content):
                return response
            response.content = compressed_content
            response['Content-Length'] = str(len(response.content))

        # If there is a strong ETag, make it weak to fulfill the requirements
        # of RFC 7232 section-2.1 while also allowing conditional request
        # matches on ETags.
        etag = response.get('ETag')
        if etag and etag.startswith('"'):
            response['ETag'] = 'W/' + etag
        response['Content-Encoding'] = 'gzip'

        return response
