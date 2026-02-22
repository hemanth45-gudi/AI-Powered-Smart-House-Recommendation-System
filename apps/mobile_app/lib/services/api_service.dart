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

  Future<List<House>> getRecommendations(int userId) async {
    final response = await http.get(Uri.parse('$mlBaseUrl/recommend/$userId'));
    if (response.statusCode == 200) {
      final recommendationResponse = RecommendationResponse.fromJson(json.decode(response.body));
      return recommendationResponse.recommendations;
    } else {
      throw Exception('Failed to load recommendations');
    }
  }

  Future<void> updatePreferences(int userId, Map<String, dynamic> prefs) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/$userId/preferences'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(prefs),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to update preferences');
    }
  }
}
