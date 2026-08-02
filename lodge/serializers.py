from rest_framework import serializers
from .models import Property, Amenity, PropertyImage , Feature , Room , RoomImage


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'image_type']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']


class RoomImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = RoomImage
        fields = [
            'id',
            'image'
        ]

    def get_image(self, obj):

        request = self.context.get('request')

        if obj.image:
            return request.build_absolute_uri(
                obj.image.url
            )

        return None


class RoomSerializer(serializers.ModelSerializer):

    images = RoomImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Room
        fields = [
            'id',
            'room_name',
            'description',
            'price_per_night',
            'capacity',
            'total_rooms',
            'images'
        ]
class PropertySerializer(serializers.ModelSerializer):

    amenities = AmenitySerializer(many=True, read_only=True)

    images = PropertyImageSerializer(many=True, read_only=True)

    features = FeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Feature.objects.all(),
        write_only=True,
        source='features'
    )

    rooms = RoomSerializer( many=True,read_only=True)

    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all(),
        write_only=True,
        source='amenities'
    )

    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'owner',
            'name',
            'slug',
            'city',
            'location',
            'description',
            'address',
            'latitude',
            'longitude',
            'property_type',
            'category',
            'price_per_night',
            'rating',
            'reviews_count',
            'badge',
            'check_in_time',
            'check_out_time',
            'amenities',
            'amenity_ids',
            'images', 
            'feature_ids' ,
            'features',
            'rooms', # 🔥 multiple images
            'is_verified',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        amenities = validated_data.pop('amenities', [])

        property_obj = Property.objects.create(**validated_data)

        property_obj.amenities.set(amenities)
        return property_obj






class PropertyImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = [
            'id',
            'image',
            'image_type'
        ]

    def get_image(self, obj):
        request = self.context.get('request')

        if obj.image:
            return request.build_absolute_uri(obj.image.url)

        return None

class RoomImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = RoomImage
        fields = [
            'id',
            'image'
        ]

    def get_image(self, obj):
        request = self.context.get('request')

        if obj.image:
            return request.build_absolute_uri(obj.image.url)

        return None

class RoomSerializer(serializers.ModelSerializer):

    images = RoomImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Room
        fields = [
            'id',
            'room_name',
            'description',
            'price_per_night',
            'capacity',
            'total_rooms',
            'images'
        ]

class PropertyDetailSerializer(serializers.ModelSerializer):

    owner = serializers.CharField(
        source='owner.username',
        read_only=True
    )

    amenities = AmenitySerializer(
        many=True,
        read_only=True
    )

    features = FeatureSerializer(
        many=True,
        read_only=True
    )

    images = PropertyImageSerializer(
        many=True,
        read_only=True
    )

    rooms = RoomSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Property

        fields = [
            # property
            'id',
            'owner',

            'name',
            'slug',
            'city',
            'location',
            'address',
            'description',

            'property_type',
            'category',

            'price_per_night',
            'rating',
            'reviews_count',

            'badge',
            'is_verified',

            'latitude',
            'longitude',

            'check_in_time',
            'check_out_time',

            'created_at',
            'updated_at',

            # relations
            'amenities',
            'features',
            'images',
            'rooms'
        ]




