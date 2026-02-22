import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/house.dart';
import '../models/recommendation.dart';

class ApiService {
  // Use localhost for emulator (10.0.2.2) or actual local IP for real device
  static const String baseUrl = 'http://10.0.2.2:8000'; 
  static const String mlBaseUrl = 'http://10.0.2.2:8001';

  Future<List<House>> getAllHouses() async {
    final response = await http.get(Uri.parse('$baseUrl/houses/'));
    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);
      return jsonResponse.map((data) => House.fromJson(data)).toList();
    } else {
      throw Exception('Failed to load houses');
    }
  }

  Future<House> createHouse(Map<String, dynamic> houseData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/houses/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(houseData),
    );
    if (response.statusCode == 200 || response.statusCode == 201) {
      return House.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create house');
    }
  }

  Future<List<House>> getRecommendations(int userId) async {
    final response = await http.get(Uri.parse('$mlBaseUrl/recommend/$userId'));
    if (response.statusCode == 200) {
      final recommendationResponse = RecommendationResponse.fromJson(json.decode(response.body));
      return recommendationResponse.recommendations;
    } else {
      throw Exception('Failed to load recommendations');
    }
  }

  Future<List<House>> getAdHocRecommendations(Map<String, dynamic> prefs) async {
    final response = await http.post(
      Uri.parse('$mlBaseUrl/recommend'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(prefs),
    );
    if (response.statusCode == 200) {
      final recommendationResponse = RecommendationResponse.fromJson(json.decode(response.body));
      return recommendationResponse.recommendations;
    } else {
      throw Exception('Failed to load ad-hoc recommendations');
    }
  }

  Future<void> updatePreferences(int userId, Map<String, dynamic> prefs) async {
    final response = await http.post(
      Uri.parse('\$baseUrl/users/\$userId/preferences'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(prefs),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update preferences');
    }
  }

  Future<void> recordInteraction(int userId, int? houseId, String eventType, [Map<String, dynamic>? metadata]) async {
    final response = await http.post(
      Uri.parse('\$baseUrl/interactions/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_id': userId,
        'house_id': houseId,
        'event_type': eventType,
        'metadata_json': metadata,
      }),
    );
    if (response.statusCode != 200) {
      print('Warning: Failed to record interaction (\$eventType)');
    }
  }

  Future<Map<String, dynamic>> getAnalyticsSummary() async {
    final response = await http.get(Uri.parse('$baseUrl/analytics/summary'));
    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    }
    throw Exception('Failed to load analytics summary');
  }

  Future<List<dynamic>> getDailyInteractions() async {
    final response = await http.get(Uri.parse('$baseUrl/analytics/interactions/daily'));
    if (response.statusCode == 200) {
      return json.decode(response.body) as List<dynamic>;
    }
    throw Exception('Failed to load daily interactions');
  }

  Future<List<dynamic>> getTopHouses() async {
    final response = await http.get(Uri.parse('$baseUrl/analytics/top-houses'));
    if (response.statusCode == 200) {
      return json.decode(response.body) as List<dynamic>;
    }
    throw Exception('Failed to load top houses');
  }
}
