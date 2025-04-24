from rest_framework import serializers

from .models import ExhibitionArea, ExhibitionContent, Artifact


class ExhibitionAreaSerializer(serializers.ModelSerializer):
    exhibition_content = serializers.SerializerMethodField()
    class Meta:
        model = ExhibitionArea
        fields = ['id', 'name', 'description', 'location', 'exhibition_content']

    def get_exhibition_content(self, obj):
        contents = obj.exhibition_area_content.all()
        results = []
        for content in contents:
            results.append({
                'id': content.id,
                'title': content.title,
                'description': content.description,
                'content_type': content.content_type,
                'artifact': self.get_artifact(content),
                'image': content.image.url if content.image else None,
                'video': content.video.url if content.video else None,
                'file': content.file.url if content.file else None
            })
        return results
    def get_artifact(self, content):
        if content.content_type == 'artifact':
            return {
                'id': content.exhibition_content_artifact.id,
                'origin': content.exhibition_content_artifact.origin
            }
        return None

class ExhibitionAreaOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExhibitionArea
        fields = ['id', 'name', 'location']

class ExhibitionContentSerializer(serializers.ModelSerializer):
    artifact = serializers.SerializerMethodField()
    exhibition_area = serializers.SerializerMethodField()
    content_type_display = serializers.SerializerMethodField()
    class Meta:
        model = ExhibitionContent
        fields = ['id', 'exhibition_area', 'title', 'description', 'content_type', 'content_type_display', 'artifact', 'image', 'video', 'file']

# Truy vấn xuôi - không cần related_name
    # Truy vấn từ model có Foreignkey đến model được tham chiếu (từ ExhibitionContent đến ExhibitionArea)
    # Không cần related_name, chỉ cần gọi thẳng tên trường Foreignkey (VD: 'id': obj.exhibition_area.id, exhibition_area là tên trường nằm trong model ExhibitionContent)
# Truy vấn ngược - cần hoặc không cần related_name (nếu không cần thì phải dùng <model>_set để lấy dữ liệu)
    # Truy vấn từ model được tham chiếu đến model có Foreignkey (từ ExhibitionContent đến Artifact)
    # Dùng related_name để truy vấn dữ liệu (VD: 'id': obj.exhibition_content_artifact.id, exhibition_content_artifact là related_name nằm trong model Artifact)

    def get_artifact(self, obj): # Truy vấn ngược
        if obj.content_type == 'artifact':
            return {
                'id': obj.exhibition_content_artifact.id,
                'origin': obj.exhibition_content_artifact.origin # Lấy origin từ đối tượng artifact liên kết với đối tượng exhibition_content
            }
        else:
            return None
        
    def get_exhibition_area(self, obj): # Truy vấn xuôi
        return {
            'id': obj.exhibition_area.id, 
            'name': obj.exhibition_area.name,
            'description:': obj.exhibition_area.description, 
            'location': obj.exhibition_area.location
        }
    
    def get_content_type_display(self, obj): # giúp hiển thị giá trị thân thiện (human-readable) của một trường có lựa chọn (choices) (artifact -> Hiện vật)
        return obj.get_content_type_display() # là một phương thức tự động của Django cho các trường choices trong Model
    
class ExhibitionContentOverviewSerializer(serializers.ModelSerializer):
    content_type_display = serializers.SerializerMethodField()
    class Meta:
        model = ExhibitionContent
        fields = ['id', 'title', 'content_type', 'content_type_display']

    def get_content_type_display(self, obj):
        return obj.get_content_type_display() 

class ArtifactSerializer(serializers.ModelSerializer):
    exhibition_content = serializers.SerializerMethodField()
    class Meta:
        model = Artifact
        fields = ['id', 'exhibition_content', 'origin', 'material', 'year']

    def get_exhibition_content(self, obj):
        content = obj.exhibition_content # Lấy ra nội dung trưng bày liên kết với hiện vật
        return {
            'id': content.id,
            'exhibition_area': self.get_exhibition_area(content), # Lấy thông về khu vực trưng bày của nội dung trưng bày thuộc về hiện vật
            'title': content.title,
            'description': content.description,
            'content_type': content.content_type,
            'image': content.image.url if content.image else None,
            'video': content.video.url if content.video else None,
            'file': content.file.url if content.file else None
        }
    def get_exhibition_area(self, content): # Nhận content (nội dung trưng bày) làm tham số. lúc này content chính là obj nội dung
        return {
            'id': content.exhibition_area.id, # Lấy ra id của khu vực trưng bày
            'name': content.exhibition_area.name,
            'description:': content.exhibition_area.description, 
            'location': content.exhibition_area.location
        }