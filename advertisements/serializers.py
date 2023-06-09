from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework import serializers
from advertisements.models import Advertisement, Favorite

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', )

class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(read_only=True, )
    

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',  )

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию. # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя. # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet. # само поле при этом объявляется как `read_only=True`
        # print(self.context['request'].status)

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if len(Advertisement.objects.filter(status='OPEN', creator=self.context['request'].user)) > 9:
            raise ValidationError('У вас не может быть больше 10 открытых объявлений')
        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    favorite = AdvertisementSerializer(read_only=True,)
    
    class Meta:
        model = Favorite
        fields = ('user', 'favorite', )

    def create(self, validated_data):
        return super().create(validated_data)
    
    # def delete(self, validated_data):
    #     return super().delete(validated_data)

    def validate(self, data):
        print(data)
        if Favorite.objects.filter(user=data['user'], favorite=data['favorite']):
            raise ValidationError('The Advertisement already is favorite')
        if data['favorite'].creator == data['user']:
            raise ValidationError("It's there is owner's advertisement")
        # if Advertisement.objects.get(id=data['favorite'].id).creator == data['user']:
        #     raise ValidationError("It's there is owner's advertisement")
        return data
        
        