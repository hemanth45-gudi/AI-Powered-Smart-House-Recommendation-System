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
  final String? embeddingId;

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
    this.embeddingId,
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
      embeddingId: json['embedding_id'],
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
      'embedding_id': embeddingId,
    };
  }
}
