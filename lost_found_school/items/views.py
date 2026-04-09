from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Item
from .forms import ItemForm
 
 
# ── Helpers ───────────────────────────────────────────────────
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)
 
def admin_required(view_func):
    return user_passes_test(is_admin, login_url='/login/')(view_func)
 
 
# ── Dashboard (admin only) ────────────────────────────────────
@admin_required
def dashboard(request):
    lost_count     = Item.objects.filter(status='lost',  is_resolved=False).count()
    found_count    = Item.objects.filter(status='found', is_resolved=False).count()
    resolved_count = Item.objects.filter(is_resolved=True).count()
    recent_items   = Item.objects.filter(is_resolved=False).order_by('-date_reported')[:5]
 
    return render(request, 'items/dashboard.html', {
        'lost_count':     lost_count,
        'found_count':    found_count,
        'resolved_count': resolved_count,
        'recent_items':   recent_items,
    })
 
 
# ── Public browse ─────────────────────────────────────────────
def home(request):
    status_filter = request.GET.get('status', '')
    query         = request.GET.get('q', '')
 
    active_items = Item.objects.filter(is_resolved=False)
    if status_filter in ['lost', 'found']:
        active_items = active_items.filter(status=status_filter)
    if query:
        active_items = active_items.filter(title__icontains=query)
 
    resolved_items = Item.objects.filter(is_resolved=True).order_by('-date_reported')[:12]
 
    return render(request, 'items/home.html', {
        'items':          active_items,
        'resolved_items': resolved_items,
        'status_filter':  status_filter,
        'query':          query,
    })
 
 
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})
 
 
# ── Admin-only item management ────────────────────────────────
@admin_required
def manage_items(request):
    status_filter = request.GET.get('status', '')
    query         = request.GET.get('q', '')
    items         = Item.objects.all()
 
    if status_filter in ['lost', 'found']:
        items = items.filter(status=status_filter)
    if query:
        items = items.filter(title__icontains=query)
 
    return render(request, 'items/manage_items.html', {
        'items':         items,
        'status_filter': status_filter,
        'query':         query,
    })
 
 
@admin_required
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            messages.success(request, 'Item posted successfully!')
            return redirect('manage_items')
    else:
        form = ItemForm()
    return render(request, 'items/post_item.html', {'form': form, 'action': 'Add'})
 
 
@admin_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('manage_items')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/post_item.html', {'form': form, 'action': 'Edit', 'item': item})
 
 
@admin_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted.')
        return redirect('manage_items')
    return render(request, 'items/confirm_delete.html', {'item': item})
 
 
@admin_required
def mark_resolved(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.is_resolved = not item.is_resolved
    item.save()
    messages.success(request, f'Item marked as {"resolved" if item.is_resolved else "reopened"}.')
    return redirect('manage_items')
 
 
# ── Auth ──────────────────────────────────────────────────────
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            # Admin → dashboard, regular user → browse reports
            if user.is_staff or user.is_superuser:
                return redirect('dashboard')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'items/login.html', {'form': form})
 
 
def logout_view(request):
    logout(request)
    return redirect('login')