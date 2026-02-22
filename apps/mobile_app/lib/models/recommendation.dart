import 'house.dart';

class RecommendationResponse {
  final int userId;
  final List<House> recommendations;

  RecommendationResponse({
    required this.userId,
    required this.recommendations,
  });

  factory RecommendationResponse.fromJson(Map<String, dynamic> json) {
    return RecommendationResponse(
      userId: json['user_id'],
      recommendations: (json['recommendations'] as List)
          .map((i) => House.fromJson(i))
          .toList(),
    );
  }
}
