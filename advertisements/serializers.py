from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement, Favorite
from rest_framework.exceptions import APIException


class ValidationError(APIException):
    status_code = 400

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', )

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, )
    

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',  )

    def create(self, validated_data):
        
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        if len(Advertisement.objects.filter(status='OPEN', creator=self.context['request'].user)) > 9:
            raise ValidationError('У вас не может быть больше 10 открытых объявлений')
        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    favorite = AdvertisementSerializer(read_only=True,)
    
    class Meta:
        model = Favorite
        fields = ('user', 'favorite', )

    def create(self, validated_data):
        return super().create(validated_data)
    
    

    def validate(self, data):
        print(data)
        if Favorite.objects.filter(user=data['user'], favorite=data['favorite']):
            raise ValidationError('The Advertisement already is favorite')
        if data['favorite'].creator == data['user']:
            raise ValidationError("It's there is owner's advertisement")
        return data
        
        