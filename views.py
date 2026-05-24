from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum

# Mock Product Database
PRODUCTS = [
    {
        'id': 1,
        'name': 'Midnight Velvet Blazer',
        'brand': 'Vantura Premium',
        'price': 850.00,
        'image': '/static/Cloths/Mens%20wear/Black%20Jacket.jpeg',
        'category': 'men',
        'section': 'jackets',
        'rating': 4.8,
        'desc': 'Expertly crafted from high-quality velvet, this blazer offers a sophisticated silhouette and timeless elegance.'
    },
    {
        'id': 2,
        'name': 'Azure Silk Evening Gown',
        'brand': 'L\'Aura Couture',
        'price': 1200.00,
        'image': '/static/Cloths/Womens war/design dress.jpg',
        'category': 'women',
        'section': 'dresses',
        'rating': 5.0,
        'desc': 'A stunning azure blue silk evening gown, featuring a flowing silhouette and delicate silk fabric for the ultimate luxury feel.'
    },
    {
        'id': 3,
        'name': 'Emerald Wool Overcoat',
        'brand': 'Heritage & Co.',
        'price': 650.00,
        'image': '/static/Cloths/Winter collection/cream woolcoat.jpg',
        'category': 'winter-collection',
        'section': 'wool-coats',
        'rating': 4.7,
        'desc': 'Stay warm in style with this premium emerald green wool overcoat. Classic design meets modern warmth.'
    },
    {
        'id': 4,
        'name': 'Ivory Cashmere Sweater',
        'brand': 'SoftTouch Luxury',
        'price': 320.00,
        'image': '/static/Cloths/Womens war/black top.jpg',
        'category': 'women',
        'section': 'tops',
        'rating': 4.9,
        'desc': 'The softest cashmere you will ever feel. This ivory sweater top is a staple for any luxury wardrobe.'
    },
    {
        'id': 5,
        'name': 'Onyx Leather Biker Jacket',
        'brand': 'Rebel Spirit',
        'price': 950.00,
        'image': '/static/Cloths/Mens%20wear/Leather%20Jackets.jpg',
        'category': 'men',
        'section': 'jackets',
        'rating': 4.5,
        'desc': 'Edgy yet sophisticated, this onyx black leather biker jacket is crafted from top-grain leather for a premium fit.'
    },
    {
        'id': 6,
        'name': 'Saffron Linen Shirt',
        'brand': 'Breezy Summer',
        'price': 180.00,
        'image': 'https://images.unsplash.com/photo-1520975911519-40036dae2a6f?auto=format&fit=crop&w=1200&q=80',
        'category': 'summer-collection',
        'section': 'linen-shirts',
        'rating': 4.6,
        'desc': 'Breathable linen in a vibrant saffron yellow. The perfect choice for a high-end summer look.'
    },
    {
        'id': 7,
        'name': 'Petite Floral Dress',
        'brand': 'Bloom Atelier',
        'price': 420.00,
        'image': '/static/Cloths/Womens war/blue frock.jpg',
        'category': 'women',
        'section': 'dresses',
        'rating': 4.9,
        'desc': 'A romantic floral dress with a graceful silhouette and premium fabric, perfect for evening events.'
    },
    {
        'id': 8,
        'name': 'Mini Explorer Jacket',
        'brand': 'Little Luxe',
        'price': 210.00,
        'image': '/static/Cloths/Kids wear/boy playware.jpg',
        'category': 'kids',
        'section': 'boys',
        'rating': 4.7,
        'desc': 'A playful and sturdy jacket made for kids who want comfort and style for every adventure.'
    },
    {
        'id': 9,
        'name': 'Charcoal Slim Suit',
        'brand': 'Executive Tailor',
        'price': 980.00,
        'image': '/static/Cloths/Formal Wear/black suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.8,
        'desc': 'A slim-fit charcoal suit crafted with tailoring precision for a refined professional profile.'
    },
    {
        'id': 10,
        'name': 'Crisp White Dress Shirt',
        'brand': 'Urban Elegance',
        'price': 120.00,
        'image': '/static/Cloths/Mens%20wear/Black%20shirt.jpg',
        'category': 'men',
        'section': 'shirts',
        'rating': 4.6,
        'desc': 'A classic white dress shirt with a slim fit, perfect for smart office and evening wear.'
    },
    {
        'id': 11,
        'name': 'Tailored Chino Pants',
        'brand': 'Monarch Attire',
        'price': 140.00,
        'image': '/static/Cloths/Mens%20wear/brown%20pant.jpg',
        'category': 'men',
        'section': 'pants',
        'rating': 4.4,
        'desc': 'Smart tailored chinos with a modern cut, designed for daily wear and refined comfort.'
    },
    {
        'id': 31,
        'name': 'Charcoal Denim Shirt',
        'brand': 'Urban Signature',
        'price': 110.00,
        'image': '/static/Cloths/Mens%20wear/blue%20shirt.jpg',
        'category': 'men',
        'section': 'shirts',
        'rating': 4.5,
        'desc': 'A refined denim shirt with a modern fit, ideal for both casual and evening wear.'
    },
    {
        'id': 32,
        'name': 'Designer Button-Up Shirt',
        'brand': 'Crafted Luxe',
        'price': 125.00,
        'image': '/static/Cloths/Mens%20wear/Designer%20shirt.jpg',
        'category': 'men',
        'section': 'shirts',
        'rating': 4.6,
        'desc': 'A designer shirt featuring premium cotton and elegant tailoring for elevated daywear.'
    },
    {
        'id': 33,
        'name': 'Relaxed Fit Cargo Pants',
        'brand': 'Trailbound',
        'price': 150.00,
        'image': '/static/Cloths/Mens%20wear/green%20cargo.jpg',
        'category': 'men',
        'section': 'pants',
        'rating': 4.4,
        'desc': 'Utility cargo pants with a relaxed fit and multiple pockets for a polished streetwear look.'
    },
    {
        'id': 34,
        'name': 'Cream Relaxed Pants',
        'brand': 'Softline',
        'price': 128.00,
        'image': '/static/Cloths/Mens%20wear/creame%20pant.jpg',
        'category': 'men',
        'section': 'pants',
        'rating': 4.5,
        'desc': 'Comfortable cream trousers with a subtle texture, perfect for smart-casual style.'
    },
    {
        'id': 35,
        'name': 'Loose Lace-Up T-Shirt',
        'brand': 'Streetwave',
        'price': 95.00,
        'image': '/static/Cloths/Mens%20wear/Loose%20Lace%20Up%20Tshirt.jpg',
        'category': 'men',
        'section': 'shirts',
        'rating': 4.7,
        'desc': 'A loose-fit lace-up tee that blends rugged attitude with comfortable everyday wear.'
    },
    {
        'id': 12,
        'name': 'Silk Camisole Top',
        'brand': 'Luna Luxe',
        'price': 220.00,
        'image': '/static/Cloths/Womens war/blue top.jpg',
        'category': 'women',
        'section': 'tops',
        'rating': 4.5,
        'desc': 'A luxurious silk camisole top designed with delicate straps and a flattering drape.'
    },
    {
        'id': 13,
        'name': 'Midi Satin Skirt',
        'brand': 'Femme & Co.',
        'price': 260.00,
        'image': '/static/Cloths/Womens war/black skirt.jpg',
        'category': 'women',
        'section': 'skirts',
        'rating': 4.7,
        'desc': 'A flowing midi skirt in satin finish for elegant day-to-night styling.'
    },
    {
        'id': 14,
        'name': 'Rainbow Playwear Hoodie',
        'brand': 'Happy Threads',
        'price': 85.00,
        'image': '/static/Cloths/Kids wear/disney playwear.jpg',
        'category': 'kids',
        'section': 'playwear',
        'rating': 4.8,
        'desc': 'A fun and cozy hoodie designed for kids to move comfortably and look great.'
    },
    {
        'id': 15,
        'name': 'Alpine Puffer Coat',
        'brand': 'North Peak',
        'price': 480.00,
        'image': '/static/Cloths/Winter collection/black hooded jacket.jpg',
        'category': 'winter-collection',
        'section': 'puffer-jackets',
        'rating': 4.8,
        'desc': 'Warm and lightweight, this alpine puffer coat is built for cold winter days with premium insulation.'
    },
    {
        'id': 16,
        'name': 'Knit Cable Sweater',
        'brand': 'Wool & Willow',
        'price': 310.00,
        'image': '/static/Cloths/Winter collection/blue knitwear.jpg',
        'category': 'winter-collection',
        'section': 'knitwear',
        'rating': 4.7,
        'desc': 'A cozy cable knit sweater made from premium yarn for a timeless winter wardrobe staple.'
    },
    {
        'id': 17,
        'name': 'Sunset Lounge Shorts',
        'brand': 'Coastline Apparel',
        'price': 95.00,
        'image': '/static/Cloths/Summer collection/cream shorts.jpg',
        'category': 'summer-collection',
        'section': 'shorts',
        'rating': 4.5,
        'desc': 'Lightweight lounge shorts perfect for warm weather relaxation and casual summer days.'
    },
    {
        'id': 18,
        'name': 'Pearl Strap Sandals',
        'brand': 'Sole Couture',
        'price': 165.00,
        'image': '/static/Cloths/Summer collection/strap sandle.jpg',
        'category': 'summer-collection',
        'section': 'sandals',
        'rating': 4.6,
        'desc': 'Chic pearl strap sandals that add a stylish finish to any summer outfit.'
    },
    {
        'id': 66,
        'name': 'Tropical Slide Sandals',
        'brand': 'Beach Breeze',
        'price': 75.00,
        'image': '/static/Cloths/Summer collection/decor sandles.jpg',
        'category': 'summer-collection',
        'section': 'sandals',
        'rating': 4.5,
        'desc': 'Comfortable slide sandals with a tropical print, perfect for sunny days by the pool.'
    },
    {
        'id': 67,
        'name': 'Leather Beach Sandals',
        'brand': 'Sunny Soles',
        'price': 135.00,
        'image': '/static/Cloths/Summer collection/leather sandles.jpg',
        'category': 'summer-collection',
        'section': 'sandals',
        'rating': 4.7,
        'desc': 'Premium leather sandals with a luxe summer finish for beachside style.'
    },
    {
        'id': 68,
        'name': 'Cream Slide Sandals',
        'brand': 'Shoreline Luxe',
        'price': 135.00,
        'image': '/static/Cloths/Summer collection/creame sandles.jpg',
        'category': 'summer-collection',
        'section': 'sandals',
        'rating': 4.8,
        'desc': 'Soft cream sandals with elegant straps that complement any warm-weather outfit.'
    },
    {
        'id': 69,
        'name': 'Black Summer Sandals',
        'brand': 'Night Shore',
        'price': 125.00,
        'image': '/static/Cloths/Summer collection/black sandle.jpg',
        'category': 'summer-collection',
        'section': 'sandals',
        'rating': 4.6,
        'desc': 'Versatile black sandals with a sleek design for summer evenings and beach looks.'
    },
    {
        'id': 70,
        'name': 'Men\'s Summer Sandals',
        'brand': 'Coastal Comfort',
        'price': 95.00,
        'image': '/static/Cloths/Summer collection/mens sandle.jpg',
        'category': 'summer-collection',
        'section': 'sandals',
        'rating': 4.4,
        'desc': 'Easygoing men\'s sandals designed for relaxed summer days and vacation wear.'
    },
    {
        'id': 19,
        'name': 'Urban Graphic Tee',
        'brand': 'Street Pulse',
        'price': 65.00,
        'image': '/static/Cloths/Streetwear/graphic street wear.png',
        'category': 'streetwear',
        'section': 'graphic-tees',
        'rating': 4.3,
        'desc': 'A bold graphic tee designed to be the centerpiece of any streetwear outfit.'
    },
    {
        'id': 29,
        'name': 'Sport Mesh Sneakers',
        'brand': 'Stride Urban',
        'price': 130.00,
        'image': '/static/Cloths/Streetwear/casual sneakers.jpg',
        'category': 'streetwear',
        'section': 'sneakers',
        'rating': 4.6,
        'desc': 'Lightweight mesh sneakers designed for street comfort and athletic-inspired style.'
    },
    {
        'id': 30,
        'name': 'Logo Baseball Cap',
        'brand': 'Capsule',
        'price': 45.00,
        'image': '/static/Cloths/Streetwear/white cap.jpg',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.4,
        'desc': 'A premium logo baseball cap made with structured fabric and vibrant embroidery.'
    },
    {
        'id': 71,
        'name': 'Brown Street Hoodie',
        'brand': 'Urban Drift',
        'price': 85.00,
        'image': '/static/Cloths/Streetwear/brown hoodie.jpg',
        'category': 'streetwear',
        'section': 'hoodies',
        'rating': 4.5,
        'desc': 'A cozy brown hoodie with a relaxed fit and street-ready design.'
    },
    {
        'id': 72,
        'name': 'Printed Hoodie',
        'brand': 'Concrete Cool',
        'price': 90.00,
        'image': '/static/Cloths/Streetwear/printed hoodie.jpg',
        'category': 'streetwear',
        'section': 'hoodies',
        'rating': 4.6,
        'desc': 'A printed hoodie with bold graphics and casual comfort.'
    },
    {
        'id': 73,
        'name': 'White Cap',
        'brand': 'City Crown',
        'price': 40.00,
        'image': '/static/Cloths/Streetwear/white cap.jpg',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.4,
        'desc': 'A crisp white cap that pairs perfectly with any streetwear outfit.'
    },
    {
        'id': 74,
        'name': 'Nike Women\'s Sneakers',
        'brand': 'Stride Urban',
        'price': 140.00,
        'image': '/static/Cloths/Streetwear/nike womens sneakers.jpg',
        'category': 'streetwear',
        'section': 'sneakers',
        'rating': 4.7,
        'desc': 'Sleek women\'s sneakers designed for style and comfort.'
    },
    {
        'id': 75,
        'name': 'Black Streetwear Cap',
        'brand': 'Night Cap',
        'price': 42.00,
        'image': '/static/Cloths/Streetwear/black cap.jpg',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.5,
        'desc': 'A lightweight black cap with premium streetwear detailing.'
    },
    {
        'id': 76,
        'name': 'Brown Street Sneakers',
        'brand': 'Urban Motion',
        'price': 135.00,
        'image': '/static/Cloths/Streetwear/brown sneakers.jpg',
        'category': 'streetwear',
        'section': 'sneakers',
        'rating': 4.5,
        'desc': 'Durable brown street sneakers built for everyday wear.'
    },
    {
        'id': 77,
        'name': 'Printed Black Cap',
        'brand': 'Vector Shade',
        'price': 48.00,
        'image': '/static/Cloths/Streetwear/printed black cap.jpg',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.6,
        'desc': 'A printed black cap with a bold logo detail.'
    },
    {
        'id': 78,
        'name': 'Zipped Hoodie',
        'brand': 'Street Pulse',
        'price': 95.00,
        'image': '/static/Cloths/Streetwear/zipped hoodie.jpg',
        'category': 'streetwear',
        'section': 'hoodies',
        'rating': 4.7,
        'desc': 'A zip-up hoodie with modern streetwear styling and a comfortable fit.'
    },
    {
        'id': 79,
        'name': 'Graphic Street Tee',
        'brand': 'City Prints',
        'price': 70.00,
        'image': '/static/Cloths/Streetwear/white grapthic tree.jpg',
        'category': 'streetwear',
        'section': 'graphic-tees',
        'rating': 4.4,
        'desc': 'A white graphic tee with bold street-inspired art.'
    },
    {
        'id': 80,
        'name': 'Black Graphic Trees Tee',
        'brand': 'Urban Canvas',
        'price': 72.00,
        'image': '/static/Cloths/Streetwear/black graphic trees.jpg',
        'category': 'streetwear',
        'section': 'graphic-tees',
        'rating': 4.5,
        'desc': 'A black graphic tee featuring abstract tree artwork for street style.'
    },
    {
        'id': 81,
        'name': 'Girl Baggy Hoodie',
        'brand': 'Free Flow',
        'price': 88.00,
        'image': '/static/Cloths/Streetwear/girl baggy hoodie.jpg',
        'category': 'streetwear',
        'section': 'hoodies',
        'rating': 4.6,
        'desc': 'A relaxed baggy hoodie with soft fabric and oversized style.'
    },
    {
        'id': 82,
        'name': 'Cream Graphic Tee',
        'brand': 'Street Pulse',
        'price': 68.00,
        'image': '/static/Cloths/Streetwear/cream grapthic tree.jpg',
        'category': 'streetwear',
        'section': 'graphic-tees',
        'rating': 4.5,
        'desc': 'A cream graphic tee with bold street-art inspired print.'
    },
    {
        'id': 21,
        'name': 'Oxford Dress Shirt',
        'brand': 'Executive Tailor',
        'price': 130.00,
        'image': '/static/Cloths/Formal Wear/light blue dress shirt.jpg',
        'category': 'formal-wear',
        'section': 'dress-shirts',
        'rating': 4.4,
        'desc': 'A polished Oxford dress shirt that pairs perfectly with tailored suits and blazers.'
    },
    {
        'id': 83,
        'name': 'Brown Formal Suit',
        'brand': 'Executive Tailor',
        'price': 1020.00,
        'image': '/static/Cloths/Formal Wear/brown suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.7,
        'desc': 'A refined brown suit with soft tailoring and a modern dress silhouette.'
    },
    {
        'id': 84,
        'name': 'Checked Night Suit',
        'brand': 'Royal Stitch',
        'price': 1080.00,
        'image': '/static/Cloths/Formal Wear/checked black suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.8,
        'desc': 'A bold checked suit with structured tailoring for a statement formal look.'
    },
    {
        'id': 85,
        'name': 'White Evening Blazer',
        'brand': 'White Label',
        'price': 520.00,
        'image': '/static/Cloths/Formal Wear/white blazer.jpg',
        'category': 'formal-wear',
        'section': 'blazers',
        'rating': 4.6,
        'desc': 'A crisp white blazer tailored for formal events and upscale evenings.'
    },
    {
        'id': 86,
        'name': 'Black Dress Shirt',
        'brand': 'Urban Elegance',
        'price': 115.00,
        'image': '/static/Cloths/Formal Wear/black dress shirt.jpg',
        'category': 'formal-wear',
        'section': 'dress-shirts',
        'rating': 4.5,
        'desc': 'A sleek black dress shirt crafted from premium cotton and precise tailoring.'
    },
    {
        'id': 87,
        'name': 'Classic Silver Watch',
        'brand': 'Timepiece Atelier',
        'price': 620.00,
        'image': '/static/Cloths/Formal Wear/silver watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.8,
        'desc': 'A polished silver watch perfect for formal attire and evening wear.'
    },
    {
        'id': 22,
        'name': 'Tactile Leather Wallet',
        'brand': 'Ascent Goods',
        'price': 95.00,
        'image': '/static/Cloths/Mens%20wear/black%20pendent%20chain.jpg',
        'category': 'men',
        'section': 'accessories',
        'rating': 4.6,
        'desc': 'A premium leather wallet with multiple compartments, crafted for durability and refined style.'
    },
    {
        'id': 23,
        'name': 'Black Signature Ring',
        'brand': 'Rogue Metal',
        'price': 75.00,
        'image': '/static/Cloths/Mens%20wear/designer%20ring.jpg',
        'category': 'men',
        'section': 'accessories',
        'rating': 4.7,
        'desc': 'A bold black ring with polished edges, perfect for adding a strong finishing touch to any outfit.'
    },
    {
        'id': 24,
        'name': 'Chain Link Bracelet',
        'brand': 'Core Jewelry',
        'price': 68.00,
        'image': '/static/Cloths/Mens%20wear/black%20bracelet.jpg',
        'category': 'men',
        'section': 'accessories',
        'rating': 4.6,
        'desc': 'A sturdy chain link bracelet with a matte finish for everyday luxury styling.'
    },
    {
        'id': 25,
        'name': 'Minimal Pendant Chain',
        'brand': 'Luxe Lines',
        'price': 120.00,
        'image': '/static/Cloths/Mens%20wear/chain.jpg',
        'category': 'men',
        'section': 'accessories',
        'rating': 4.8,
        'desc': 'A sleek pendant chain with a versatile design that complements both casual and formal looks.'
    },
    {
        'id': 26,
        'name': 'Girls Floral Set',
        'brand': 'Petite Chic',
        'price': 120.00,
        'image': '/static/Cloths/Kids wear/blue girl frock.jpg',
        'category': 'kids',
        'section': 'girls',
        'rating': 4.7,
        'desc': 'A charming floral outfit set designed for girls with a bright and playful look.'
    },
    {
        'id': 27,
        'name': 'School Plaid Blazer',
        'brand': 'Campus Classics',
        'price': 150.00,
        'image': '/static/Cloths/Kids wear/blue school.jpg',
        'category': 'kids',
        'section': 'school-uniforms',
        'rating': 4.5,
        'desc': 'A smart plaid blazer ideal for school uniforms with a polished and comfortable fit.'
    },
    {
        'id': 28,
        'name': 'Steel Chronograph Watch',
        'brand': 'Timepiece Atelier',
        'price': 680.00,
        'image': '/static/Cloths/Formal Wear/black watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.9,
        'desc': 'A refined steel chronograph watch with premium detailing for an elegant evening look.'
    },
    {
        'id': 29,
        'name': 'Sport Mesh Sneakers',
        'brand': 'Stride Urban',
        'price': 130.00,
        'image': 'https://images.unsplash.com/photo-1519741495787-6444ad4b4e76?auto=format&fit=crop&w=1200&q=80',
        'category': 'streetwear',
        'section': 'sneakers',
        'rating': 4.6,
        'desc': 'Lightweight mesh sneakers designed for street comfort and athletic-inspired style.'
    },
    {
        'id': 30,
        'name': 'Logo Baseball Cap',
        'brand': 'Capsule',
        'price': 45.00,
        'image': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?auto=format&fit=crop&w=1200&q=80&sat=20',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.4,
        'desc': 'A premium logo baseball cap made with structured fabric and vibrant embroidery.'
    },
    {
        'id': 36,
        'name': 'Sunrise Maxi Dress',
        'brand': 'Serene Silhouettes',
        'price': 360.00,
        'image': 'https://images.unsplash.com/photo-1523293838764-6fc28e88c8f2?auto=format&fit=crop&w=1200&q=80',
        'category': 'summer-collection',
        'section': 'maxi-dresses',
        'rating': 4.8,
        'desc': 'A breezy maxi dress with a sunset-inspired print and soft flowing fabric for summer days.'
    },
    {
        'id': 37,
        'name': 'Ebony Lace Frock',
        'brand': 'Noir Atelier',
        'price': 290.00,
        'image': '/static/Cloths/Womens war/black frock.jpg',
        'category': 'women',
        'section': 'frocks',
        'rating': 4.7,
        'desc': 'A delicate lace frock with refined detailing for elegant evening occasions.'
    },
    {
        'id': 38,
        'name': 'Royal Blue Crop Top',
        'brand': 'Couture Mist',
        'price': 145.00,
        'image': '/static/Cloths/Womens war/royal blue top.jpg',
        'category': 'women',
        'section': 'tops',
        'rating': 4.6,
        'desc': 'A vibrant crop top in royal blue, designed for style and effortless layering.'
    },
    {
        'id': 39,
        'name': 'Green Evening Dress',
        'brand': 'Verve & Grace',
        'price': 420.00,
        'image': '/static/Cloths/Womens war/green dress.png',
        'category': 'women',
        'section': 'dresses',
        'rating': 4.8,
        'desc': 'An elegant green evening dress with a sleek silhouette and premium fabric.'
    },
    {
        'id': 40,
        'name': 'Purple Pleated Skirt',
        'brand': 'Silhouette Muse',
        'price': 180.00,
        'image': '/static/Cloths/Womens war/pyrple skirt.png',
        'category': 'women',
        'section': 'skirts',
        'rating': 4.5,
        'desc': 'A playful pleated skirt in purple with a flattering fit for chic daywear.'
    },
    {
        'id': 41,
        'name': 'Designer Frock',
        'brand': 'Luna Muse',
        'price': 310.00,
        'image': '/static/Cloths/Womens war/designer frock.jpg',
        'category': 'women',
        'section': 'frocks',
        'rating': 4.9,
        'desc': 'A statement designer frock crafted from luxurious fabric with refined draping.'
    },
    {
        'id': 42,
        'name': 'Black Evening Dress',
        'brand': 'Noir Atelier',
        'price': 340.00,
        'image': '/static/Cloths/Womens war/black dree.jpeg',
        'category': 'women',
        'section': 'dresses',
        'rating': 4.8,
        'desc': 'A sleek black evening dress with graceful lines and premium detailing.'
    },
    {
        'id': 43,
        'name': 'Designer Kids Shirt',
        'brand': 'Tiny Trends',
        'price': 65.00,
        'image': '/static/Cloths/Kids wear/design shirt.jpg',
        'category': 'kids',
        'section': 'boys',
        'rating': 4.6,
        'desc': 'A stylish designer shirt for boys with modern patterns and comfortable fit.'
    },
    {
        'id': 44,
        'name': 'Blue Kids T-Shirt',
        'brand': 'Playful Prints',
        'price': 45.00,
        'image': '/static/Cloths/Kids wear/blue Tshirt.jpg',
        'category': 'kids',
        'section': 'boys',
        'rating': 4.5,
        'desc': 'A vibrant blue t-shirt perfect for casual play and everyday wear.'
    },
    {
        'id': 45,
        'name': 'Designer White Dress',
        'brand': 'Little Luxe',
        'price': 95.00,
        'image': '/static/Cloths/Kids wear/designer white.jpg',
        'category': 'kids',
        'section': 'girls',
        'rating': 4.7,
        'desc': 'An elegant white designer dress for special occasions and play dates.'
    },
    {
        'id': 46,
        'name': 'White Summer Outfit',
        'brand': 'Sunny Days',
        'price': 55.00,
        'image': '/static/Cloths/Kids wear/white summer cloth.jpg',
        'category': 'kids',
        'section': 'girls',
        'rating': 4.4,
        'desc': 'Light and breezy white summer clothing perfect for warm weather fun.'
    },
    {
        'id': 47,
        'name': 'Short Playwear Set',
        'brand': 'Active Kids',
        'price': 70.00,
        'image': '/static/Cloths/Kids wear/short playwear.jpg',
        'category': 'kids',
        'section': 'playwear',
        'rating': 4.6,
        'desc': 'Comfortable short playwear set designed for active kids and outdoor adventures.'
    },
    {
        'id': 48,
        'name': 'White School Uniform',
        'brand': 'Academy Wear',
        'price': 85.00,
        'image': '/static/Cloths/Kids wear/white school.jpg',
        'category': 'kids',
        'section': 'school-uniforms',
        'rating': 4.5,
        'desc': 'Classic white school uniform with a neat and professional appearance.'
    },
    {
        'id': 49,
        'name': 'Red & White School Set',
        'brand': 'School Pride',
        'price': 90.00,
        'image': '/static/Cloths/Kids wear/white & red school.png',
        'category': 'kids',
        'section': 'school-uniforms',
        'rating': 4.6,
        'desc': 'Stylish red and white school uniform set with comfortable fabric.'
    },
    {
        'id': 50,
        'name': 'Beige Kurta Set',
        'brand': 'Cultural Threads',
        'price': 75.00,
        'image': '/static/Cloths/Kids wear/Beige Kurta.jpg',
        'category': 'kids',
        'section': 'boys',
        'rating': 4.7,
        'desc': 'Traditional beige kurta set perfect for cultural events and celebrations.'
    },
    {
        'id': 51,
        'name': 'Black Winter Boots',
        'brand': 'Frost Gear',
        'price': 180.00,
        'image': '/static/Cloths/Winter collection/black boots.jpg',
        'category': 'winter-collection',
        'section': 'boots',
        'rating': 4.6,
        'desc': 'Sturdy black winter boots designed for extreme cold weather protection.'
    },
    {
        'id': 52,
        'name': 'Women\'s Black Boots',
        'brand': 'Elegant Steps',
        'price': 195.00,
        'image': '/static/Cloths/Winter collection/black women boots.jpg',
        'category': 'winter-collection',
        'section': 'boots',
        'rating': 4.7,
        'desc': 'Stylish black boots for women with waterproof design and comfortable fit.'
    },
    {
        'id': 53,
        'name': 'Blue Winter Boots',
        'brand': 'Arctic Comfort',
        'price': 165.00,
        'image': '/static/Cloths/Winter collection/blue boots.jpg',
        'category': 'winter-collection',
        'section': 'boots',
        'rating': 4.5,
        'desc': 'Vibrant blue winter boots with thermal insulation for cold weather.'
    },
    {
        'id': 54,
        'name': 'Brown Winter Boots',
        'brand': 'Terra Trail',
        'price': 175.00,
        'image': '/static/Cloths/Winter collection/brown boots.jpg',
        'category': 'winter-collection',
        'section': 'boots',
        'rating': 4.6,
        'desc': 'Classic brown winter boots with rugged design for outdoor adventures.'
    },
    {
        'id': 55,
        'name': 'Snow Boots',
        'brand': 'Polar Gear',
        'price': 200.00,
        'image': '/static/Cloths/Winter collection/snow boots.jpg',
        'category': 'winter-collection',
        'section': 'boots',
        'rating': 4.8,
        'desc': 'Heavy-duty snow boots built for deep snow and extreme winter conditions.'
    },
    {
        'id': 56,
        'name': 'White Snow Boots',
        'brand': 'Winter White',
        'price': 185.00,
        'image': '/static/Cloths/Winter collection/white snow boots.jpg',
        'category': 'winter-collection',
        'section': 'boots',
        'rating': 4.7,
        'desc': 'Elegant white snow boots with waterproof membrane and warm lining.'
    },
    {
        'id': 57,
        'name': 'Brown Puffer Jacket',
        'brand': 'Urban Warmth',
        'price': 420.00,
        'image': '/static/Cloths/Winter collection/brown jacket.jpg',
        'category': 'winter-collection',
        'section': 'puffer-jackets',
        'rating': 4.6,
        'desc': 'Classic brown puffer jacket with down filling for maximum warmth.'
    },
    {
        'id': 58,
        'name': 'Cement Puffer Jacket',
        'brand': 'Concrete Cool',
        'price': 395.00,
        'image': '/static/Cloths/Winter collection/cement and black jacket.jpg',
        'category': 'winter-collection',
        'section': 'puffer-jackets',
        'rating': 4.5,
        'desc': 'Modern cement-colored puffer jacket with sleek urban design.'
    },
    {
        'id': 59,
        'name': 'Red Puffer Jacket',
        'brand': 'Bold Winter',
        'price': 410.00,
        'image': '/static/Cloths/Winter collection/red jacket.jpg',
        'category': 'winter-collection',
        'section': 'puffer-jackets',
        'rating': 4.7,
        'desc': 'Vibrant red puffer jacket that stands out in winter landscapes.'
    },
    {
        'id': 60,
        'name': 'Stylish Puffer Jacket',
        'brand': 'Fashion Frost',
        'price': 450.00,
        'image': '/static/Cloths/Winter collection/stylish jacket.jpg',
        'category': 'winter-collection',
        'section': 'puffer-jackets',
        'rating': 4.8,
        'desc': 'Fashion-forward puffer jacket with premium materials and modern cut.'
    },
    {
        'id': 61,
        'name': 'Designer Knitwear',
        'brand': 'Knit Couture',
        'price': 280.00,
        'image': '/static/Cloths/Winter collection/designer knitwear.jpg',
        'category': 'winter-collection',
        'section': 'knitwear',
        'rating': 4.9,
        'desc': 'Designer knitwear piece crafted with luxurious yarns and intricate patterns.'
    },
    {
        'id': 62,
        'name': 'Classic Knitwear',
        'brand': 'Timeless Threads',
        'price': 250.00,
        'image': '/static/Cloths/Winter collection/knitwaer.jpg',
        'category': 'winter-collection',
        'section': 'knitwear',
        'rating': 4.6,
        'desc': 'Classic knitwear sweater with traditional patterns and cozy comfort.'
    },
    {
        'id': 63,
        'name': 'Gray Wool Coat',
        'brand': 'Heritage & Co.',
        'price': 620.00,
        'image': '/static/Cloths/Winter collection/gray woolcoat.jpg',
        'category': 'winter-collection',
        'section': 'wool-coats',
        'rating': 4.7,
        'desc': 'Sophisticated gray wool coat with timeless elegance and superior warmth.'
    },
    {
        'id': 64,
        'name': 'Navy Blue Wool Coat',
        'brand': 'Classic Wardrobe',
        'price': 680.00,
        'image': '/static/Cloths/Winter collection/navy blue woolcoat.jpg',
        'category': 'winter-collection',
        'section': 'wool-coats',
        'rating': 4.8,
        'desc': 'Navy blue wool coat with structured shoulders and premium tailoring.'
    },
    {
        'id': 65,
        'name': 'White Wool Coat',
        'brand': 'Pure Elegance',
        'price': 650.00,
        'image': '/static/Cloths/Winter collection/white coat.jpg',
        'category': 'winter-collection',
        'section': 'wool-coats',
        'rating': 4.9,
        'desc': 'Pure white wool coat that exudes sophistication and winter luxury.'
    },
    {
        'id': 88,
        'name': 'Black Cargo Pants',
        'brand': 'Urban Cargo',
        'price': 155.00,
        'image': '/static/Cloths/Mens%20wear/Black%20cargo.jpg',
        'category': 'men',
        'section': 'pants',
        'rating': 4.6,
        'desc': 'A sharp black cargo pant with durable pockets and refined streetwear appeal.'
    },
    {
        'id': 89,
        'name': 'Silver Toggle Bracelet',
        'brand': 'Modern Link',
        'price': 85.00,
        'image': '/static/Cloths/Mens%20wear/silver%20bracelet%20with%20toggle.jpg',
        'category': 'men',
        'section': 'accessories',
        'rating': 4.7,
        'desc': 'A polished silver bracelet with toggle closure for a refined urban finish.'
    },
    {
        'id': 90,
        'name': 'Casual Button-Up Shirt',
        'brand': 'Daily Tailor',
        'price': 98.00,
        'image': '/static/Cloths/Mens%20wear/Casual%20shirt.jpg',
        'category': 'men',
        'section': 'shirts',
        'rating': 4.5,
        'desc': 'A laid-back casual shirt with a relaxed fit, perfect for everyday summer style.'
    },
    {
        'id': 91,
        'name': 'Indigo Denim Jacket',
        'brand': 'Denim Works',
        'price': 210.00,
        'image': '/static/Cloths/Mens%20wear/Denim%20Jacket.jpg',
        'category': 'men',
        'section': 'jackets',
        'rating': 4.6,
        'desc': 'A versatile denim jacket with a classic indigo wash and rugged tailoring.'
    },
    {
        'id': 92,
        'name': 'Black Band Ring',
        'brand': 'Edge Forge',
        'price': 62.00,
        'image': '/static/Cloths/Mens%20wear/Black%20ring.jpg',
        'category': 'men',
        'section': 'accessories',
        'rating': 4.4,
        'desc': 'A bold black ring with a matte finish for modern and minimalist styling.'
    },
    {
        'id': 93,
        'name': 'Brown Tailored Blazer',
        'brand': 'Regal Threads',
        'price': 510.00,
        'image': '/static/Cloths/Formal Wear/brown blazer.jpg',
        'category': 'formal-wear',
        'section': 'blazers',
        'rating': 4.6,
        'desc': 'A warm brown blazer with elegant tailoring for modern formal occasions.'
    },
    {
        'id': 94,
        'name': 'Brown Leather Watch',
        'brand': 'Heritage Time',
        'price': 540.00,
        'image': '/static/Cloths/Formal Wear/brown watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.7,
        'desc': 'A refined brown leather watch with timeless style and polished detailing.'
    },
    {
        'id': 95,
        'name': 'Chain-Link Watch',
        'brand': 'Precision Time',
        'price': 680.00,
        'image': '/static/Cloths/Formal Wear/chain watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.8,
        'desc': 'A standout chain-link watch with elegant design for evening wear.'
    },
    {
        'id': 96,
        'name': 'Checked Formal Blazer',
        'brand': 'Dapper Edge',
        'price': 575.00,
        'image': '/static/Cloths/Formal Wear/checked blazer.jpg',
        'category': 'formal-wear',
        'section': 'blazers',
        'rating': 4.6,
        'desc': 'A checked blazer with sharp tailoring for sophisticated office and event style.'
    },
    {
        'id': 97,
        'name': 'Curved Collar Dress Shirt',
        'brand': 'Elite Shirts',
        'price': 135.00,
        'image': '/static/Cloths/Formal Wear/curved dress shirt.jpg',
        'category': 'formal-wear',
        'section': 'dress-shirts',
        'rating': 4.5,
        'desc': 'An elegant dress shirt with a curved collar and refined finish.'
    },
    {
        'id': 98,
        'name': 'Design Movement Watch',
        'brand': 'Avant Time',
        'price': 720.00,
        'image': '/static/Cloths/Formal Wear/design watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.8,
        'desc': 'A designer watch with a striking face and premium leather strap.'
    },
    {
        'id': 99,
        'name': 'Gray Tailored Suit',
        'brand': 'Executive Tailor',
        'price': 1080.00,
        'image': '/static/Cloths/Formal Wear/gray suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.7,
        'desc': 'A sharp gray suit with precise tailoring and a timeless silhouette.'
    },
    {
        'id': 100,
        'name': 'Green Dress Shirt',
        'brand': 'Silk & Stitch',
        'price': 125.00,
        'image': '/static/Cloths/Formal Wear/green drress shirt.jpg',
        'category': 'formal-wear',
        'section': 'dress-shirts',
        'rating': 4.5,
        'desc': 'A green dress shirt with a crisp finish and polished formal appeal.'
    },
    {
        'id': 101,
        'name': 'Navy Blue Blazer',
        'brand': 'Navy Court',
        'price': 540.00,
        'image': '/static/Cloths/Formal Wear/navy blue blazer.jpg',
        'category': 'formal-wear',
        'section': 'blazers',
        'rating': 4.6,
        'desc': 'A classic navy blazer with structured shoulders and tailored style.'
    },
    {
        'id': 102,
        'name': 'Navy Blue Suit',
        'brand': 'Ocean Tailor',
        'price': 1120.00,
        'image': '/static/Cloths/Formal Wear/navy blue suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.8,
        'desc': 'A navy blue suit crafted for premium comfort and polished formal dressing.'
    },
    {
        'id': 103,
        'name': 'Pink Formal Blazer',
        'brand': 'Rose & Co.',
        'price': 570.00,
        'image': '/static/Cloths/Formal Wear/pink blazer.jpg',
        'category': 'formal-wear',
        'section': 'blazers',
        'rating': 4.5,
        'desc': 'A feminine pink blazer with refined tailoring for statement formal looks.'
    },
    {
        'id': 104,
        'name': 'Pink Dress Watch',
        'brand': 'Rose Time',
        'price': 590.00,
        'image': '/static/Cloths/Formal Wear/pink watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.7,
        'desc': 'A luxurious pink watch with delicate detailing and a polished finish.'
    },
    {
        'id': 105,
        'name': 'Printed Dress Shirt',
        'brand': 'Patterned Classics',
        'price': 140.00,
        'image': '/static/Cloths/Formal Wear/print dress shirt.jpg',
        'category': 'formal-wear',
        'section': 'dress-shirts',
        'rating': 4.6,
        'desc': 'A printed dress shirt with subtle patterning for a modern formal outfit.'
    },
    {
        'id': 106,
        'name': 'Purple Suit',
        'brand': 'Royal Tailor',
        'price': 1095.00,
        'image': '/static/Cloths/Formal Wear/purple suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.7,
        'desc': 'An elegant purple suit with bold colors and tailored structure.'
    },
    {
        'id': 107,
        'name': 'Red Executive Suit',
        'brand': 'Red Label',
        'price': 1150.00,
        'image': '/static/Cloths/Formal Wear/red suit.jpg',
        'category': 'formal-wear',
        'section': 'suits',
        'rating': 4.8,
        'desc': 'A striking red suit designed to make a polished formal statement.'
    },
    {
        'id': 108,
        'name': 'Women Formal Blazer',
        'brand': 'Feminine Cut',
        'price': 560.00,
        'image': '/static/Cloths/Formal Wear/women blazer.png',
        'category': 'formal-wear',
        'section': 'blazers',
        'rating': 4.5,
        'desc': 'A tailored women’s blazer with a modern fit and refined finish.'
    },
    {
        'id': 109,
        'name': 'Women’s Gold Watch',
        'brand': 'Elle Time',
        'price': 710.00,
        'image': '/static/Cloths/Formal Wear/women watch.jpg',
        'category': 'formal-wear',
        'section': 'watches',
        'rating': 4.9,
        'desc': 'A polished women’s watch with delicate styling and luxurious design.'
    },
    {
        'id': 110,
        'name': 'Black Graphic Tree Tee',
        'brand': 'Ink Street',
        'price': 68.00,
        'image': '/static/Cloths/Streetwear/black graphc tree.jpg',
        'category': 'streetwear',
        'section': 'graphic-tees',
        'rating': 4.4,
        'desc': 'A street-inspired graphic tee with bold imagery and urban attitude.'
    },
    {
        'id': 111,
        'name': 'Brown Street Cap',
        'brand': 'Urban Shade',
        'price': 42.00,
        'image': '/static/Cloths/Streetwear/brown cap.jpg',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.5,
        'desc': 'A soft brown cap with sleek detailing for everyday streetwear looks.'
    },
    {
        'id': 112,
        'name': 'Classic Street Cap',
        'brand': 'Topside',
        'price': 40.00,
        'image': '/static/Cloths/Streetwear/cap.jpg',
        'category': 'streetwear',
        'section': 'caps',
        'rating': 4.3,
        'desc': 'A classic clean cap that completes any casual streetwear outfit.'
    },
    {
        'id': 113,
        'name': 'Cream Street Hoodie',
        'brand': 'Cloud Layer',
        'price': 92.00,
        'image': '/static/Cloths/Streetwear/cream hoodie.jpg',
        'category': 'streetwear',
        'section': 'hoodies',
        'rating': 4.7,
        'desc': 'A cream hoodie with soft fabric and relaxed streetwear styling.'
    },
    {
        'id': 114,
        'name': 'Printed Street Hoodie',
        'brand': 'Artisan Urban',
        'price': 95.00,
        'image': '/static/Cloths/Streetwear/printed hoodies.jpg',
        'category': 'streetwear',
        'section': 'hoodies',
        'rating': 4.6,
        'desc': 'A printed hoodie with bold graphics and a comfortable fit.'
    },
    {
        'id': 115,
        'name': 'White Sport Sneakers',
        'brand': 'Runway Steps',
        'price': 145.00,
        'image': '/static/Cloths/Streetwear/white nike shoes.jpg',
        'category': 'streetwear',
        'section': 'sneakers',
        'rating': 4.6,
        'desc': 'A fresh white sneaker with athletic styling and street-ready comfort.'
    },
    {
        'id': 116,
        'name': 'Women’s White Sneakers',
        'brand': 'Stride Urban',
        'price': 148.00,
        'image': '/static/Cloths/Streetwear/women whitte sneakers.jpg',
        'category': 'streetwear',
        'section': 'sneakers',
        'rating': 4.7,
        'desc': 'A clean white sneaker designed to blend comfort with street style.'
    },
    {
        'id': 117,
        'name': 'Sky Blue Linen Shirt',
        'brand': 'Coastal Linen',
        'price': 110.00,
        'image': '/static/Cloths/Summer collection/blue linen shirts.jpg',
        'category': 'summer-collection',
        'section': 'linen-shirts',
        'rating': 4.6,
        'desc': 'A breezy sky blue linen shirt perfect for warm weather days.'
    },
    {
        'id': 118,
        'name': 'Brown Cargo Shorts',
        'brand': 'Harbor Wear',
        'price': 75.00,
        'image': '/static/Cloths/Summer collection/brown cargo shorts.jpeg',
        'category': 'summer-collection',
        'section': 'shorts',
        'rating': 4.5,
        'desc': 'Practical cargo shorts in brown with comfortable stretch and summer-ready detail.'
    },
    {
        'id': 119,
        'name': 'Denim Summer Shorts',
        'brand': 'Sunset Denim',
        'price': 85.00,
        'image': '/static/Cloths/Summer collection/denim short.jpg',
        'category': 'summer-collection',
        'section': 'shorts',
        'rating': 4.4,
        'desc': 'Casual denim shorts designed for easy summer layering and beach days.'
    },
    {
        'id': 120,
        'name': 'Botanical Maxi Dress',
        'brand': 'Garden Muse',
        'price': 410.00,
        'image': '/static/Cloths/Summer collection/design maxi dress.jpg',
        'category': 'summer-collection',
        'section': 'maxi-dresses',
        'rating': 4.7,
        'desc': 'A floral maxi dress with lightweight fabric for elegant summer evenings.'
    },
    {
        'id': 121,
        'name': 'Designer Print Maxi Dress',
        'brand': 'Feminine Flair',
        'price': 430.00,
        'image': '/static/Cloths/Summer collection/designer maxi dress.jpg',
        'category': 'summer-collection',
        'section': 'maxi-dresses',
        'rating': 4.8,
        'desc': 'A designer maxi dress with distinctive printwork and fluid movement.'
    },
    {
        'id': 122,
        'name': 'Olive Cargo Shorts',
        'brand': 'Summerset',
        'price': 80.00,
        'image': '/static/Cloths/Summer collection/green cargo shorts.jpg',
        'category': 'summer-collection',
        'section': 'shorts',
        'rating': 4.5,
        'desc': 'Relaxed olive cargo shorts built for warm-weather adventures.'
    },
    {
        'id': 123,
        'name': 'Green Linen Shirt',
        'brand': 'Evergreen Linen',
        'price': 115.00,
        'image': '/static/Cloths/Summer collection/green linen.jpg',
        'category': 'summer-collection',
        'section': 'linen-shirts',
        'rating': 4.6,
        'desc': 'A soft green linen shirt that keeps you cool and polished through summer.'
    },
    {
        'id': 124,
        'name': 'Men’s Tropical Maxi Dress',
        'brand': 'Freeform',
        'price': 220.00,
        'image': '/static/Cloths/Summer collection/men maxi dress.jpg',
        'category': 'summer-collection',
        'section': 'maxi-dresses',
        'rating': 4.3,
        'desc': 'A bold tropical maxi dress with a relaxed silhouette for summer style.'
    },
    {
        'id': 125,
        'name': 'Men’s Soft Maxi Dress',
        'brand': 'Urban Flow',
        'price': 225.00,
        'image': '/static/Cloths/Summer collection/mens maxi dress.jpg',
        'category': 'summer-collection',
        'section': 'maxi-dresses',
        'rating': 4.4,
        'desc': 'A lightweight maxi dress with soft texture and easy summer wear.'
    },
    {
        'id': 126,
        'name': 'Pink Linen Shirt',
        'brand': 'Blush Beach',
        'price': 112.00,
        'image': '/static/Cloths/Summer collection/pink linen shirts.png',
        'category': 'summer-collection',
        'section': 'linen-shirts',
        'rating': 4.6,
        'desc': 'A delicate pink linen shirt with a lightweight design for sunny weekends.'
    },
    {
        'id': 127,
        'name': 'Sunset Maxi Dress',
        'brand': 'Summer Aura',
        'price': 395.00,
        'image': '/static/Cloths/Summer collection/summer maxi dress.jpg',
        'category': 'summer-collection',
        'section': 'maxi-dresses',
        'rating': 4.7,
        'desc': 'A flowing maxi dress inspired by sunset hues for warm-weather glamour.'
    },
    {
        'id': 128,
        'name': 'Women Black Shorts',
        'brand': 'Noir Breeze',
        'price': 78.00,
        'image': '/static/Cloths/Summer collection/women black shorts.jpg',
        'category': 'summer-collection',
        'section': 'shorts',
        'rating': 4.5,
        'desc': 'A pair of sleek black shorts styled for summer layering and versatility.'
    },
    {
        'id': 129,
        'name': 'Yellow Linen Shirt',
        'brand': 'Sunshine Linen',
        'price': 118.00,
        'image': '/static/Cloths/Summer collection/yellow linen shirts.png',
        'category': 'summer-collection',
        'section': 'linen-shirts',
        'rating': 4.6,
        'desc': 'A bright yellow linen shirt with effortless comfort for summer days.'
    },
    {
        'id': 130,
        'name': 'Black Lace Frock',
        'brand': 'Noir Atelier',
        'price': 310.00,
        'image': '/static/Cloths/Womens war/Black Frock.jpg',
        'category': 'women',
        'section': 'frocks',
        'rating': 4.7,
        'desc': 'A luxurious black lace frock crafted for refined evening events.'
    },
    {
        'id': 131,
        'name': 'Designer Pleated Skirt',
        'brand': 'Silhouette Muse',
        'price': 170.00,
        'image': '/static/Cloths/Womens war/designer skirt.jpg',
        'category': 'women',
        'section': 'skirts',
        'rating': 4.5,
        'desc': 'A chic pleated skirt with designer detailing for day-to-night style.'
    }
]

CATEGORY_LABELS = {
    'men': 'Men',
    'women': 'Women',
    'kids': 'Kids',
    'winter-collection': 'Winter Collection',
    'summer-collection': 'Summer Collection',
    'streetwear': 'Streetwear',
    'formal-wear': 'Formal Wear'
}

CATEGORY_SECTIONS = {
    'men': [
        {'slug': 'shirts', 'label': 'Shirts'},
        {'slug': 'pants', 'label': 'Pants'},
        {'slug': 'jackets', 'label': 'Jackets'},
        {'slug': 'accessories', 'label': 'Accessories'}
    ],
    'women': [
        {'slug': 'frocks', 'label': 'Frocks'},
        {'slug': 'dresses', 'label': 'Dresses'},
        {'slug': 'tops', 'label': 'Tops'},
        {'slug': 'skirts', 'label': 'Skirts'}
    ],
    'kids': [
        {'slug': 'boys', 'label': 'Boys Wear'},
        {'slug': 'girls', 'label': 'Girls Wear'},
        {'slug': 'school-uniforms', 'label': 'School Uniforms'},
        {'slug': 'playwear', 'label': 'Playwear'}
    ],
    'winter-collection': [
        {'slug': 'puffer-jackets', 'label': 'Puffer Jackets'},
        {'slug': 'knitwear', 'label': 'Knitwear'},
        {'slug': 'wool-coats', 'label': 'Wool Coats'},
        {'slug': 'boots', 'label': 'Winter Boots'}
    ],
    'summer-collection': [
        {'slug': 'linen-shirts', 'label': 'Linen Shirts'},
        {'slug': 'maxi-dresses', 'label': 'Maxi Dresses'},
        {'slug': 'shorts', 'label': 'Shorts'},
        {'slug': 'sandals', 'label': 'Sandals'}
    ],
    'streetwear': [
        {'slug': 'hoodies', 'label': 'Hoodies'},
        {'slug': 'sneakers', 'label': 'Sneakers'},
        {'slug': 'caps', 'label': 'Caps'},
        {'slug': 'graphic-tees', 'label': 'Graphic Tees'}
    ],
    'formal-wear': [
        {'slug': 'suits', 'label': 'Suits'},
        {'slug': 'blazers', 'label': 'Blazers'},
        {'slug': 'dress-shirts', 'label': 'Dress Shirts'},
        {'slug': 'watches', 'label': 'Watches'}
    ]
}

MIN_PRICE = 499.0
MAX_PRICE = 950.0

def normalize_price(price):
    price = float(price)
    if price < MIN_PRICE:
        transformed = MIN_PRICE + ((price / MIN_PRICE) * 300.0)
        return round(min(max(transformed, MIN_PRICE), MAX_PRICE), 2)
    return round(min(price, MAX_PRICE), 2)

for product in PRODUCTS:
    product['price'] = normalize_price(product.get('price', 0))


def get_normalized_product(product):
    product_copy = product.copy()
    product_copy['price'] = normalize_price(product_copy.get('price', 0))
    return product_copy


def get_normalized_products(products):
    return [get_normalized_product(p) for p in products]


def home(request):
    featured_products = get_normalized_products(PRODUCTS)[:3]
    context = {'featured_products': featured_products}
    return render(request, 'core/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'core/login.html')
            
        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'core/login.html')
            
    return render(request, 'core/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not full_name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'core/signup.html')
            
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'core/signup.html')
            
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email address already exists.")
            return render(request, 'core/signup.html')
            
        first_name = ""
        last_name = ""
        if full_name:
            parts = full_name.split(maxsplit=1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]
                
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'core/signup.html')
            
    return render(request, 'core/signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_staff:
        # Get all orders
        all_orders = Order.objects.all()
        
        # Calculate total revenue from all orders
        revenue_data = all_orders.aggregate(total=Sum('total_amount'))
        total_revenue = revenue_data['total'] or 0
        
        # Get pending orders count
        pending_orders = all_orders.filter(status='Pending')
        
        context = {
            'staff_dashboard': True,
            'total_orders': all_orders.count(),
            'total_customers': User.objects.filter(is_staff=False).count(),
            'total_revenue': total_revenue,
            'pending_orders_count': pending_orders.count(),
            'recent_orders': all_orders.order_by('-created_at')[:5],
        }
    else:
        user_orders = Order.objects.filter(user=request.user)
        wishlist_count = WishlistItem.objects.filter(user=request.user).count()
        profile = getattr(request.user, 'profile', None)
        context = {
            'staff_dashboard': False,
            'dashboard_order_count': user_orders.count(),
            'wishlist_items': wishlist_count,
            'loyalty_points': profile.loyalty_points if profile else 0,
            'recent_orders': user_orders.order_by('-created_at')[:3],
        }
    return render(request, 'core/dashboard.html', context)


def shop(request, category=None):
    products = get_normalized_products(PRODUCTS)
    section = request.GET.get('section')
    price_max_input = request.GET.get('price_max')
    category_title = CATEGORY_LABELS.get(category, category.title() if category else 'All Collections')
    category_sections = CATEGORY_SECTIONS.get(category, [])
    section_title = None

    # Filter products if category is provided
    if category:
        filtered_products = [p for p in products if p['category'].lower() == category.lower()]
        if filtered_products:
            products = filtered_products

    # Further filter products if a section is selected
    if section:
        section_products = [p for p in products if p.get('section') == section]
        if section_products:
            products = section_products
            section_title = next((s['label'] for s in category_sections if s['slug'] == section), section.replace('-', ' ').title())

    try:
        price_max = float(price_max_input) if price_max_input else MAX_PRICE
    except (TypeError, ValueError):
        price_max = MAX_PRICE
    price_max = min(max(price_max, MIN_PRICE), MAX_PRICE)

    products = [p for p in products if MIN_PRICE <= p['price'] <= price_max]

    context = {
        'category': category,
        'category_title': category_title,
        'category_sections': category_sections,
        'section': section,
        'section_title': section_title,
        'price_max': int(price_max),
        'min_price': int(MIN_PRICE),
        'max_price': int(MAX_PRICE),
        'products': products
    }
    return render(request, 'core/shop.html', context)

def product_details(request, product_id):
    product_raw = next((p for p in PRODUCTS if p['id'] == int(product_id)), PRODUCTS[0])
    product = get_normalized_product(product_raw)
    context = {'product': product}
    return render(request, 'core/product_details.html', context)

from .models import CartItem, Order, OrderItem, Profile, WishlistItem

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    items_with_details = []
    subtotal = 0.0
    
    for item in cart_items:
        product_raw = next((p for p in PRODUCTS if p['id'] == item.product_id), None)
        if product_raw:
            product = get_normalized_product(product_raw)
            total_price = float(product['price']) * item.quantity
            subtotal += total_price
            items_with_details.append({
                'cart_item': item,
                'product': product,
                'total_price': total_price
            })
            
    tax_rate = 0.10
    taxes = subtotal * tax_rate
    total = subtotal + taxes
    
    context = {
        'items': items_with_details,
        'subtotal': subtotal,
        'taxes': taxes,
        'total': total,
        'cart_count': sum(item.quantity for item in cart_items)
    }
    return render(request, 'core/cart.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        size = request.POST.get('size', 'M')
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if not product:
            messages.error(request, "Product not found.")
            return redirect('shop')
            
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product_id=int(product_id),
            size=size,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
        messages.success(request, f"Added {product['name']} (Size {size}) to your cart!")
        return redirect('cart')
    return redirect('shop')

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
    if not product:
        messages.error(request, "Product not found.")
        return redirect('shop')

    WishlistItem.objects.get_or_create(user=request.user, product_id=int(product_id))
    messages.success(request, f"{product['name']} added to your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'shop'))

@login_required(login_url='login')
def remove_from_wishlist(request, wishlist_item_id):
    if request.method == 'POST':
        try:
            item = WishlistItem.objects.get(id=wishlist_item_id, user=request.user)
            item.delete()
            messages.success(request, "Item removed from wishlist.")
        except WishlistItem.DoesNotExist:
            messages.error(request, "Wishlist item not found.")
    return redirect('wishlist')

@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in cart.")
    return redirect('cart')

@login_required(login_url='login')
def update_cart_quantity(request, cart_item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                    messages.success(request, "Item removed from cart.")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found.")
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
        
    items_with_details = []
    subtotal = 0.0
    for item in cart_items:
        product_raw = next((p for p in PRODUCTS if p['id'] == item.product_id), None)
        if product_raw:
            product = get_normalized_product(product_raw)
            total_price = float(product['price']) * item.quantity
            subtotal += total_price
            items_with_details.append({
                'cart_item': item,
                'product': product,
                'total_price': total_price
            })
            
    tax_rate = 0.10
    taxes = subtotal * tax_rate
    total = subtotal + taxes
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        payment_method = request.POST.get('payment', 'Credit / Debit Card')
        upi_id = request.POST.get('upi_id', '').strip()
        
        if not first_name or not last_name or not address or not city or not postal_code:
            messages.error(request, "Please fill in all shipping fields.")
        elif payment_method == 'UPI' and not upi_id:
            messages.error(request, "Please enter your UPI ID for UPI payments.")
        else:
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                postal_code=postal_code,
                payment_method=payment_method,
                payment_reference=upi_id if payment_method == 'UPI' else '',
                total_amount=total
            )
            
            for item_data in items_with_details:
                OrderItem.objects.create(
                    order=order,
                    product_id=item_data['cart_item'].product_id,
                    quantity=item_data['cart_item'].quantity,
                    size=item_data['cart_item'].size,
                    price=item_data['product']['price']
                )
            
            cart_items.delete()
            messages.success(request, f"Thank you! Your order #{order.id} has been placed successfully.")
            return redirect('orders')
            
    first_name_initial = request.user.first_name or ""
    last_name_initial = request.user.last_name or ""

    context = {
        'items': items_with_details,
        'subtotal': subtotal,
        'taxes': taxes,
        'total': total,
        'first_name_initial': first_name_initial,
        'last_name_initial': last_name_initial,
    }
    return render(request, 'core/checkout.html', context)

@login_required(login_url='login')
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user)
    wishlist_items = []
    for item in items:
        product_raw = next((p for p in PRODUCTS if p['id'] == item.product_id), None)
        if product_raw:
            product = get_normalized_product(product_raw)
            wishlist_items.append({
                'id': item.id,
                'product': product,
            })
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'core/wishlist.html', context)

@login_required(login_url='login')
def orders(request):
    user_orders = Order.objects.filter(user=request.user)
    orders_with_items = []
    
    for order in user_orders:
        items_list = []
        for item in order.items.all():
            product_raw = next((p for p in PRODUCTS if p['id'] == item.product_id), None)
            product = get_normalized_product(product_raw) if product_raw else None
            items_list.append({
                'item': item,
                'product': product,
                'total_price': float(item.price) * item.quantity
            })
        orders_with_items.append({
            'order': order,
            'items': items_list
        })
        
    context = {
        'orders': orders_with_items
    }
    return render(request, 'core/orders.html', context)

@login_required(login_url='login')
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        bio = request.POST.get('bio', '').strip()
        profile_image = request.FILES.get('profile_image')

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        profile_obj.phone_number = phone_number
        profile_obj.bio = bio
        if profile_image:
            profile_obj.image = profile_image
        profile_obj.save()

        messages.success(request, "Your profile has been updated.")
        return redirect('profile')

    context = {
        'profile': profile_obj,
    }
    return render(request, 'core/profile.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

@login_required(login_url='login')
def update_order_status(request, order_id):
    """Update order status - Admin only"""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('dashboard')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Accepted', 'Shipped', 'Completed', 'Cancelled']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status.")
    
    return redirect('dashboard')
