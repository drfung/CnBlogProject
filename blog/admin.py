from django.contrib import admin
from blog import models as M
# Register your models here.
admin.site.register(M.UserInfo)
admin.site.register(M.Blog)
admin.site.register(M.Category)
admin.site.register(M.Article)
admin.site.register(M.Article2Tag)
admin.site.register(M.ArticleUpDown)
admin.site.register(M.Comment)