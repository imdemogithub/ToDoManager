from django.db import models

class Department(models.Model):
    Name = models.CharField(max_length=30)
    JobTitles = models.TextField(max_length=255)

    class Meta:
        db_table = 'Department'

class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)

    class Meta:
        db_table = 'master'

    def __str__(self) -> str:
        return self.Email

choice_gender = (
    ('m', 'male'),
    ('f', 'female'),
    # ('o', 'other'),
)
file_path = "users/profile/"
class Profile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    Avatar = models.FileField(upload_to=file_path, default=f"{file_path}avatar.png")
    Department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default='')
    JobTitle = models.CharField(max_length=30, null=True, default='')
    FullName = models.CharField(max_length=30, null=True, default='')
    RefID = models.CharField(max_length=10, null=True, default='')
    Mobile = models.CharField(max_length=10, null=True, default='')
    BirthDate = models.DateField(auto_created=True, default='1999-08-01')
    Gender = models.CharField(max_length=25, null=True, choices=choice_gender)
    Country = models.CharField(max_length=25, null=True, default='')
    State = models.CharField(max_length=25, null=True, default='')
    City = models.CharField(max_length=25, null=True, default='')
    Address = models.TextField(max_length=150, null=True, default='')

    class Meta:
        db_table = 'profile'

    def __str__(self) -> str:
        return f"{self.id} {self.Master.Email}"


class Connection(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, default='pending')

    class Meta:
        db_table = 'connection'

    def __str__(self) -> str:
        return f"{self.id} {self.Profile.FullName}"

# Master | Profile
# Jai-1    | Kapil
# Jai    | Lucil
# Jai    | Sanjay

class ToDo(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    Title = models.CharField(max_length=25)
    Tags = models.CharField(max_length=100)
    Deadline = models.DateTimeField(auto_created=True)
    Description = models.TextField(max_length=255)
    IsCompleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'todo'

    def __str__(self):
        return f"{self.id} {self.Title}"


class ToDoMember(models.Model):
    ToDo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ToDoMember'

    def __str__(self) -> str:
        return self.Profile.FullName