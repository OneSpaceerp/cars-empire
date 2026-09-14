import re

# Read the file
with open('merchants/serializers.py', 'r') as f:
    content = f.read()

# Fix the get_logo_url method with proper indentation
old_method = '''    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None'''

new_method = '''    def get_logo_url(self, obj):
        if obj.logo:
            if 'request' in self.context:
                return self.context['request'].build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None'''

# Replace the method
content = content.replace(old_method, new_method)

# Write the file back
with open('merchants/serializers.py', 'w') as f:
    f.write(content)

print("Fixed get_logo_url method with proper indentation")
