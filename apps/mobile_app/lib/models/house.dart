class Explanation {
  final String reason;
  final List<String> topMatches;

  Explanation({required this.reason, required this.topMatches});

  factory Explanation.fromJson(Map<String, dynamic> json) {
    return Explanation(
      reason: json['reason'],
      topMatches: List<String>.from(json['top_matches']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'reason': reason,
      'top_matches': topMatches,
    };
  }
}

class House {
  final int id;
  final String title;
  final String description;
  final double price;
  final String location;
  final int bedrooms;
  final int bathrooms;
  final int sqft;
  final double? score; // Added for ML recommendation ranking
  final double? contentMatch;
  final double? behaviorMatch;
  final String? embeddingId;
  final Explanation? explanation;

  House({
    required this.id,
    required this.title,
    required this.description,
    required this.price,
    required this.location,
    required this.bedrooms,
    required this.bathrooms,
    required this.sqft,
    this.score,
    this.contentMatch,
    this.behaviorMatch,
    this.embeddingId,
    this.explanation,
  });

  factory House.fromJson(Map<String, dynamic> json) {
    return House(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      price: json['price'].toDouble(),
      location: json['location'],
      bedrooms: json['bedrooms'],
      bathrooms: json['bathrooms'],
      sqft: json['sqft'],
      score: json['score']?.toDouble(),
      contentMatch: json['content_match']?.toDouble(),
      behaviorMatch: json['behavior_match']?.toDouble(),
      embeddingId: json['embedding_id'],
      explanation: json['explanation'] != null 
          ? Explanation.fromJson(json['explanation']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'price': price,
      'location': location,
      'bedrooms': bedrooms,
      'bathrooms': bathrooms,
      'sqft': sqft,
      'score': score,
      'content_match': contentMatch,
      'behavior_match': behaviorMatch,
      'embedding_id': embeddingId,
      'explanation': explanation?.toJson(),
    };
  }
}
