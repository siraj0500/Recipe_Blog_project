from django.contrib import admin
from .models import RecipePost


# class IngredientInline(admin.TabularInline):
#     model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_name','short_description','ingredients','cooking_directions', 'cooking_tips', 'cooking_time', 'preparation_time',
                    'recipe_images', 'recipe_datePosted')
    list_filter = ("status",)
    search_fields = ['recipe_name', 'cooking_directions']


admin.site.register(RecipePost, RecipeAdmin)
admin.site.site_header = "God's Own Recipe"
