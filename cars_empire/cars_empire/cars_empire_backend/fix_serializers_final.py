import re

# Read the file
with open('merchants/serializers.py', 'r') as f:
    content = f.read()

# Fix get_image_url method (line 52)
old_image_method = '''    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None'''

new_image_method = '''    def get_image_url(self, obj):
        if obj.image:
            if 'request' in self.context:
                return self.context['request'].build_absolute_uri(obj.image.url)
            return obj.image.url
        return None'''

# Fix get_logo_url method (line 83)
old_logo_method = '''    def get_logo_url(self, obj):
        if obj.logo:
            if 'request' in self.context:
                return self.context['request'].build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None'''

new_logo_method = '''    def get_logo_url(self, obj):
        if obj.logo:
            if 'request' in self.context:
                return self.context['request'].build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None'''

# Replace both methods
content = content.replace(old_image_method, new_image_method)
content = content.replace(old_logo_method, new_logo_method)

# Write the file back
with open('merchants/serializers.py', 'w') as f:
    f.write(content)

print("Fixed both get_image_url and get_logo_url methods")
