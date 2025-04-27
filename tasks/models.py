from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - by {self.user.username}"


class Order(models.Model):
    order_id = models.PositiveIntegerField(unique=True)
    quantity = models.PositiveIntegerField()
    order_date = models.DateField()
    due_date = models.DateField()
    mo_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ])
    lot_number = models.CharField(max_length=5)
    codeitem = models.ForeignKey('CodeItem', on_delete=models.PROTECT)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)


class Procedure(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    prepared_by = models.CharField(max_length=100)
    prepared_date = models.DateField()
    reviewed_by = models.CharField(max_length=200)
    review_date = models.DateField()
    approved_by = models.CharField(max_length=200)
    approved_date = models.DateField()
    procedure_number = models.CharField(max_length=50)
    assembly_number = models.CharField(max_length=50)
    revision_number = models.CharField(max_length=20)
    tools = models.TextField() # opcional si luego se migra todo a Tool

    def __str__(self):
        return f"{self.name} - {self.prepared_by}"
    
class CodeItem(models.Model):
    code = models.CharField(max_length=10, unique=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.PROTECT)
    image = models.CharField(max_length=255, blank=True, null=True)
  # Imagen general del producto

    def __str__(self):
        return self.code
    
class Tool(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name='tool_items')
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    image_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Component(models.Model):
    codeitem = models.ForeignKey(CodeItem, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=100)
    item_id = models.CharField(max_length=50)
    required_quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)  # Imagen opcional por componente
    pos_x = models.PositiveIntegerField(default=0, help_text="px desde el borde izquierdo")
    pos_y = models.PositiveIntegerField(default=0, help_text="px desde el borde superior")
    z_index = models.PositiveIntegerField(default=1, help_text="Orden de apilado")
    def __str__(self):
        return f"{self.name} - {self.codeitem.code}"

class Profile(models.Model):
    """
    Étend le modèle User avec un numéro d'employé unique.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Numéro d'employé"
    )

    def __str__(self):
        # Affiche le nom complet de l'utilisateur suivi du numéro d'employé
        return f"{self.user.get_full_name()} ({self.employee_number})"



