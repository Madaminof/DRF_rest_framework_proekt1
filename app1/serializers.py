from rest_framework import serializers
from .models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

    def validate_name(self, name):
        for i in name:
            if not i.isalpha():
                raise serializers.ValidationError('Name harfdan iborat bolishi kerak')
        return name

    def validate_surname(self, surname):
        for i in surname:
            if not i.isalpha():
                raise serializers.ValidationError('Surname harfdan iborat bolishi kerak')
        return surname

    def validate_age(self, age):
        if age < 1 and age > 100:
            raise serializers.ValidationError('Yosh 0 dan Katta bo\'lishi kerak')
        return age

    # phone = uzb raqam
    def validate_phone(self, phone):
        if phone[0] != '+' and len(phone) != 13:
            raise serializers.ValidationError('+ bilan boshlanishi kerak va raqam uzunligi 13ta bolsin!')
        return phone

    def validate_username(self, username):
        if len(username) < 5:
            raise serializers.ValidationError('Username uzunligi 5ta bolsin!')
        return username













