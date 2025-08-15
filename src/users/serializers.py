from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        write_only=True,
        required=True
    )
    role = serializers.ChoiceField(
        choices=(
            ('RENTER', 'Renter'),
            ('LANDLORD', 'Landlord')
        ),
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'role',
            'password_confirm'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords don't match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)

        if role.lower() == 'landlord':
            group = Group.objects.get(name='Landlord')
        else:
            group = Group.objects.get(name='Renter')

        user.groups.add(group)
        return user
