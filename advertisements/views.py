from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter

from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrIsStaffOrReadOnly
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer

from rest_framework.decorators import action

    
class AdvertisementViewSet(ModelViewSet):
  
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsStaffOrReadOnly()]
        return []


    def get_queryset(self, *args, **kwargs):
    #     # if self.context['request'].user is IsAuthenticated():
    #     #     return Advertisement.objects.filter(status)=='DRAFT' and self.creator != self.context['request'].user
    #     # if Advertisement.objects.filter(status)=='DRAFT' and self.creator != self.context['request'].user:
    #     #     return IsNotOwner
    #     # if self.context['request'].user == self.creator:
    #     #     return Advertisement.objects.filter(status)=='DRAFT'
            # return Advertisement.objects.all()
        
        if IsAuthenticated():
            print(1)
            user = self.request.user
            return Advertisement.objects.filter(creator=user)
        # if not IsAuthenticated(): # Почему не срабатывает это условие?
        else: # Почему не срабатывает это условие?
            print(2)
            return Advertisement.objects.filter(status='OPEN') or Advertisement.objects.filter(status='CLOSED')
            # return Advertisement.objects.filter(status=='OPEN') or Advertisement.objects.filter(status)=='CLOSED'
    
        # return Advertisement.objects.all()
        
    
    
    # def get_queryset(self, *args, **kwargs):
    #     return Advertisement.objects.all()

    @action(detail=False)
    def favorites(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = FavoriteAdvertisementSerializer(queryset, many=True)
        return Response({request.user.username: serializer.data})
    
    @action(methods=['post'], detail=True)
    def add_favorite(self, request, pk=None):
        print(pk)
        queryset = Advertisement.objects.filter(id=pk).first()
        if queryset:
            validated_data = {'favorite': queryset, 'user': request.user}
            serializer = FavoriteAdvertisementSerializer(data=validated_data)
            serializer.validate(data=validated_data)
            serializer.create(validated_data)
            return Response('The Advertisement added to Favorites', status=status.HTTP_201_CREATED)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=True)
    def delete_favorite(self, request, pk=None):
        queryset = Favorite.objects.filter(favorite=pk, user=request.user)
        if queryset:
            Favorite.delete(Favorite.objects.get(favorite=pk, user=request.user))
            return Response('The Advertisement deleted from Favorites', status=status.HTTP_204_NO_CONTENT)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)

