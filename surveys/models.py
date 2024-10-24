from django.db import models

# Create your models here.
class Encuesta(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Question(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    encuesta = models.ForeignKey(Encuesta, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    options = models.JSONField(null=True, blank=True)  # Almacenar opciones como una lista de cadenas

    def __str__(self):
        return f"{self.title} - {self.encuesta.title}"

class Response(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    encuesta = models.ForeignKey(Encuesta, related_name='responses', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"Response to {self.encuesta.title} on {self.date}"

class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"Answer to {self.question.title} for {self.response.encuesta.title}"
