import re

# Read the file
with open('deals/views.py', 'r') as f:
    content = f.read()

# Find and replace the problematic line
old_line = "        category = self.request.query_params.get('category', None)"
new_line = "        # Get query parameters - handle both DRF and Django requests\n        if hasattr(self.request, 'query_params'):\n            # DRF request\n            query_params = self.request.query_params\n        else:\n            # Django request\n            query_params = self.request.GET\n        \n        category = query_params.get('category', None)"

# Replace the line
content = content.replace(old_line, new_line)

# Also fix other query_params references
content = content.replace("self.request.query_params.get", "query_params.get")

# Write the file back
with open('deals/views.py', 'w') as f:
    f.write(content)

print("Fixed get_queryset method to handle both DRF and Django requests")
