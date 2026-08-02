import re
from django.db.models import Q
from .models import Property, Amenity

class DatabaseChatbotEngine:
    """
    NLP & Database Query Engine for LodgeHub properties.
    Processes user natural language queries and returns matching lodges from database.
    """

    @classmethod
    def process_query(cls, message: str) -> dict:
        msg = (message or "").strip().lower()
        if not msg:
            return {
                "reply": "Hello! I am your LodgeHub Assistant. How can I help you find a stay today?",
                "properties": [],
                "suggestions": ["Lodges in Pune", "Under ₹3,000", "Luxury Resorts", "Top Rated Stays"]
            }

        # Handle greetings & general help
        if msg in ["hi", "hello", "hey", "hii", "hiii", "help", "who are you"]:
            return {
                "reply": "Hello! 👋 I can help you search properties directly from our database! Try asking me:\n\n• *'Show me price below 3000 rupees'*\n• *'Show lodges near Pune or in Pune'*\n• *'Luxury resorts with swimming pool'*\n• *'Budget hotels under 2000'*",
                "properties": [],
                "suggestions": ["Lodges under 3000 in Pune", "Hotels in Pune", "Luxury stays", "Under ₹2000"]
            }

        qs = Property.objects.all().prefetch_related('images', 'amenities')

        filters_applied = []
        city_found = None
        max_price_found = None
        min_price_found = None

        # 1. City / Location Extraction
        # Get unique cities from DB or fallback defaults
        existing_cities = list(Property.objects.values_list('city', flat=True).distinct())
        known_cities = set([c.lower() for c in existing_cities if c] + ["pune", "mumbai", "lonavala", "nashik", "alibaug", "goa", "delhi", "bangalore"])

        for city in known_cities:
            # Matches "in pune", "near pune", "pune lodges", or just "pune"
            pattern = r'\b' + re.escape(city) + r'\b'
            if re.search(pattern, msg):
                city_found = city
                qs = qs.filter(Q(city__icontains=city) | Q(location__icontains=city))
                filters_applied.append(f"in/near {city.capitalize()}")
                break

        # 2. Price Extraction
        # Range matching: "between 1000 and 3000", "1000 to 3000", "1000-3000"
        range_match = re.search(r'(?:between|from)?\s*₹?\s*(\d+)\s*(?:to|and|-)\s*₹?\s*(\d+)', msg)
        if range_match:
            p1 = float(range_match.group(1))
            p2 = float(range_match.group(2))
            min_price_found, max_price_found = min(p1, p2), max(p1, p2)
            qs = qs.filter(price_per_night__gte=min_price_found, price_per_night__lte=max_price_found)
            filters_applied.append(f"price between ₹{int(min_price_found):,} and ₹{int(max_price_found):,}")
        else:
            # Below / Under / Max matching: "below 3000", "under 3000", "less than 3000", "< 3000", "max 3000", "3000 rupees", "3000 rs", "below 3000 rupees"
            below_match = re.search(r'(?:below|under|less than|max|within|<=?|<|cheap|cheaper than|price)\s*₹?\s*(\d+)\s*(?:rupees|rupee|rs|INR)?', msg)
            if not below_match:
                # Also try number before 'rupees' or 'rs' e.g. "3000 rupees"
                below_match = re.search(r'₹?\s*(\d+)\s*(?:rupees|rupee|rs|INR|per night)', msg)

            if below_match:
                price_val = float(below_match.group(1))
                if price_val > 100: # filter out arbitrary small numbers
                    max_price_found = price_val
                    qs = qs.filter(price_per_night__lte=max_price_found)
                    filters_applied.append(f"price under ₹{int(max_price_found):,}")

            # Above / Greater matching: "above 5000", "more than 5000", "> 5000"
            above_match = re.search(r'(?:above|more than|greater than|>|>=)\s*₹?\s*(\d+)', msg)
            if above_match:
                price_val = float(above_match.group(1))
                min_price_found = price_val
                qs = qs.filter(price_per_night__gte=min_price_found)
                filters_applied.append(f"price above ₹{int(min_price_found):,}")

        # 3. Property Type Filter
        types_map = {
            'lodge': 'lodge',
            'lodges': 'lodge',
            'hotel': 'hotel',
            'hotels': 'hotel',
            'resort': 'resort',
            'resorts': 'resort',
            'hostel': 'hostel',
            'hostels': 'hostel'
        }
        for word, p_type in types_map.items():
            if re.search(r'\b' + word + r'\b', msg):
                qs = qs.filter(property_type__iexact=p_type)
                filters_applied.append(f"type: {p_type.capitalize()}")
                break

        # 4. Category Filter
        categories_map = {
            'luxury': 'luxury',
            'budget': 'budget',
            'cheap': 'budget',
            'family': 'family',
            'business': 'business',
            'pet friendly': 'pet-friendly',
            'pet-friendly': 'pet-friendly',
            'beachfront': 'beachfront',
            'beach': 'beachfront',
            'hillside': 'hillside',
            'hill': 'hillside'
        }
        for kw, cat in categories_map.items():
            if kw in msg:
                qs = qs.filter(category__iexact=cat)
                filters_applied.append(f"category: {cat.capitalize()}")
                break

        # 5. Rating Filter
        if any(term in msg for term in ["top rated", "best", "popular", "5 star", "highly rated", "top"]):
            qs = qs.filter(rating__gte=4.0).order_by('-rating')
            filters_applied.append("top rated (4.0+ ★)")

        # 6. Amenity Filter
        amenity_keywords = {
            'wifi': 'WiFi',
            'pool': 'Pool',
            'swimming': 'Pool',
            'ac': 'AC',
            'air condition': 'AC',
            'parking': 'Parking',
            'restaurant': 'Restaurant',
            'food': 'Restaurant',
            'gym': 'Gym'
        }
        for kw, amenity_name in amenity_keywords.items():
            if kw in msg:
                qs = qs.filter(amenities__name__icontains=amenity_name)
                filters_applied.append(f"with {amenity_name}")
                break

        # 7. Name search fallback if no properties matched yet or explicit property query
        name_query = None
        if not filters_applied:
            # Check if matching property name directly
            matching_by_name = Property.objects.filter(name__icontains=msg)
            if matching_by_name.exists():
                qs = matching_by_name
                filters_applied.append(f"matching '{msg}'")

        # Distinct results & ordering
        qs = qs.distinct()
        total_found = qs.count()

        # Build response list
        results = []
        for p in qs[:8]: # Limit to top 8 for chat UI
            image_url = None
            first_img = p.images.first()
            if first_img and first_img.image:
                image_url = first_img.image.url

            results.append({
                "id": p.id,
                "name": p.name,
                "city": p.city,
                "location": p.location,
                "property_type": p.get_property_type_display(),
                "category": p.get_category_display(),
                "price_per_night": float(p.price_per_night),
                "rating": float(p.rating),
                "reviews_count": p.reviews_count,
                "badge": p.badge or p.get_category_display(),
                "image": image_url,
                "detail_url": f"/property/{p.id}/"
            })

        # Formulate intelligent natural language reply
        if total_found > 0:
            desc = " matching ".join(filters_applied) if filters_applied else "available"
            if city_found and max_price_found:
                reply_text = f"I found **{total_found} property(ies)** in **{city_found.capitalize()}** priced under **₹{int(max_price_found):,}** per night:"
            elif city_found:
                reply_text = f"I found **{total_found} property(ies)** in/near **{city_found.capitalize()}**:"
            elif max_price_found:
                reply_text = f"I found **{total_found} property(ies)** with price below **₹{int(max_price_found):,}** per night:"
            elif filters_applied:
                reply_text = f"Found **{total_found} stay(s)** ({', '.join(filters_applied)}):"
            else:
                reply_text = f"Here are **{total_found} properties** currently available in our database:"
        else:
            filters_str = ", ".join(filters_applied) if filters_applied else msg
            reply_text = f"I couldn't find any stays matching **{filters_str}** in our database. Try expanding your search or checking another price range!"

        # Generate contextual suggestions
        suggestions = []
        if not city_found:
            suggestions.append("Lodges in Pune")
        if not max_price_found:
            suggestions.append("Under ₹3,000")
        if "luxury" not in msg:
            suggestions.append("Luxury Resorts")
        suggestions.append("Top rated stays")

        return {
            "reply": reply_text,
            "total": total_found,
            "properties": results,
            "suggestions": suggestions[:4]
        }
