from django.contrib import admin
from  .models import Post,Comment,Catagory,Author
from mce_filebrowser.admin import MCEFilebrowserAdmin

# Register your models here.
class PostAdmin(MCEFilebrowserAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Catagory)
admin.site.register(Author)