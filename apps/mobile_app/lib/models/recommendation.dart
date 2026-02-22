import 'house.dart';

class RecommendationResponse {
  final int? userId;
  final List<House> recommendations;
  final String engine;

  RecommendationResponse({
    this.userId,
    required this.recommendations,
    required this.engine,
  });

  factory RecommendationResponse.fromJson(Map<String, dynamic> json) {
    return RecommendationResponse(
      userId: json['user_id'],
      recommendations: (json['recommendations'] as List)
          .map((i) => House.fromJson(i))
          .toList(),
      engine: json['engine'],
    );
  }
}
