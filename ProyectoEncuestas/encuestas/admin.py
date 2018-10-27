from django.contrib import admin

from .models import Pregunta, Opcion

class PreguntaInline(admin.TabularInline):

	model=Opcion
	extra=3

class PreguntaAdmin(admin.ModelAdmin):

	fieldsets=[

		(None, {'fields':['pregunta']}),
		('Fecha', {'fields':['fecha_publicacion'], 'classes':['collapse']}),
	]
	
	inlines=[PreguntaInline]

	list_display=('pregunta','fecha_publicacion','publicada_recientemente')

	list_filter=['fecha_publicacion']

	search_fields=['pregunta']

admin.site.register(Pregunta, PreguntaAdmin)


