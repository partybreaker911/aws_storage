import rsa

from django.views.generic import View, CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.storage.models import Folder, File, FileSignature
from apps.accounts.models import RSAKeyPair
from apps.storage.forms import FileUploadForm

# from apps.storage.services.files import FileUploadService


# class FileUploadView(LoginRequiredMixin, View):
#     template_name = "storage/file_upload.html"

#     def get(self, request: HttpRequest) -> HttpResponse:
#         """Handles GET requests to the view.

#         Args:
#             request (HttpRequest): The HTTP request object.

#         Returns:
#             HttpResponse: The HTTP response object.
#         """
#         form = FileUploadForm()
#         context = {
#             "form": form,
#         }
#         return render(request, self.template_name, context)

#     def post(self, request: HttpRequest) -> HttpResponse:
#         """
#         Handle HTTP POST requests.

#         Args:
#             request (HttpRequest): The HTTP request object.

#         Returns:
#             HttpResponse: The HTTP response object.

#         """
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.cleaned_data["file"]
#             name = file.name
#             user = request.user

#             file_obj = FileUploadService.upload_file(user=user, name=name, file=file)
#             return redirect("dashboard:dashboard")
#         return render(request, self.template_name)


# class FileUploadView(CreateView):
# template_name = "storage/file_upload.html"
# form_class = FileUploadForm
# success_url = "/"

# def form_valid(self, form):
#     # Get the uploaded file
#     uploaded_file = form.cleaned_data["file"]

#     # Retrieve the RSA key pair for the current user
#     user = self.request.user
#     rsa_key_pair = RSAKeyPair.objects.get(user=user)

#     # Extract the public key from the stored key pair
#     public_key = rsa.PublicKey.load_pkcs1_openssl_pem(
#         rsa_key_pair.public_key.encode()
#     )

#     # Encrypt the uploaded file
#     encrypted_file = rsa.encrypt(uploaded_file.read(), public_key)

#     # Sign the encrypted file
#     signature = rsa.sign(encrypted_file, rsa_key_pair.private_key, "SHA-256")

#     # Save the encrypted file and signature in the database
#     file_obj = File(user=user, name=uploaded_file.name, file=uploaded_file)
#     file_obj.save()

#     signature_obj = FileSignature(file=file_obj, signature=signature)
#     signature_obj.save()

#     return super().form_valid(form)


from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes,
)
from Crypto.Random import get_random_bytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


class FileUploadView(LoginRequiredMixin, CreateView):
    template_name = "storage/file_upload.html"
    form_class = FileUploadForm
    success_url = "/"

    def form_valid(self, form):
        # Get the uploaded file
        uploaded_file = form.cleaned_data["file"]

        # Retrieve the RSA key pair for the current user
        user = self.request.user
        rsa_key_pair = RSAKeyPair.objects.get(user=user)

        # Load the private key
        private_key = serialization.load_pem_private_key(
            rsa_key_pair.private_key.encode(), password=None, backend=default_backend()
        )

        # Sign the uploaded file
        file_data = uploaded_file.read()
        signature = private_key.sign(
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        # Create the file object and set the user and other fields
        file_obj = File(
            user=self.request.user, name=uploaded_file.name, file=uploaded_file
        )

        # Save the file object
        file_obj.save()

        # Set the signature object for the file
        signature_obj = FileSignature.objects.create(file=file_obj, signature=signature)

        # Save the signature object
        signature_obj.save()

        return super().form_valid(form)
