from django.contrib import admin

from .models import Resource
from .models import Step
from .models import Field
from .models import Format
from .models import Entrepreneur
from .models import Mentor
from .models import Organisation
from .models import Language

admin.site.register(Resource)
admin.site.register(Step)
admin.site.register(Field)
admin.site.register(Format)
admin.site.register(Mentor)
admin.site.register(Organisation)
admin.site.register(Entrepreneur)
admin.site.register(Language)
