from django.db import models


class Task(models.Model):
	STATUS_CHOICES = [
		('To_do', 'To do'),
		('In Progress', 'In Progress'),
		('Done', 'Done'),
	]
	title = models.CharField(max_length=200)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To_do')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.title} ({self.get_status_display()})"	