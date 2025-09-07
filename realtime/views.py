from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from django.apps import apps
from .models import ShoppingSession
import uuid


@login_required
def dashboard(request):
    """Enhanced dashboard with live shopping features"""
    UserModel = apps.get_model(settings.AUTH_USER_MODEL)
    
    # Get referral code
    referral_code = getattr(request.user, "referral_code", None)
    if not referral_code and hasattr(request.user, "userprofile"):
        referral_code = getattr(request.user.userprofile, "referral_code", None)
    
    referral_link = request.build_absolute_uri(
        f"/accounts/register/?ref={referral_code or ''}"
    )
    
    # Get user sessions
    active_sessions = ShoppingSession.objects.filter(host=request.user, is_active=True)
    joined_sessions = request.user.joined_shopping_sessions.filter(is_active=True)
    
    # Get referred users if applicable
    referred_users = []
    if hasattr(UserModel, "referred_by"):
        referred_users = UserModel.objects.filter(referred_by=request.user)
    
    total_referrals = referred_users.count() if referred_users else 0
    
    context = {
        "referral_code": referral_code,
        "referral_link": referral_link,
        "active_sessions": active_sessions,
        "joined_sessions": joined_sessions,
        "referred_users": referred_users,
        "total_referrals": total_referrals,
        "user": request.user,
    }
    
    return render(request, "realtime/referral_dashboard.html", context)


@login_required
def create_session(request):
    """Create a new live shopping session"""
    if request.method == 'POST':
        session_name = request.POST.get('session_name', f"{request.user.email}'s Shopping Session")
    else:
        session_name = f"{request.user.email}'s Shopping Session"
    
    session = ShoppingSession.objects.create(
        host=request.user,
        session_name=session_name
    )
    
    invite_url = request.build_absolute_uri(
        reverse("realtime:join_session", args=[str(session.session_id)])
    )
    
    messages.success(
        request,
        f"Live session created! Share this link with friends: {invite_url}",
    )
    
    return redirect("realtime:live_shopping_room", room_name=str(session.session_id))


@login_required
def live_shopping_room(request, room_name):
    """Main live shopping room with products, chat, and voice features"""
    session = get_object_or_404(ShoppingSession, session_id=room_name, is_active=True)
    
    # Auto-add participant if not host
    if request.user != session.host and request.user not in session.participants.all():
        session.participants.add(request.user)
    
    # Get referral info
    referral_code = getattr(request.user, "referral_code", None)
    if not referral_code and hasattr(request.user, "userprofile"):
        referral_code = getattr(request.user.userprofile, "referral_code", None)
    
    referral_link = request.build_absolute_uri(
        f"/accounts/register/?ref={referral_code or ''}"
    )
    
    invite_link = request.build_absolute_uri(
        reverse("realtime:join_session", args=[str(session.session_id)])
    )
    
    # Sample products - replace with your actual Product model
    sample_products = [
        {
            "id": "smartphone-pro",
            "name": "iPhone 15 Pro Max 256GB",
            "price": "999.99",
            "image": "https://via.placeholder.com/280x220/007bff/ffffff?text=iPhone+15",
            "category": "Electronics",
            "rating": 4.8,
            "reviews": 2431,
        },
        {
            "id": "laptop-gaming",
            "name": "Gaming Laptop RTX 4080",
            "price": "1899.99",
            "image": "https://via.placeholder.com/280x220/28a745/ffffff?text=Gaming+Laptop",
            "category": "Electronics",
            "rating": 4.9,
            "reviews": 1567,
        },
        {
            "id": "cotton-tshirt",
            "name": "Premium Cotton T-Shirt",
            "price": "29.99",
            "image": "https://via.placeholder.com/280x220/ffc107/ffffff?text=T-Shirt",
            "category": "Clothing",
            "rating": 4.2,
            "reviews": 856,
        },
        {
            "id": "wireless-headphones",
            "name": "Sony WH-1000XM5 Headphones",
            "price": "399.99",
            "image": "https://via.placeholder.com/280x220/17a2b8/ffffff?text=Headphones",
            "category": "Electronics",
            "rating": 4.9,
            "reviews": 3241,
        },
        {
            "id": "running-shoes",
            "name": "Nike Air Max Running Shoes",
            "price": "149.99",
            "image": "https://via.placeholder.com/280x220/6f42c1/ffffff?text=Nike+Shoes",
            "category": "Clothing",
            "rating": 4.6,
            "reviews": 1823,
        },
        {
            "id": "kindle-reader",
            "name": "Kindle Paperwhite E-reader",
            "price": "139.99",
            "image": "https://via.placeholder.com/280x220/fd7e14/ffffff?text=Kindle",
            "category": "Books",
            "rating": 4.5,
            "reviews": 9876,
        },
    ]
    
    context = {
        "room_name": str(room_name),
        "session": session,
        "is_host": session.host == request.user,
        "participants": session.participants.all(),
        "participant_count": session.participants.count() + 1,
        "products": sample_products,
        "invite_link": invite_link,
        "referral_link": referral_link,
        "user": request.user,
    }
    
    return render(request, "realtime/live_shopping.html", context)


@login_required
def shopping_room(request, room_name):
    """Simple shopping room (legacy compatibility)"""
    return live_shopping_room(request, room_name)


@login_required
def join_session(request, session_id):
    """Join an existing session"""
    session = get_object_or_404(ShoppingSession, session_id=session_id, is_active=True)
    
    if request.user != session.host and request.user not in session.participants.all():
        session.participants.add(request.user)
        messages.success(request, f"Joined {session.host.email}'s shopping session!")
    
    return redirect("realtime:live_shopping_room", room_name=str(session.session_id))


@login_required
def end_session(request, session_id):
    """Host ends the session"""
    session = get_object_or_404(ShoppingSession, session_id=session_id, host=request.user)
    session.is_active = False
    session.save()
    
    messages.success(request, "Session ended successfully.")
    return redirect("realtime:dashboard")


@login_required
def leave_session(request, session_id):
    """Participant leaves the session"""
    session = get_object_or_404(ShoppingSession, session_id=session_id, is_active=True)
    
    if request.user in session.participants.all():
        session.participants.remove(request.user)
        messages.success(request, "You left the session.")
    
    return redirect("realtime:dashboard")


@login_required
def browse_sessions(request):
    """Browse available sessions to join"""
    sessions = (
        ShoppingSession.objects.filter(is_active=True)
        .exclude(host=request.user)
        .exclude(participants=request.user)
        .order_by("-created_at")[:20]
    )
    
    return render(request, "realtime/browse_sessions.html", {"sessions": sessions})


# API endpoints
@login_required
def session_details_api(request, session_id):
    """API endpoint for session details"""
    session = get_object_or_404(ShoppingSession, session_id=session_id, is_active=True)
    
    return JsonResponse({
        "session_id": str(session.session_id),
        "host": session.host.email,
        "participants": [u.email for u in session.participants.all()],
        "participant_count": session.participants.count() + 1,
        "is_host": request.user == session.host,
        "created_at": session.created_at.isoformat(),
    })


@login_required
def test_websocket(request):
    """Test WebSocket connection"""
    return JsonResponse({
        "status": "success",
        "message": "WebSocket endpoints are configured",
        "user": request.user.email,
        "websocket_url": f"ws://{request.get_host()}/ws/shopping/test-room/",
    })