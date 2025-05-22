from django.shortcuts import render
from tools.models import Tool, Category

def home(request):
    """Home page view"""
    featured_tools = Tool.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_tools': featured_tools,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)
