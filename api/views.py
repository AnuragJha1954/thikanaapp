from django.shortcuts import render

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (
    CustomUserLoginSerializer,
    CustomUserSignupSerializer,
    FamilyMemberSerializer,
    UserListSerializer
)
from users.models import CustomUser
from .models import FamilyMembers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
import requests
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method="post",
    request_body=CustomUserLoginSerializer,
    responses={
        status.HTTP_200_OK: "User Logged in successfully",
        status.HTTP_400_BAD_REQUEST: "Invalid credentials",
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    try:
        if request.method == "POST":
            serializer = CustomUserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                token, _ = Token.objects.get_or_create(user=user)

                # Get additional user details including full name
                user_details = {
                    "id": user.id,
                    "username": user.username,
                    "mobile": user.mobile,
                    "full_name": user.full_name,
                    "email": user.email,
                    "address": user.address,
                    "thikana": user.thikana,
                    "gender": user.gender,
                    "education": user.education,
                    "date_of_birth": user.date_of_birth,
                    "relationship_status": user.relationship_status,
                    "pincode": user.pincode,
                    "verified": user.isVerified,
                    "rejected": user.isRejected,
                    "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
                }

                return Response(
                    {
                        "error": False,
                        "detail": "User logged in successfully",
                        "token": token.key,
                        "user_details": user_details,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": True, "detail": "Invalid mobile number, full name, or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )





# Demo Body
# {
#     "full_name": "John Doe",
#     "mobile": "1234567890",
#     "email": "john@example.com",
#     "password": "password123",
#     "confirm_password": "password123",
#     "address": "123 Main St",
#     "thikana": "Home",
#     "gender": "Male",
#     "education": "Bachelor's",
#     "date_of_birth": "1990-01-01",
#     "profile_picture": null
# }


@swagger_auto_schema(
    method='post',
    request_body=CustomUserSignupSerializer,
    responses={
        201: openapi.Response(
            description="User signed up successfully",
            schema=CustomUserSignupSerializer(),
        ),
        400: openapi.Response(
            description="Invalid input data",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'detail': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )
        ),
        500: openapi.Response(
            description="Internal server error",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        )
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    try:
        if request.method == "POST":
            serializer = CustomUserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                return Response(
                    {
                        "error": False,
                        "detail": "User signed up successfully",
                        "user_details": {
                            "id": user.id,
                            "username": user.username,
                            "full_name": user.full_name,
                            "email": user.email,
                            "mobile": user.mobile,
                            "address": user.address,
                            "thikana": user.thikana,
                            "gender": user.gender,
                            "education": user.education,
                            "date_of_birth": user.date_of_birth,
                            "relationship_status": user.relationship_status,
                            "pincode": user.pincode,
                            "verified": user.isVerified,
                            "rejected": user.isRejected,
                            "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
                        }
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"error": True, "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )








@swagger_auto_schema(
    method='post',
    operation_summary="Add a Family Member",
    operation_description="Adds a new family member for a verified user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the family member'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the family member'),
            'thikana': openapi.Schema(type=openapi.TYPE_STRING, description='Thikana of the family member'),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender of the family member'),
            'education': openapi.Schema(type=openapi.TYPE_STRING, description='Education of the family member'),
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='Mobile number of the family member'),
            'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of birth of the family member'),
            'isVerified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Verification status of the family member'),
            'isRejected': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Rejection status of the family member'),
            'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='Profile picture of the family member', format=openapi.FORMAT_BINARY),
        },
        required=['full_name', 'address', 'thikana', 'gender', 'education', 'mobile'],
    ),
    responses={
        201: openapi.Response('Family member added successfully.'),
        400: openapi.Response('Invalid input.'),
        403: openapi.Response('User is not verified.'),
        401: openapi.Response('Unauthorized access.'),
        500: openapi.Response('Internal server error.')
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def add_family_member(request, user_id):
    try:
        
        # Check if the user exists and get the user object
        user = get_object_or_404(CustomUser, id=user_id)

        # Get the token from the request headers
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if not token_key:
            return Response(
                {"error": True, "detail": "Authorization header is missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Extract the token
        token = token_key.strip()  # Use the token directly as passed
        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response(
                {"error": True, "detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the token corresponds to the user
        if token_obj.user != user:
            return Response(
                {"error": True, "detail": "Unauthorized access."},
                status=status.HTTP_403_FORBIDDEN,
            )

        

        # Check if the user is verified
        if not user.isVerified:
            return Response(
                {"error": True, "detail": "User is not verified."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # If all checks pass, create a new family member
        serializer = FamilyMemberSerializer(data=request.data)
        if serializer.is_valid():
            family_member = serializer.save(added_by=user)
            return Response(
                {
                    "error": False,
                    "detail": "Family member added successfully.",
                    "family_member": serializer.data
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": True, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )












@swagger_auto_schema(
    method='get',
    operation_summary="Get Family Members",
    operation_description="Retrieves all family members added by a specific user.",
    responses={
        200: openapi.Response(
            'List of family members',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Error status'),
                    'family_members': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the family member'),
                                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the family member'),
                                'thikana': openapi.Schema(type=openapi.TYPE_STRING, description='Thikana of the family member'),
                                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender of the family member'),
                                'education': openapi.Schema(type=openapi.TYPE_STRING, description='Education of the family member'),
                                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='Mobile number of the family member'),
                                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of birth of the family member'),
                                'isVerified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Verification status of the family member'),
                                'isRejected': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Rejection status of the family member'),
                                'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='Profile picture of the family member', format=openapi.FORMAT_URI),
                            },
                        ),
                    ),
                },
            ),
        ),
        404: openapi.Response('User not found.'),
        500: openapi.Response('Internal server error.')
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_family_members(request, user_id):
    try:
        # Check if the user exists
        user = get_object_or_404(CustomUser, id=user_id)

        # Retrieve all family members added by the user
        family_members = FamilyMembers.objects.filter(added_by=user)

        # Serialize the family member data
        family_member_data = [
            {
                "member_id": member.id,
                "full_name": member.full_name,
                "address": member.address,
                "thikana": member.thikana,
                "gender": member.gender,
                "education": member.education,
                "mobile": member.mobile,
                "date_of_birth": member.date_of_birth,
                "relationship_status": member.relationship_status,
                "profile_picture": member.profile_picture.url if member.profile_picture else None,
            }
            for member in family_members
        ]

        return Response(
            {
                "error": False,
                "family_members": family_member_data,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )











@swagger_auto_schema(
    method='put',
    operation_summary="Edit Family Member Details",
    operation_description="Allows a verified user to edit details of a family member.",
    responses={
        200: openapi.Response(
            'Family member details updated successfully.',
            FamilyMemberSerializer()
        ),
        400: openapi.Response(
            'Invalid data.',
            examples={'application/json': {"error": True, "detail": "Validation error details"}}
        ),
        403: openapi.Response(
            'User is not verified.',
            examples={'application/json': {"error": True, "detail": "User is not verified."}}
        ),
        404: openapi.Response(
            'Family member not found.',
            examples={'application/json': {"error": True, "detail": "Not found."}}
        ),
    },
    request_body=FamilyMemberSerializer(),
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_family_member(request, user_id, family_member_id):
    try:
        # Get the user object
        user = get_object_or_404(CustomUser, id=user_id)
        
        # Get the token from the request headers
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if not token_key:
            return Response(
                {"error": True, "detail": "Authorization header is missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Extract the token
        token = token_key.strip()  # Use the token directly as passed
        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response(
                {"error": True, "detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the token corresponds to the user
        if token_obj.user != user:
            return Response(
                {"error": True, "detail": "Unauthorized access."},
                status=status.HTTP_403_FORBIDDEN,
            )        


        # Check if the user is verified
        if not user.isVerified:
            return Response(
                {"error": True, "detail": "User is not verified."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the family member object
        family_member = get_object_or_404(FamilyMembers, id=family_member_id, added_by=user)

        # Deserialize and update the family member details with partial updates
        serializer = FamilyMemberSerializer(family_member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": False, "detail": "Family member details updated successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": True, "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )











@swagger_auto_schema(
    method='delete',
    operation_summary="Delete Family Member",
    operation_description="Allows a verified user to delete a family member.",
    responses={
        204: openapi.Response('Family member deleted successfully.'),
        403: openapi.Response(
            'User is not verified.',
            examples={'application/json': {"error": True, "detail": "User is not verified."}}
        ),
        404: openapi.Response(
            'Family member not found.',
            examples={'application/json': {"error": True, "detail": "Not found."}}
        ),
    },
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_family_member(request, user_id, family_member_id):
    try:
        # Get the user object
        user = get_object_or_404(CustomUser, id=user_id)
        
        # Get the token from the request headers
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if not token_key:
            return Response(
                {"error": True, "detail": "Authorization header is missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Extract the token
        token = token_key.strip()  # Use the token directly as passed
        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response(
                {"error": True, "detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the token corresponds to the user
        if token_obj.user != user:
            return Response(
                {"error": True, "detail": "Unauthorized access."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if the user is verified
        if not user.isVerified:
            return Response(
                {"error": True, "detail": "User is not verified."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the family member object
        family_member = get_object_or_404(FamilyMembers, id=family_member_id, added_by=user)

        # Delete the family member
        family_member.delete()

        return Response(
            {"error": False, "detail": "Family member deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )













@swagger_auto_schema(
    method='get',
    operation_summary="Get All Users",
    operation_description="Retrieve a list of all users excluding superadmin. Optionally filter by full name.",
    manual_parameters=[
        openapi.Parameter(
            'full_name',
            openapi.IN_QUERY,
            description="Filter users by full name (case insensitive).",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        200: openapi.Response(
            'Successful Response',
            UserListSerializer(many=True)
        ),
        403: openapi.Response(
            'Forbidden',
            examples={'application/json': {"error": True, "detail": "You do not have permission to perform this action."}}
        ),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users(request):
    try:
        # Get the search query parameter
        search_full_name = request.query_params.get('full_name', '')

        # Fetch users excluding superadmin and filter by full name if provided
        users = CustomUser.objects.exclude(is_superuser=True)

        if search_full_name:
            users = users.filter(full_name__icontains=search_full_name)

        # Serialize user data
        serializer = UserListSerializer(users, many=True)

        return Response(
            {
                "error": False,
                "users": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )














@swagger_auto_schema(
    method='patch',
    operation_summary="Verify User",
    operation_description="Set the isVerified field to True for a user. Requires super admin permission.",
    responses={
        200: openapi.Response(
            'Successful Response',
            examples={'application/json': {"error": False, "detail": "User has been verified successfully."}}
        ),
        403: openapi.Response(
            'Forbidden',
            examples={'application/json': {"error": True, "detail": "Permission denied. You are not a super admin."}}
        ),
        404: openapi.Response(
            'Not Found',
            examples={'application/json': {"error": True, "detail": "User not found."}}
        ),
    },
)
@api_view(['PATCH'])
@permission_classes([AllowAny])
def verify_user(request, user_id, admin_id):
    try:
        # Check if the requesting user is a super admin
        admin_user = CustomUser.objects.get(id=admin_id)
        
        if not admin_user.is_superuser:
            return Response(
                {"error": True, "detail": "Permission denied. You are not a super admin."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fetch the user to be verified
        user_to_verify = CustomUser.objects.get(id=user_id)

        # Update the isVerified field
        user_to_verify.isVerified = True
        user_to_verify.save()

        return Response(
            {
                "error": False,
                "detail": f"User {user_to_verify.full_name} has been verified successfully."
            },
            status=status.HTTP_200_OK,
        )

    except CustomUser.DoesNotExist:
        return Response(
            {"error": True, "detail": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )










@swagger_auto_schema(
    method='patch',
    operation_summary="Reject User",
    operation_description="Set the isRejected field to True for a user. Requires super admin permission.",
    responses={
        200: openapi.Response(
            'Successful Response',
            examples={'application/json': {"error": False, "detail": "User has been rejected successfully."}}
        ),
        403: openapi.Response(
            'Forbidden',
            examples={'application/json': {"error": True, "detail": "Permission denied. You are not a super admin."}}
        ),
        404: openapi.Response(
            'Not Found',
            examples={'application/json': {"error": True, "detail": "User not found."}}
        ),
    },
)
@api_view(['PATCH'])
@permission_classes([AllowAny])
def reject_user(request, user_id, admin_id):
    try:
        # Check if the requesting user is a super admin
        admin_user = CustomUser.objects.get(id=admin_id)
        
        if not admin_user.is_superuser:
            return Response(
                {"error": True, "detail": "Permission denied. You are not a super admin."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fetch the user to be rejected
        user_to_reject = CustomUser.objects.get(id=user_id)

        # Update the isRejected field
        user_to_reject.isRejected = True
        user_to_reject.save()

        return Response(
            {
                "error": False,
                "detail": f"User {user_to_reject.full_name} has been rejected successfully."
            },
            status=status.HTTP_200_OK,
        )

    except CustomUser.DoesNotExist:
        return Response(
            {"error": True, "detail": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"error": True, "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )






