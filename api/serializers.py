from rest_framework import serializers
from users.models import CustomUser
from .models import FamilyMembers


class CustomUserLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        mobile = data.get('mobile')
        full_name = data.get('full_name')
        password = data.get('password')

        if not mobile or not full_name or not password:
            raise serializers.ValidationError("Mobile number, full name, and password are required.")

        try:
            # Verify the combination of mobile and full_name
            user = CustomUser.objects.get(mobile=mobile, full_name=full_name)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid mobile number or full name.")

        # Check if the password matches
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid  password.")

        data['user'] = user
        return data






# class CustomUserSignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['full_name', 'mobile', 'email', 'password', 'confirm_password', 'address', 'thikana', 'gender', 'education', 'date_of_birth', 'profile_picture']

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data

#     def create(self, validated_data):
#         # Remove confirm_password from the validated data
#         validated_data.pop('confirm_password')

#         # Generate username from full_name
#         full_name = validated_data['full_name']
#         username = full_name.lower().replace(" ", "")

#         # Create a new user
#         user = CustomUser(
#             username=username,  # Generated username
#             full_name=validated_data['full_name'],
#             mobile=validated_data['mobile'],
#             email=validated_data['email'],
#             address=validated_data['address'],
#             thikana=validated_data['thikana'],
#             gender=validated_data['gender'],
#             education=validated_data['education'],
#             date_of_birth=validated_data['date_of_birth'],
#             profile_picture=validated_data.get('profile_picture', None)
#         )

#         # Set password using Django's built-in method
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
    

class CustomUserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'mobile', 'email', 'password', 'confirm_password', 'address', 'thikana', 'gender', 'education', 'date_of_birth', 'profile_picture']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove confirm_password from the validated data
        validated_data.pop('confirm_password')

        # Generate username from full_name
        full_name = validated_data['full_name']
        base_username = full_name.lower().replace(" ", "")
        username = base_username

        # Check if the username already exists and make it unique
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create a new user
        user = CustomUser(
            username=username,  # Unique username
            full_name=validated_data['full_name'],
            mobile=validated_data['mobile'],
            email=validated_data['email'],
            address=validated_data['address'],
            thikana=validated_data['thikana'],
            gender=validated_data['gender'],
            education=validated_data['education'],
            date_of_birth=validated_data['date_of_birth'],
            profile_picture=validated_data.get('profile_picture', None)
        )

        # Set password using Django's built-in method
        user.set_password(validated_data['password'])
        user.save()
        return user






class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMembers
        fields = ['full_name', 'address', 'thikana', 'gender', 'education', 'mobile', 'date_of_birth', 'profile_picture']
        
        




class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'mobile', 'address', 'gender', 'education', 'mobile', 'date_of_birth', 'isVerified', 'isRejected', 'profile_picture']