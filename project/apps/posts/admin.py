from django.contrib import admin
from posts.models import Backup, Fantastic, Post, PostRevision, Author, Read

BASE_POEM_LIST_DISPLAY = [
    "title",
    "author",
    "longest_line",
    "is_draft",
    "allow_comments",
    "show_draft_revisions",
    "show_published_revisions"
]


class PostAdmin(admin.ModelAdmin):
    list_display = BASE_POEM_LIST_DISPLAY
    search_fields = ["title", "body", ]
    model = Post


admin.site.register(Post, PostAdmin)


class PostRevisionAdmin(admin.ModelAdmin):
    list_display = ["revised_at", ] + BASE_POEM_LIST_DISPLAY
    search_fields = ["title", "body", ]
    model = PostRevision


admin.site.register(PostRevision, PostRevisionAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "slug", "premium_user",)
    model = Author


admin.site.register(Author, AuthorAdmin)


class FantasticAdmin(admin.ModelAdmin):
    list_display = ("post", "reader", "on", "marked_at",)
    model = Fantastic


admin.site.register(Fantastic, FantasticAdmin)


class ReadAdmin(admin.ModelAdmin):
    list_display = ("post", "reader", "read_at",)
    model = Read


admin.site.register(Read, ReadAdmin)



class BackupAdmin(admin.ModelAdmin):
    list_display = ("author", "backup_at",)
    model = Backup


admin.site.register(Backup, BackupAdmin)
