from database import init_db, insert_influencer

MOCK_INFLUENCERS = [
    {"name": "Sara Fit", "platform": "Instagram", "profile_url": "https://instagram.com/sarafit", "follower_count": 48000, "engagement_rate": 5.2, "niche": "fitness", "content_themes": "workout, gym, nutrition"},
    {"name": "Mike Lifts", "platform": "Instagram", "profile_url": "https://instagram.com/mikelifts", "follower_count": 72000, "engagement_rate": 3.8, "niche": "fitness", "content_themes": "weightlifting, bodybuilding"},
    {"name": "Zara Glow", "platform": "Instagram", "profile_url": "https://instagram.com/zaraglow", "follower_count": 31000, "engagement_rate": 6.1, "niche": "beauty", "content_themes": "skincare, makeup, glowup"},
    {"name": "Priya Style", "platform": "Instagram", "profile_url": "https://instagram.com/priyastyle", "follower_count": 55000, "engagement_rate": 4.4, "niche": "fashion", "content_themes": "ootd, streetstyle, fashion"},
    {"name": "TechWithAlex", "platform": "YouTube", "profile_url": "https://youtube.com/techwithale", "follower_count": 89000, "engagement_rate": 3.2, "niche": "tech", "content_themes": "gadgets, reviews, coding"},
    {"name": "Luna Beauty", "platform": "Instagram", "profile_url": "https://instagram.com/lunabeauty", "follower_count": 22000, "engagement_rate": 7.3, "niche": "beauty", "content_themes": "skincare routine, tutorials"},
    {"name": "FitDad Joe", "platform": "Instagram", "profile_url": "https://instagram.com/fitdadjoe", "follower_count": 18000, "engagement_rate": 5.9, "niche": "fitness", "content_themes": "dad fitness, home workout"},
    {"name": "Crypto Kai", "platform": "YouTube", "profile_url": "https://youtube.com/cryptokai", "follower_count": 67000, "engagement_rate": 4.1, "niche": "fintech", "content_themes": "crypto, investing, defi"},
    {"name": "Mia Runs", "platform": "Instagram", "profile_url": "https://instagram.com/miaruns", "follower_count": 29000, "engagement_rate": 6.8, "niche": "fitness", "content_themes": "running, marathon, cardio"},
    {"name": "StyleByNadia", "platform": "Instagram", "profile_url": "https://instagram.com/stylebynadia", "follower_count": 44000, "engagement_rate": 4.9, "niche": "fashion", "content_themes": "luxury fashion, styling tips"},
    {"name": "GamerZack", "platform": "YouTube", "profile_url": "https://youtube.com/gamerzack", "follower_count": 95000, "engagement_rate": 3.5, "niche": "gaming", "content_themes": "fps games, reviews, esports"},
    {"name": "Mom of Three", "platform": "Instagram", "profile_url": "https://instagram.com/momofthree", "follower_count": 37000, "engagement_rate": 5.6, "niche": "parenting", "content_themes": "motherhood, kids, family"},
    {"name": "VeganVita", "platform": "Instagram", "profile_url": "https://instagram.com/veganvita", "follower_count": 26000, "engagement_rate": 7.1, "niche": "fitness", "content_themes": "vegan diet, plant based, nutrition"},
    {"name": "Kevin Codes", "platform": "YouTube", "profile_url": "https://youtube.com/kevincodes", "follower_count": 41000, "engagement_rate": 4.6, "niche": "tech", "content_themes": "programming, tutorials, python"},
    {"name": "Bella Trends", "platform": "Instagram", "profile_url": "https://instagram.com/bellatrends", "follower_count": 63000, "engagement_rate": 3.9, "niche": "fashion", "content_themes": "trends, haul, fashion week"},
    {"name": "YogaWithSam", "platform": "Instagram", "profile_url": "https://instagram.com/yogawithsam", "follower_count": 15000, "engagement_rate": 8.2, "niche": "fitness", "content_themes": "yoga, mindfulness, wellness"},
    {"name": "FinanceFred", "platform": "YouTube", "profile_url": "https://youtube.com/financefred", "follower_count": 52000, "engagement_rate": 4.3, "niche": "fintech", "content_themes": "personal finance, budgeting, stocks"},
    {"name": "GlowByRia", "platform": "Instagram", "profile_url": "https://instagram.com/glowbyria", "follower_count": 19000, "engagement_rate": 6.9, "niche": "beauty", "content_themes": "natural beauty, skincare, tutorials"},
    {"name": "DadLifeDan", "platform": "Instagram", "profile_url": "https://instagram.com/dadlifedan", "follower_count": 24000, "engagement_rate": 5.4, "niche": "parenting", "content_themes": "fatherhood, family vlogs"},
    {"name": "TechNinja", "platform": "YouTube", "profile_url": "https://youtube.com/techninja", "follower_count": 78000, "engagement_rate": 3.7, "niche": "tech", "content_themes": "unboxing, smartphones, laptops"},
    {"name": "FashionFara", "platform": "Instagram", "profile_url": "https://instagram.com/fashionfara", "follower_count": 33000, "engagement_rate": 5.1, "niche": "fashion", "content_themes": "modest fashion, ethnic wear"},
    {"name": "GymQueen", "platform": "Instagram", "profile_url": "https://instagram.com/gymqueen", "follower_count": 57000, "engagement_rate": 4.7, "niche": "fitness", "content_themes": "gym, women fitness, strength"},
    {"name": "CryptoLisa", "platform": "YouTube", "profile_url": "https://youtube.com/cryptolisa", "follower_count": 42000, "engagement_rate": 4.2, "niche": "fintech", "content_themes": "bitcoin, altcoins, web3"},
    {"name": "MakeupByMia", "platform": "Instagram", "profile_url": "https://instagram.com/makeupbymia", "follower_count": 68000, "engagement_rate": 4.8, "niche": "beauty", "content_themes": "makeup tutorials, looks, products"},
    {"name": "StreetStyleKen", "platform": "Instagram", "profile_url": "https://instagram.com/streetstyleken", "follower_count": 39000, "engagement_rate": 5.3, "niche": "fashion", "content_themes": "streetwear, sneakers, menswear"},
    {"name": "FitMomAmy", "platform": "Instagram", "profile_url": "https://instagram.com/fitmomamy", "follower_count": 21000, "engagement_rate": 6.5, "niche": "fitness", "content_themes": "postnatal fitness, mom workouts"},
    {"name": "GamersHub", "platform": "YouTube", "profile_url": "https://youtube.com/gamershub", "follower_count": 84000, "engagement_rate": 3.4, "niche": "gaming", "content_themes": "game reviews, walkthroughs"},
    {"name": "NaturalNadia", "platform": "Instagram", "profile_url": "https://instagram.com/naturalnadia", "follower_count": 16000, "engagement_rate": 7.8, "niche": "beauty", "content_themes": "natural hair, afro beauty"},
    {"name": "InvestWithIan", "platform": "YouTube", "profile_url": "https://youtube.com/investwithian", "follower_count": 59000, "engagement_rate": 4.0, "niche": "fintech", "content_themes": "investing, ETFs, retirement"},
    {"name": "PapaGeorge", "platform": "Instagram", "profile_url": "https://instagram.com/papageorge", "follower_count": 27000, "engagement_rate": 5.7, "niche": "parenting", "content_themes": "single dad, kids activities"},
    {"name": "RunWithRiya", "platform": "Instagram", "profile_url": "https://instagram.com/runwithriya", "follower_count": 13000, "engagement_rate": 8.9, "niche": "fitness", "content_themes": "trail running, ultramarathon"},
    {"name": "LuxeByLara", "platform": "Instagram", "profile_url": "https://instagram.com/luxebylara", "follower_count": 71000, "engagement_rate": 3.6, "niche": "fashion", "content_themes": "luxury brands, high fashion"},
    {"name": "TechTalkTom", "platform": "YouTube", "profile_url": "https://youtube.com/techtalktom", "follower_count": 46000, "engagement_rate": 4.5, "niche": "tech", "content_themes": "ai tools, software reviews"},
    {"name": "GlossyGirl", "platform": "Instagram", "profile_url": "https://instagram.com/glossygirl", "follower_count": 35000, "engagement_rate": 5.5, "niche": "beauty", "content_themes": "lip care, nail art, beauty hacks"},
    {"name": "EsportsElite", "platform": "YouTube", "profile_url": "https://youtube.com/esportselite", "follower_count": 91000, "engagement_rate": 3.3, "niche": "gaming", "content_themes": "esports, tournaments, pro gaming"},
    {"name": "BabyDaysElla", "platform": "Instagram", "profile_url": "https://instagram.com/babydaysella", "follower_count": 32000, "engagement_rate": 5.8, "niche": "parenting", "content_themes": "newborn, baby care, nursery"},
    {"name": "FitFoodFinn", "platform": "Instagram", "profile_url": "https://instagram.com/fitfoodfinn", "follower_count": 43000, "engagement_rate": 4.9, "niche": "fitness", "content_themes": "meal prep, macros, healthy eating"},
    {"name": "StockSavvy", "platform": "YouTube", "profile_url": "https://youtube.com/stocksavvy", "follower_count": 38000, "engagement_rate": 4.4, "niche": "fintech", "content_themes": "stock market, trading, options"},
    {"name": "ChicWithChloe", "platform": "Instagram", "profile_url": "https://instagram.com/chicwithchloe", "follower_count": 61000, "engagement_rate": 4.1, "niche": "fashion", "content_themes": "chic looks, paris fashion, minimalist"},
    {"name": "SkinDeep", "platform": "Instagram", "profile_url": "https://instagram.com/skindeep", "follower_count": 28000, "engagement_rate": 6.3, "niche": "beauty", "content_themes": "dermatology tips, acne care, spf"},
    {"name": "IndieGamer", "platform": "YouTube", "profile_url": "https://youtube.com/indiegamer", "follower_count": 54000, "engagement_rate": 4.6, "niche": "gaming", "content_themes": "indie games, hidden gems, reviews"},
    {"name": "PowerliftPete", "platform": "Instagram", "profile_url": "https://instagram.com/powerliftpete", "follower_count": 17000, "engagement_rate": 7.5, "niche": "fitness", "content_themes": "powerlifting, strength, competition"},
    {"name": "MomBlogMaya", "platform": "Instagram", "profile_url": "https://instagram.com/momblogmaya", "follower_count": 45000, "engagement_rate": 4.7, "niche": "parenting", "content_themes": "mom tips, toddler, home routines"},
    {"name": "DevDiaries", "platform": "YouTube", "profile_url": "https://youtube.com/devdiaries", "follower_count": 36000, "engagement_rate": 5.0, "niche": "tech", "content_themes": "developer life, startups, coding vlogs"},
    {"name": "BoldBeautyBee", "platform": "Instagram", "profile_url": "https://instagram.com/boldbeautybee", "follower_count": 23000, "engagement_rate": 6.7, "niche": "beauty", "content_themes": "bold makeup, creative looks"},
    {"name": "WealthWave", "platform": "YouTube", "profile_url": "https://youtube.com/wealthwave", "follower_count": 74000, "engagement_rate": 3.9, "niche": "fintech", "content_themes": "wealth building, real estate, passive income"},
    {"name": "SportySpencer", "platform": "Instagram", "profile_url": "https://instagram.com/sportyspencer", "follower_count": 30000, "engagement_rate": 6.0, "niche": "fitness", "content_themes": "crossfit, hiit, sports performance"},
    {"name": "FashionForward", "platform": "Instagram", "profile_url": "https://instagram.com/fashionforward_", "follower_count": 82000, "engagement_rate": 3.5, "niche": "fashion", "content_themes": "fashion forward, editorial, trends"},
    {"name": "GameNight", "platform": "YouTube", "profile_url": "https://youtube.com/gamenight", "follower_count": 66000, "engagement_rate": 4.2, "niche": "gaming", "content_themes": "multiplayer, party games, streams"},
    {"name": "PureSkinPaola", "platform": "Instagram", "profile_url": "https://instagram.com/pureskinpaola", "follower_count": 20000, "engagement_rate": 7.0, "niche": "beauty", "content_themes": "clean beauty, organic skincare"},
    {"name": "TinyHumans", "platform": "Instagram", "profile_url": "https://instagram.com/tinyhumans", "follower_count": 53000, "engagement_rate": 4.8, "niche": "parenting", "content_themes": "kids fashion, parenting hacks, school"},
    {"name": "CyclingCarlos", "platform": "Instagram", "profile_url": "https://instagram.com/cyclingcarlos", "follower_count": 14000, "engagement_rate": 8.5, "niche": "fitness", "content_themes": "cycling, biking, outdoor fitness"},
    {"name": "PennyWise", "platform": "YouTube", "profile_url": "https://youtube.com/pennywise_finance", "follower_count": 47000, "engagement_rate": 4.3, "niche": "fintech", "content_themes": "budgeting, frugal living, saving tips"},
]


def load_mock_data():
    init_db()
    count = 0
    for inf in MOCK_INFLUENCERS:
        row_id = insert_influencer(inf)
        if row_id:
            count += 1
    print(f"[Mock Data] {count} influencers loaded into database")
    return len(MOCK_INFLUENCERS)
