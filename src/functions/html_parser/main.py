import functions_framework
import requests
from bs4 import BeautifulSoup

@functions_framework.http
def parse_job_posting(request):
    """HTTP Cloud Function to parse job posting HTML from a URL.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text (JSON), or any set of values that can be turned into a
        Response object using `make_response`.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'url' in request_json:
        url = request_json['url']
    elif request_args and 'url' in request_args:
        url = request_args['url']
    else:
        return {'error': 'Please provide a URL parameter'}, 400

    try:
        # User-Agent header (often required by sites)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove unwanted tags
        for script in soup(["script", "style", "nav", "footer", "iframe", "noscript"]):
            script.decompose()

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string
            soup.title.decompose()  # Remove title from text extraction

        # Extract text
        text = soup.get_text(separator=' ', strip=True)

        return {'title': title, 'text': text}, 200

    except requests.exceptions.RequestException as e:
        return {'error': f'Failed to fetch URL: {str(e)}'}, 500
    except Exception as e:
        return {'error': f'Internal Server Error: {str(e)}'}, 500
