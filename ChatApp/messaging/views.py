# messaging/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User  # Import User model
from .models import Message
from .serializers import MessageSerializer
from .forms import ComposeForm, UserRegisterForm  # Ensure you have these forms defined
from .utils import encrypt_message, decrypt_message, generate_key
from rest_framework.permissions import IsAuthenticated

# Home view
def home(request):
    return HttpResponse("Welcome to the Secure Messaging System!")

# Inbox view
@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messaging/inbox.html', {'messages': messages})

# Compose message view
@login_required
def compose(request):
    if request.method == 'POST':
        form = ComposeForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # Set the sender to the current user

            # Get recipient by username
            recipient_username = form.cleaned_data['recipient']  # Assuming your form includes recipient
            try:
                message.recipient = User.objects.get(username=recipient_username)  # Set the recipient
            except User.DoesNotExist:
                form.add_error('recipient', 'User does not exist.')  # Handle invalid recipient

            message.save()
            return redirect('inbox')
    else:
        form = ComposeForm()
    return render(request, 'messaging/compose.html', {'form': form})

# View individual message
@login_required
def message_view(request, id):
    message = get_object_or_404(Message, id=id, recipient=request.user)
    return render(request, 'messaging/message_view.html', {'message': message})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inbox')  # Redirect to inbox on successful login
        else:
            # Handle invalid login
            error_message = "Invalid username or password"
            return render(request, 'messaging/login.html', {'error': error_message})
    return render(request, 'messaging/login.html')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserRegisterForm()
    return render(request, 'messaging/register.html', {'form': form})

# API views for sending and receiving messages
class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        key = generate_key()  # Generate a new key for each message
        encrypted_content = encrypt_message(serializer.validated_data['content'], key)
        serializer.save(sender=self.request.user, content=encrypted_content)

class ReceiveMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)

@login_required
def reply_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.recipient = original_message.sender
            new_message.subject = f"Re: {original_message.subject}"
            new_message.save()
            return redirect('inbox')  # Redirect to inbox after sending
    else:
        form = MessageForm()
    return render(request, 'messaging/reply.html', {'form': form, 'original_message': original_message})

@login_required
def forward_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.recipient = form.cleaned_data['recipient']  # Assuming recipient is selected from the form
            new_message.subject = f"Fwd: {original_message.subject}"
            new_message.body = original_message.body  # Forwarding original message body
            new_message.save()
            return redirect('inbox')  # Redirect to inbox after sending
    else:
        form = MessageForm()
    return render(request, 'messaging/forward.html', {'form': form, 'original_message': original_message})

@login_required
def mark_as_unread(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = False  # Assuming there's an `is_read` field in your Message model
    message.save()
    return redirect('inbox')


