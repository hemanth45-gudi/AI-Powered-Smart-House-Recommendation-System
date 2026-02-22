import 'package:flutter/material.dart';
import '../models/house.dart';

class HouseCard extends StatelessWidget {
  final House house;

  const HouseCard({super.key, required this.house});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        // Mocking behavior tracking
        print('TRACKING EVENT: User viewed house ${house.id} - "${house.title}"');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Viewing ${house.title}... (Behavior Tracked)')),
        );
      },
      child: Card(
        elevation: 4,
      margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 15),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            height: 180,
            decoration: BoxDecoration(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(15)),
              gradient: LinearGradient(
                colors: [Colors.blue.shade300, Colors.blue.shade900],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Center(
              child: Icon(Icons.home, size: 80, color: Colors.white.withOpacity(0.5)),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      house.title,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    if (house.score != null)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.green.shade100,
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          'Match: ${(house.score! * 100).toStringAsFixed(0)}%',
                          style: TextStyle(color: Colors.green.shade700, fontWeight: FontWeight.bold),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  house.location,
                  style: TextStyle(color: Colors.grey.shade600),
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    _infoBadge(Icons.king_bed, '${house.bedrooms} BR'),
                    const SizedBox(width: 15),
                    _infoBadge(Icons.bathtub, '${house.bathrooms} BA'),
                    const SizedBox(width: 15),
                    _infoBadge(Icons.square_foot, '${house.sqft} sqft'),
                  ],
                ),
                const SizedBox(height: 10),
                Text(
                  '\$${house.price.toStringAsFixed(0)}',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue.shade800,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _infoBadge(IconData icon, String label) {
    return Row(
      children: [
        Icon(icon, size: 16, color: Colors.grey.shade700),
        const SizedBox(width: 4),
        Text(label, style: TextStyle(color: Colors.grey.shade700)),
      ],
    );
  }
}
