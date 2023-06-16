
from django_filters import rest_framework as filters, DateFromToRangeFilter
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    created_at = DateFromToRangeFilter()
        
    status = filters.CharFilter(field_name='status',
                                lookup_expr='iexact')
    
    class Meta:
        model = Advertisement
        fields = ['status','created_at', 'creator', 'id', ]
        

