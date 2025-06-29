from rest_framework import serializers
import re
from django.contrib.auth.models import User
from .models import PasswordEntry
from .utils import decrypt_password, encrypt_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {'password': {'write_only': True}}  #this avoids reading the password

    #validate input text for password and username
    def validate_username(self, username):
        disallowed_chars = ['=', '|', ';', '<', '>', '"', "'", '\\']
        sql_keywords = [
            'select', 'drop', 'insert', 'delete', 'update', 'alter',
            'create', 'exec', 'execute', 'union', 'truncate', '==', 'or', '='
        ]
        if any(char in username for char in disallowed_chars):
            raise serializers.ValidationError("Username contains disallowed characters")


        username_lower = username.lower()
        if any(keyword in username_lower for keyword in sql_keywords):
            raise serializers.ValidationError("Username contains Forbidden Characters")

        return username

    ###PASSWORD RULES
    # at least 8 characters long
    # cannot contain spaces
    # needs to have letters and numbers 
    ###
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password has to be at least 8 characters long")

        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise serializers.ValidationError("Password must include letters and numbers.")

        # forbid spaces or control characters
        if re.search(r'\s', password):
            raise serializers.ValidationError("Password cannot contain spaces.")

        return password

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user



class PasswordEntriesSerializer(serializers.ModelSerializer):
    decrypted_password = serializers.SerializerMethodField()
    password = serializers.CharField()
    class Meta:
        model = PasswordEntry
        fields = ['site_name',  'username',  'password',  'iv',  'created_at',  'decrypted_password']
        extra_kwargs = {
            "iv": {"read_only": True},"created_at": {"read_only": True}}

    #validate data agains user input
    def validate(self, data):
        sql_keywords = [
            'select', 'drop', 'insert', 'delete', 'update', 'alter',
            'create', 'exec', 'execute', 'union', 'truncate','==','or','='
        ]
        allowed_pattern = re.compile(r'^[\w.@\-]+$')


        #check each filed and validate the input
        for field in ['username', 'site_name']:
            value = data.get(field, '')
            value = value.strip()

            if any(keyword in value.lower() for keyword in sql_keywords):
                raise serializers.ValidationError({field: f"{field} contains disallowed SQL-related keywords."})
            if not allowed_pattern.match(value):
                raise serializers.ValidationError({field: f"{field} contains invalid characters."})

        return data

    def get_decrypted_password(self, obj):
        return decrypt_password(obj.password, obj.iv)

    def create(self, validated_data):
        password = validated_data.pop('password')
        encrypted_password, iv = encrypt_password(password)

        user = self.context['request'].user
        site_name = validated_data.get('site_name')

        #Create new entry if another entry already exists with the same site_name
        entry, created = PasswordEntry.objects.update_or_create(
            user=user,
            site_name=site_name,
            username=validated_data.get('username'),
            defaults = {
            'username': validated_data.get('username'),
            'password': encrypted_password,
            'iv': iv
            }
        )

        return entry

class PasswordEntryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordEntry
        fields = ['id', 'site_name', 'username', 'password']
