import json
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from PIL import Image
from io import BytesIO
import os
from django.conf import settings
from rest_framework import viewsets
from .models import PullRequest
from .serializers import PullRequestSerializer


@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # Handle the webhook payload here
        # Example: process the payload and perform necessary actions
        event_type = request.headers.get('X-GitHub-Event')
        print(payload)
        if event_type == 'pull_request':
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
                new_pull_request = PullRequest.objects.create(
                    action=action,
                    id=id,
                    url=url,
                    state=state,
                    title=pull_request['title'],
                    body=pull_request['body'],
                    created_at=datetime.strptime(pull_request['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                    updated_at=updated_at,
                    merge_commit_sha=pull_request['merge_commit_sha'],
                    user=pull_request['user']['login']
                )

                # Save the screenshot
                #new_pull_request.save_screenshot()
        # Return a response
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


def capture_screenshot(url, save_path):
    # Send an HTTP GET request to the pull request URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the response content as an image using Pillow
        image = Image.open(BytesIO(response.content))

        # Save the image to the specified path
        print(save_path)
        image.save(save_path)


def index(request):
    # Assuming you have the pull request URL stored in a variable
    pull_request_url = "https://github.com/username/repository/pull/123"

    # Construct the save path for the screenshot
    screenshot_path = r"C:\Users\hens2\Desktop\exe"
    screenshot_path = os.path.join(screenshot_path, "pull_request.png")
    print(settings.MEDIA_ROOT)
    print(screenshot_path)
    # Call the capture_screenshot function to take the screenshot
    capture_screenshot(pull_request_url, screenshot_path)

    # Save the screenshot path to the database or perform any other necessary operations

    # Return a response or render a template
    return HttpResponse("Screenshot captured successfully.")


class PullRequestViewSet(viewsets.ModelViewSet):
    queryset = PullRequest.objects.all()
    serializer_class = PullRequestSerializer
