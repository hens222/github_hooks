from django.db import models

from .utils import capture_screenshot


class PullRequest(models.Model):
    ACTION_CHOICES = [
        ('opened', 'Open'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    STATE_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Close'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    id = models.PositiveIntegerField(primary_key=True)
    url = models.URLField()
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default=None, null=True)
    merge_commit_sha = models.CharField(max_length=40, null=True)
    user = models.CharField(max_length=100)
    screenshot = models.URLField(null=True)

    class Meta:
        db_table = 'pull_requests'

    def save_screenshot(self):
        # Capture the screenshot of the pull request
        screenshot_url = self.url  # Use the HTML URL of the pull request as the screenshot URL
        screenshot_path = capture_screenshot(screenshot_url)

        # Update the screenshot field of the model instance
        self.screenshot = screenshot_path

        # Save the model instance
        self.save()
