from django.contrib import admin
from drugs import models

class ProviderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "has_sitemaps", "excluded")
    readonly_fields = ["sitemaps"]
    fieldsets = [
        (
            None,
            { "fields": ["name", "url", "excluded", "sitemaps"] }
        )
    ]

    @admin.display(description="Nested sitemaps")
    def sitemaps(self, obj):
        return [b.url for b in obj.sitemap.all()]


class SitemapAdmin(admin.ModelAdmin):
    list_display = ("__str__", "included", "has_parser_code")


admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.XMLSiteMap, SitemapAdmin)
admin.site.register(models.ProviderCategory)
admin.site.register(models.Drug)
