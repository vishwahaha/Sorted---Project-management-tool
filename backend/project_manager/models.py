from django.db import models
from djrichtextfield.models import RichTextField

# Create your models here.

class user(models.Model):
    """
    full_name, display_picture, enrollment_number are provided by channel-i
    (Might use more details in the future)
    """
    user_id = models.IntegerField(primary_key = True)
    full_name = models.CharField(max_length = 200)
    display_picture = models.ImageField()
    enrolment_number = models.IntegerField(default = 00000000)

    USER_TYPES = [
        ('admin', 'admin'),
        ('normal', 'normal'),
    ]
    user_type = models.CharField(
        max_length = 6,
        choices = USER_TYPES,
        default = 'normal',
    )

    """
    Redundant here, but can be accessed by project_set, card_set and comment_set
    """
    #projects = models.ManyToManyField(project)
    #cards = models.ManyToManyField(cards)
    #comments = models.ManyToManyField(comment)
    """
    Projects, lists and cards created by the user can be accsessed by using 
    the related_name = project_creator, list_creater, card_creator respectively
    """

    ONLINE_STATUS = [
        ('ON', 'online'),
        ('OFF', 'offline'),
    ]
    online_status = models.CharField(
        max_length = 3,
        choices = ONLINE_STATUS,
        default = 'OFF', 
    )
    
    is_disabled = models.BooleanField(default = False)

    def __str__(self):
        return f"This is {self.full_name}({self.enrol_number})'s data"

class project(models.Model):

    members = models.ManyToManyField(user)
    name = models.CharField(max_length = 100)
    wiki = RichTextField()

    creator = models.OneToOneField(
        user, 
        primary_key = False, 
        on_delete = models.DO_NOTHING, 
        related_name = 'project_creator',
    )

    date_created = models.DateField(auto_now_add = True)

    #False = project is incomplete, True = project is finished
    finished_status = models.BooleanField(default = False)

    def __str__(self):
        return f"Project : {self.name}, created by : {self.creator.full_name}"

class list(models.Model):
    
    project = models.ForeignKey(
        project, 
        on_delete = models.CASCADE,
    )

    title = models.CharField(max_length = 200)

    creator = models.OneToOneField(user, 
        primary_key = False, 
        on_delete = models.DO_NOTHING, 
        related_name = 'list_creator',
    )

    time_stamp = models.DateTimeField(auto_now_add = True)

    #False = incomplete, True = complete
    finished_status = models.BooleanField(default = False)

    def __str__(self):
        return f"List id: {self.id}, in project: {self.project.name}"

class card(models.Model):

    list = models.ForeignKey(
        list, 
        on_delete = models.CASCADE,
    )
    title = models.CharField(max_length = 100)
    desc = RichTextField()

    creator = models.OneToOneField(
        user, 
        primary_key = False, 
        on_delete = models.DO_NOTHING, 
        related_name = 'card_creator',
    )

    assignees = models.ManyToManyField(user)

    #False = incomplete, True = complete
    finished_status = models.BooleanField(default = False)

    def __str__(self):
        return f"Card in {self.list}"

class comment(models.Model):

    content = models.TextField()

    commentor = models.ForeignKey(
        user, 
        on_delete = models.CASCADE,
    )
    
    def __str__(self):
        return f"{self.content} *BY* {self.commentor.full_name}"