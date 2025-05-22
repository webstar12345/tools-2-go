from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Tool, Category, ToolImage
from .forms import ToolForm, ToolImageFormSet
from .filters import ToolFilter
from bookings.forms import BookingForm
from .models import Tool, Booking


def tool_list(request):
    """Display all available tools with filtering"""
    tools = Tool.objects.filter(available=True)
    tool_filter = ToolFilter(request.GET, queryset=tools)
    
    context = {
        'filter': tool_filter,
        'categories': Category.objects.all(),
    }
    return render(request, 'tools/tool_list.html', context)

def tool_detail(request, pk):
    """Display details of a specific tool"""
    tool = get_object_or_404(Tool, pk=pk)
    related_tools = Tool.objects.filter(category=tool.category).exclude(pk=tool.pk)[:4]
    
    context = {
        'tool': tool,
        'related_tools': related_tools,
    }
    return render(request, 'tools/tool_detail.html', context)

@login_required
def create_tool(request):
    """Create a new tool listing"""
    if request.method == 'POST':
        form = ToolForm(request.POST)
        formset = ToolImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            tool = form.save(commit=False)
            tool.owner = request.user
            tool.save()
            
            # Save the image formset
            instances = formset.save(commit=False)
            for instance in instances:
                instance.tool = tool
                instance.save()
            
            messages.success(request, 'Tool listed successfully!')
            return redirect('tool_detail', pk=tool.pk)
    else:
        form = ToolForm()
        formset = ToolImageFormSet()
    
    return render(request, 'tools/create_tool.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def update_tool(request, pk):
    """Update an existing tool"""
    tool = get_object_or_404(Tool, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool)
        formset = ToolImageFormSet(request.POST, request.FILES, instance=tool)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Tool updated successfully!')
            return redirect('tool_detail', pk=tool.pk)
    else:
        form = ToolForm(instance=tool)
        formset = ToolImageFormSet(instance=tool)
    
    return render(request, 'tools/update_tool.html', {
        'form': form,
        'formset': formset,
        'tool': tool,
    })

@login_required
def delete_tool(request, pk):
    """Delete a tool"""
    tool = get_object_or_404(Tool, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        tool.delete()
        messages.success(request, 'Tool deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'tools/delete_tool.html', {'tool': tool})

def search_tools(request):
    """Search for tools"""
    query = request.GET.get('q', '')
    tools = Tool.objects.filter(available=True)
    
    if query:
        tools = tools.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'tools': tools,
        'query': query,
    }
    return render(request, 'tools/search_results.html', context)


def create_booking(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    if request.method == 'POST':
        # Create a booking
        booking = Booking.objects.create(
            user=request.user,
            tool=tool,
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
        )
        return redirect('tools:booking_success')  # Or wherever you want
    return render(request, 'tools/create_booking.html', {'tool': tool})

def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'tools/booking_list.html', {'bookings': bookings})

def booking_success(request):
    return render(request, 'tools/booking_success.html')