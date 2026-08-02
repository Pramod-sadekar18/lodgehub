from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Property


class PropertySlugUrlTests(TestCase):
    def test_property_slugged_detail_url_returns_page(self):
        User = get_user_model()
        owner = User.objects.create_user(username='owner', password='testpass123')
        property_obj = Property.objects.create(
            owner=owner,
            name='Sunrise Resort',
            city='Pokhara',
            location='Lake Side',
            property_type='resort',
            category='luxury',
            price_per_night='1200.00',
            rating='4.8',
            reviews_count=10,
            address='Some address'
        )

        response = self.client.get(reverse('property_detail', kwargs={'id': property_obj.id, 'slug': property_obj.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Photo Gallery')
