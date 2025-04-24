from rest_framework import serializers

from .models import HistoricalFigure, ImageFolder, HistoricalImage, HistoricalFilm, HistoricalDocument


class HistoricalFigureSerializer(serializers.ModelSerializer):
    image_folder_list = serializers.SerializerMethodField()
    historical_film = serializers.SerializerMethodField()
    historical_document = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    class Meta:
        model = HistoricalFigure
        fields = ['id', 'name', 'avatar', 'birth_date', 'death_date', 
                  'description', 'category', 'category_display', 'is_approve', 
                  'image_folder_list', 'historical_film', 'historical_document']
        
    def get_image_folder_list(self, obj):
        images_folder_list = obj.historical_figure_folder.all()
        results = []
        for image_folder_list in images_folder_list:
            results.append({
                'id': image_folder_list.id,
                'name': image_folder_list.name,
                'description': image_folder_list.description,
                'image_list': self.get_image_list(image_folder_list),
            })
        return results
    
    def get_image_list(self, image_folder_list):
        images_list = image_folder_list.folder_image.all()
        results = []
        for image_list in images_list:
            results.append({
                'image': image_list.image.url,
                'description': image_list.description,
            })
        return results
    
    def get_historical_film(self, obj):
        films = obj.historical_figure_film.all()
        results = []
        for film in films:
            results.append({
                'id': film.id,
                'title': film.title,
                'video': film.video.url,
                'description': film.description,
                'director': film.director,
                'release_year': film.release_year,
                'is_approve': film.is_approve,
            })
        return results
    
    def get_historical_document(self, obj):
        documents = obj.historical_figure_document.all()
        results = []
        for document in documents:
            results.append({
                'id': document.id,
                'title': document.title,
                'content': document.content,
                'document_type': document.document_type,
                'author': document.author,
                'publish_year': document.publish_year,
                'file': document.file.url,
            })
        return results
    
    def get_category_display(self, obj):
        return obj.get_category_display()
    
class HistoricalFigureOverviewSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()
    class Meta:
        model = HistoricalFigure
        fields = ['id', 'name', 'avatar', 'category', 'category_display', 'is_approve']

    def get_category_display(self, obj):
        return obj.get_category_display()

class ImageFolderSerializer(serializers.ModelSerializer):
    historical_figure = serializers.SerializerMethodField()
    image_list = serializers.SerializerMethodField()
    class Meta:
        model = ImageFolder
        fields = ['id', 'name', 'description', 'historical_figure', 'image_list']

    def get_historical_figure(self, obj):
        return {
            'id': obj.historical_figure.id,
            'name': obj.historical_figure.name,
            'avatar': obj.historical_figure.avatar.url if obj.historical_figure.avatar else None,
            'birth_date': obj.historical_figure.birth_date,
            'death_date': obj.historical_figure.death_date,
            'description': obj.historical_figure.description,
            'category': obj.historical_figure.category,
            'is_approve': obj.historical_figure.is_approve
        }
    
    def get_image_list(self, obj):
        images = obj.folder_image.all()
        results = []
        for image in images:
            results.append({
                'image': image.image.url,
                'description': image.description,
            })
        return results
    
class ImageFolderOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFolder
        fields = ['id', 'name']

class HistoricalImageSerializer(serializers.ModelSerializer):
    folder = serializers.SerializerMethodField()
    class Meta:
        model = HistoricalImage
        fields = ['id', 'image', 'description', 'folder']

    def get_folder(self, obj):
        folder = obj.folder
        return {
            'id': folder.id,
            'name': folder.name,
            'description': folder.description,
            'historical_figure': self.get_historical_figure(folder),
        }
    
    def get_historical_figure(self, folder):
        return {
            'id': folder.historical_figure.id,
            'name': folder.historical_figure.name,
            'avatar': folder.historical_figure.avatar.url if folder.historical_figure.avatar else None,
            'birth_date': folder.historical_figure.birth_date,
            'death_date': folder.historical_figure.death_date,
            'description': folder.historical_figure.description,
            'category': folder.historical_figure.category,
            'is_approve': folder.historical_figure.is_approve
        }
    
class HistoricalImageOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalImage
        fields = ['id', 'image']

class HistoricalFilmSerializer(serializers.ModelSerializer):
    historical_figure = serializers.SerializerMethodField()
    class Meta:
        model = HistoricalFilm
        fields = ['id', 'title', 'video', 'description', 'director', 'release_year', 'is_approve', 'historical_figure']

    def get_historical_figure(self, obj):
        return {
            'id': obj.historical_figure.id,
            'name': obj.historical_figure.name,
            'avatar': obj.historical_figure.avatar.url if obj.historical_figure.avatar else None,
            'birth_date': obj.historical_figure.birth_date,
            'death_date': obj.historical_figure.death_date,
            'description': obj.historical_figure.description,
            'category': obj.historical_figure.category,
            'is_approve': obj.historical_figure.is_approve,
        }
    
class HistoricalFilmOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalFilm
        fields = ['id', 'title', 'video', 'release_year', 'is_approve']

class HistoricalDocumentSerializer(serializers.ModelSerializer):
    historical_figure = serializers.SerializerMethodField()
    document_type_display = serializers.SerializerMethodField()
    class Meta:
        model = HistoricalDocument
        fields = ['id', 'title', 'content', 'document_type', 'document_type_display', 
                  'author', 'publish_year', 'file', 'historical_figure']

    def get_historical_figure(self, obj):
        return {
            'id': obj.historical_figure.id,
            'name': obj.historical_figure.name,
            'avatar': obj.historical_figure.avatar.url if obj.historical_figure.avatar else None,
            'birth_date': obj.historical_figure.birth_date,
            'death_date': obj.historical_figure.death_date,
            'description': obj.historical_figure.description,
            'category': obj.historical_figure.category,
            'is_approve': obj.historical_figure.is_approve,
        }
    
    def get_document_type_display(self, obj):
        return obj.get_document_type_display()
        
class HistoricalDocumentOverviewSerializer(serializers.ModelSerializer):
    document_type_display = serializers.SerializerMethodField()
    class Meta:
        model = HistoricalDocument
        fields = ['id', 'title', 'document_type', 'document_type_display', 'publish_year']

    def get_document_type_display(self, obj):
        return obj.get_document_type_display()