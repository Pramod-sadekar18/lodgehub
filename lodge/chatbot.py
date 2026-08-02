import re
from django.db.models import Q, Min, Max
from .models import Property, Amenity, Feature

class DatabaseChatbotEngine:
    """
    100% Dynamic Unscripted Query Engine for LodgeHub properties.
    Dynamically analyzes user natural language queries and translates them
    into Django ORM queries across all database fields without hardcoded scripts or fixed lists.
    """

    STOP_WORDS = {
        "show", "me", "give", "find", "get", "search", "list", "display", "tell",
        "about", "the", "a", "an", "is", "are", "were", "was", "be", "being",
        "in", "at", "from", "near", "around", "by", "to", "for", "with", "and", "or",
        "all", "some", "any", "please", "can", "you", "i", "want", "need", "stay", "stays"
    }

    @classmethod
    def process_query(cls, message: str) -> dict:
        raw_msg = (message or "").strip()
        msg = raw_msg.lower()

        if not msg:
            return {
                "reply": "Hello! I am your AI Database Assistant. Ask me anything about lodges or stays!",
                "properties": [],
                "suggestions": []
            }

        # Base queryset with prefetched relationships
        qs = Property.objects.all().prefetch_related('images', 'amenities', 'features')
        filters_applied = []

        # Tokenize message
        words = re.findall(r'\b[a-zA-Z0-9_\-\.\₹]+\b', msg)

        # -------------------------------------------------------------
        # 1. DYNAMIC PRICE PARSING (No hardcoded limits)
        # -------------------------------------------------------------
        # Range check: "between X and Y", "X to Y", "X - Y"
        range_match = re.search(r'(?:between|from)?\s*₹?\s*(\d{3,6})\s*(?:to|and|-)\s*₹?\s*(\d{3,6})', msg)
        if range_match:
            val1 = float(range_match.group(1))
            val2 = float(range_match.group(2))
            min_p, max_p = min(val1, val2), max(val1, val2)
            qs = qs.filter(price_per_night__gte=min_p, price_per_night__lte=max_p)
            filters_applied.append(f"Price: ₹{int(min_p):,} – ₹{int(max_p):,}")
        else:
            # Below / Under / Max
            below_match = re.search(r'(?:below|under|less than|max|within|<=?|<|cheap|cheaper than)\s*₹?\s*(\d{3,6})', msg)
            if not below_match:
                # e.g. "3000 rupees", "3000 rs", "₹3000"
                below_match = re.search(r'(?:₹\s*(\d{3,6})|(\d{3,6})\s*(?:rupees|rupee|rs|inr))', msg)

            if below_match:
                val_str = below_match.group(1) or below_match.group(2)
                if val_str:
                    val = float(val_str)
                    qs = qs.filter(price_per_night__lte=val)
                    filters_applied.append(f"Price ≤ ₹{int(val):,}")

            # Above / Greater
            above_match = re.search(r'(?:above|more than|greater than|>|>=)\s*₹?\s*(\d{3,6})', msg)
            if above_match:
                val = float(above_match.group(1))
                qs = qs.filter(price_per_night__gte=val)
                filters_applied.append(f"Price ≥ ₹{int(val):,}")

        # -------------------------------------------------------------
        # 2. DYNAMIC SORTING / SUPERLATIVES (No hardcoded scripts)
        # -------------------------------------------------------------
        # Low price sorting
        if any(w in msg for w in ["lowest", "cheapest", "least price", "minimum price", "affordable"]):
            qs = qs.order_by('price_per_night')
            filters_applied.append("Sorted by Lowest Price")
        # High price sorting
        elif any(w in msg for w in ["highest", "expensive", "costliest", "maximum price"]):
            qs = qs.order_by('-price_per_night')
            filters_applied.append("Sorted by Highest Price")
        # Low rating sorting
        elif any(w in msg for w in ["low rated", "lowest rated", "lowest rating", "poor rating", "bad rating"]):
            qs = qs.order_by('rating')
            filters_applied.append("Sorted by Lowest Rating")
        # High rating sorting
        elif any(w in msg for w in ["top rated", "highest rated", "best rated", "5 star", "popular", "best"]):
            qs = qs.order_by('-rating')
            filters_applied.append("Sorted by Highest Rating")

        # -------------------------------------------------------------
        # 3. DYNAMIC SEARCH ACROSS ALL DB TEXT FIELDS
        # -------------------------------------------------------------
        # Filter out numbers and stop words from search tokens
        search_tokens = [w for w in words if not w.isdigit() and w not in cls.STOP_WORDS and len(w) > 1]

        # Combine remaining search tokens into dynamic Q filters
        for token in search_tokens:
            token_q = (
                Q(city__icontains=token) |
                Q(location__icontains=token) |
                Q(name__icontains=token) |
                Q(property_type__icontains=token) |
                Q(category__icontains=token) |
                Q(address__icontains=token) |
                Q(description__icontains=token) |
                Q(badge__icontains=token) |
                Q(amenities__name__icontains=token) |
                Q(features__name__icontains=token)
            )
            
            # Check if this token yields results on DB
            sub_qs = qs.filter(token_q)
            if sub_qs.exists():
                qs = sub_qs
                filters_applied.append(token.capitalize())

        # Execute distinct query
        qs = qs.distinct()
        total_found = qs.count()

        # Build property cards response
        results = []
        for p in qs[:10]:
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

        # Dynamic reply generation
        if total_found > 0:
            if filters_applied:
                reply_text = f"I found **{total_found} property(ies)** matching **{', '.join(filters_applied)}** directly from the database:"
            else:
                reply_text = f"I found **{total_found} property(ies)** available in our database:"
        else:
            reply_text = f"No database records matched your query **\"{raw_msg}\"**. Try asking with different keywords or price ranges!"

        return {
            "reply": reply_text,
            "total": total_found,
            "properties": results,
            "suggestions": []
        }
