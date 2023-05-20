import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import PullRequest
from .serializers import PullRequestSerializer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
import os


def screen_shoot(url, id):
    driver = None
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Create a new instance of the Chrome driver
        #path='home/ubuntu/chromedriver'
        driver = webdriver.Chrome(settings.CHROME_DRIVER, options=chrome_options)

        #driver = webdriver.Chrome(path, options=chrome_options)

        # Set the desired URL to open

        # Navigate to the URL
        driver.get(url)
        file_name = "".join([id, '.png'])
        # Perform your desired actions with the page elements
        # For example, capture a screenshot
        driver.save_screenshot(file_name)

        # Close the browser
        driver.quit()
        return os.path.join(os.getcwd(), file_name)
    except:
        driver.quit()
        traceback.print_exc()
        return None


@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # Handle the webhook payload here
        # Example: process the payload and perform necessary actions
        event_type = request.headers.get('X-GitHub-Event')
        if event_type == 'pull_request':
            print(payload)
            pull_request = payload['pull_request']
            id = pull_request['id']
            action = payload['action']
            state = pull_request['state']
            url = pull_request['html_url']
            updated_at = None
            if pull_request['updated_at']:
                updated_at = datetime.strptime(pull_request['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

            try:
                existing_pull_request = PullRequest.objects.get(id=id)
                # Update the existing pull request attributes
                existing_pull_request.action = action
                existing_pull_request.state = state
                existing_pull_request.updated_at = updated_at
                existing_pull_request.save()
            except PullRequest.DoesNotExist:

                url_screenshot = screen_shoot(url, id)
                PullRequest.objects.create(
                    action=action,
                    id=id,
                    url=url,
                    state=state,
                    title=pull_request['title'],
                    body=pull_request['body'],
                    created_at=datetime.strptime(pull_request['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                    updated_at=updated_at,
                    merge_commit_sha=pull_request['merge_commit_sha'],
                    user=pull_request['user']['login'],
                    screenshot=url_screenshot
                )

                # Save the screenshot
                # new_pull_request.save_screenshot()
        # Return a response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


def index(request):
    return HttpResponse(status=200)


class PullRequestViewSet(viewsets.ModelViewSet):
    queryset = PullRequest.objects.all()
    serializer_class = PullRequestSerializer
